__author__ = 'imsparsh'

#importing all libraries..
import sys
import images_rc
from PyQt4 import QtCore, QtGui
import numpy, scipy, librosa, os, time, gc, multiprocessing as mp, fingerprint as fp

# pymongo driver for MongoDB
from pymongo import *

# metadata for scanning song info
from metadata import *

# locality sensitive hashing function
def hash_func(vecs, projections):
    # dot vector co-variance of the feature vector with randomly generated vector.
    bools = scipy.dot(vecs, projections.T) > 0
    # return a boolean co-variance vector
    return [bool2int(bool_vec) for bool_vec in bools]

#generates the hash for the given boolean co-variance vector
def bool2int(x):
    y = 0
    for i,j in enumerate(x):
        if j: y += 1<<i
    return y

#main fingerprint function
def fingerprint(filepath, songId, projections):
    
    # connecting to dataBase
    cl = MongoClient('localhost',27017)
    dB = cl.lycaon_db
    #initializing environment variables
    framesize = 4096
    hopsize = 4000
    tables = dict()
    # scanning downsampled data in mono (data, sampling rate = 22050)
    x, fs = librosa.load(filepath)
    # retrieving chroma features from audio
    features = librosa.feature.spectral.chromagram(x, fs, n_fft=framesize, hop_length=hopsize).T
    # converting the feature vector to normalized hash vector
    hashes = hash_func(features, projections)
    # total features found
    num_features = len(features)

    del x, fs, features
    
    # unique song key for identification and database setup
    fpath_strp = songId
    # hash vector iteration to build table of distinct hashes
    for h in hashes:
        if tables.has_key(h):
            if tables[h].has_key(fpath_strp):
                tables[h][fpath_strp] += 1
            else:
                tables[h][fpath_strp] = 1
        else:
            tables[h] = {fpath_strp : 1}

    # multiple documents in list to be stored in the database..
    dBfeatures = dB.features
    # inserting the feature count in dataBase
    dBfeatures.insert({fpath_strp:num_features})
               
    # inserting the hashes in dataBase synchronously
    dBhash = dB.hashes
    for key in tables.keys():
        toBeStoredhash = []
        # check for existence of the hash key in hash collection
        diction = dBhash.find({str(key):{'$exists':1}},{'_id':0})
        for cursor in diction:
            toBeStoredhash.append(cursor)
        if toBeStoredhash == []:
            dBhash.insert({str(key) : tables[key]})
        else:
            partial = tables[key]
            for item in toBeStoredhash[0].values():
                for iter in item.keys():
                    partial[unicode(iter)] = item[iter]
            dBhash.update({str(key):{'$exists':1}},{'$set':{str(key):partial}})
                      
            del partial
