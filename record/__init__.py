__author__ = 'imsparsh'

# importing libraries
from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave

# initialize variables
THRESHOLD = 2000  # audio levels not normalised.
CHUNK_SIZE = 100
MAX_CHUNK = 1300000 # max data to be scanned
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1 # frame size
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 44100 # sampling rate
CHANNELS = 2 # stereo
TRIM_APPEND = RATE / 4

# normalize the recorded audio
def normalize(data_all):
    """Amplify the volume out to max -1dB"""
    # MAXIMUM = 16384
    normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
                        / max(abs(i) for i in data_all))

    r = array('h')
    for i in data_all:
        r.append(int(i * normalize_factor))
    return r

# trim silence in recorded audio
def trim(data_all):
    _from = 0
    _to = len(data_all) - 1
    for i, b in enumerate(data_all):
        if abs(b) > THRESHOLD:
            _from = max(0, i - TRIM_APPEND)
            break

    for i, b in enumerate(reversed(data_all)):
        if abs(b) > THRESHOLD:
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
            break

    return copy.deepcopy(data_all[_from:(_to + 1)])

def record(queue):
    """Record a word or words from the microphone and 
    return the data as an array of signed shorts."""

    # initialize Microphone with stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

    # initialize array with key 'h'
    data_all = array('h')

    while True:
        # little endian, signed short
        data_chunk = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            data_chunk.byteswap()
        # check for minimum sound frequency : discard silence
        if abs(min(data_chunk)) > THRESHOLD:
            data_all.extend(data_chunk)
        # check for high sound frequency
        if abs(max(data_chunk)) > 10000:
            queue.put(max(data_chunk))
        # terminate when desired stream is filled
        if len(data_all) > MAX_CHUNK:
            break
    queue.close()
    '''
    file = open('wave.txt', 'wb')
    file.write(str(data_all))
    file.close()
    '''
    # terminate and release stream
    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    # we trim before normalize as threshhold applies to un-normalized wave, and then normalize
    data_all = normalize(trim(data_all))
    # returns normalised data stream
    return sample_width, data_all

def record_to_file(path, queue, tqueue):
    '''
    Records from the microphone and outputs the resulting data to 'path'
    queue : communicates parent for sending status
    tqueue : communicates parent for live stream
    '''
    sample_width, data = record(queue)
    data = pack('<' + ('h' * len(data)), *data)

    # save the stream to wave
    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()
    tqueue.put(1)
    tqueue.close()

'''
if __name__ == '__main__':
    print("Recording started")
    record_to_file('sample.wav')
    print("Recording completed")
'''