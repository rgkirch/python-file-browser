from searchObjects import *
import os
import re
import zipfile
import lzma, bz2, zlib

compression = zipfile.ZIP_STORED
try:
    import lzma
    copmression = zipfile.ZIP_LZMA
except:
    try:
        import bz2
        compression = zipfile.ZIP_BZIP2
    except:
        try:
            import zlib
            compression = zipfile.ZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED

setDatabase('history.db')

def getSearchResults(user, directory, searchString, includeSubDirs = False):
    results = []
    userObj = UserObject(user)
    srch = SearchObject(userObj.userID, searchString, None, directory, includeSubDirs)
    for parent, dirs, files in os.walk(directory):
        regex = re.compile(searchString);
        for found in files:
            if regex.match(found):
                results += [os.path.join(parent, found)]
        if not includeSubDirs:
            break;
    if (results):
        srch.addMatchesOnly(results)
    return tuple(results)

def getPotentialRenames(user, directory, searchString, replaceRegex, includeSubDirs = False):
    results = {}
    userObj = UserObject(user)
    srch = SearchObject(userObj.userID, searchString, replaceRegex, directory, includeSubDirs)
    for parent, dirs, files in os.walk(directory):
        regex = re.compile(searchString);
        for found in files:
            if regex.match(found):
                results[os.path.join(parent, found)] = os.path.join(parent, re.sub(searchString, replaceRegex, found))
        if not includeSubDirs:
            break;
    if (results):
        #get list to ensure order for matching files to new files
        searched = list(results.keys())
        srch.addRenamePairs(searched, [results[k] for k in searched])
    return results

def renameFiles(user, renameResults):
    for key in renameResults.keys():
        os.rename(key, renameResults[key])

'''creates a new zip - will truncate any existing zipName. Files is a list of filenames'''
def createNewZip(zipName, files):
    print("compression", compression)
    with zipfile.ZipFile(zipName, 'w', compression) as zipper:
        for filename in files:
            zipper.write(filename);

'''If zipName exists, appends files to, else creates new'''
def appendToZip(zipName, files):
    if not os.path.exists(zipName):
        mode = 'w'
    else:
        mode = 'a'
    with zipfile.ZipFile(zipName, mode, compression) as zipper:
        for filename in files:
            zipper.write(filename);

'''Returns a list of filenames in zipName'''
def getListOfFilesInZip(zipName):
    files = []
    with zipfile.ZipFile(zipName) as zipper:
        files += zipper.namelist()
    return files

'''Extracts zipName into given directory (defaults to .)'''
def extractZip(zipName, directory = '.'):
    with zipfile.ZipFile(zipName) as zipper:
        zipper.extractall(directory)

'''Extracts filename from zipName into given directory (defaults to .)'''
def extractOneFile(zipName, filename, directory = '.'):
    with zipfile.ZipFile(zipName) as zipper:
        zipper.extract(filename, directory)

'''Extracts list of filenames from zipName into given directory (defaults to .)'''
def extractFiles(zipName, filenames, directory = '.'):
    with zipfile.ZipFile(zipName) as zipper:
        zipper.extractall(directory, filenames)