from searchObjects import *
import os
import re

setDatabase('history.db')

def getSearchResults(directory, searchString, includeSubDirs = False):
    results = []
    for parent, dirs, files in os.walk(directory):
        regex = re.compile(searchString);
        for found in files:
            if regex.match(found):
                results += [os.path.join(parent, found)]
        if not includeSubDirs:
            break;
    return tuple(results)

def getPotentialRenames(directory, searchString, replaceRegex, includeSubDirs = False):
    results = {}
    for parent, dirs, files in os.walk(directory):
        regex = re.compile(searchString);
        for found in files:
            if regex.match(found):
                results[os.path.join(parent, found)] = os.path.join(parent, re.sub(searchString, replaceRegex, found))
        if not includeSubDirs:
            break;
    return results

def renameFiles(renameResults):
    for key in renameResults.keys():
        os.rename(key, renameResults[key])
