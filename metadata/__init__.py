__author__ = 'imsparsh'

# importing libraries
from mutagen import File

# scans song metaData for the future display in recognition
def getSongInfo(inputFile):
    info = {}
    # detect format and type of tags
    file = File(inputFile)
    '''
    if 'APIC:' in file.keys():
        artwork = file.tags['APIC:'].data # access APIC frame and grab the image
        with open('./image.jpg', 'wb') as img:
            img.write(artwork) # write artwork to new image
    '''
    # check for album art existence
    if 'APIC:' in file.keys():
        artwork = file.tags['APIC:'].data # access APIC frame and grab the image
        # extract image
        info['image'] = artwork

    # extract title
    info['title'] = str(file['TIT2'][0])
    # extract artist
    info['artist'] = str(file['TPE1'][0])
    # extract album
    info['album'] = str(file['TALB'][0])
    if 'TDRC' in file.keys():
        # extract year
        info['year'] = str(file['TDRC'][0])
    if 'TCON' in file.keys():
        # extract genre
        info['genre'] = str(file['TCON'][0])
    if 'TPUB' in file.keys():
        # extract publisher
        info['publisher'] = str(file['TPUB'][0])
    # extract length / duration
    info['length'] = str(round(file.info.length/60,2))
    
    return info