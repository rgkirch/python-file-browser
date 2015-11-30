from historyInterface import HistoryDBInterface

def setDatabase(database):
    HistoryDBInterface.database = database

class UserObject(object):
    '''Given user name, will get user ID number from db or insert if name not found'''
    def __init__(self, userID):
        self._userID = userID
        self._idNum = UserObject._getUserIdNum(userID)

    def _getUserIdNum(userName):
        with HistoryDBInterface() as histIf:
            row = histIf.getOne('SELECT idNum FROM users WHERE userID = ?', (userName,))
            if row is None:
                histIf.upsert('INSERT INTO users(userID) values(?)', (userName,))
                row = histIf.getOne('SELECT idNum FROM users WHERE userID = ?', (userName,))
            return row[0]
    @property
    def userID(self):
        return self._userID

    @property
    def idNum(self):
        return self._idNum

class SearchObject:
    '''Inserts search object into database on creation'''
    def __init__(self, userIdNum, searchString, replacementStr, directory, searchSubDirs, insert = True):
        self._userIdNum = userIdNum
        self._searchString = searchString
        self._replaceStr = replacementStr
        self._dir = directory
        self._incSubDirs = searchSubDirs
        self._matches = []
        self._newnames = []
        if insert:
            with HistoryDBInterface() as histIf:
                histIf.upsert('INSERT INTO searches(user, search, replace, directory, searchSubDirs) values(?, ?, ?, ?, ?)', (self._userIdNum, self._searchString, self._replaceStr, self._dir, self._incSubDirs))
                self._id = histIf.getOne('SELECT id FROM searches ORDER BY id DESC LIMIT 1')[0] 

    '''Returns a list of count (default 10) searches by user'''
    def getSearchesByUser(userIdNum, count = 10):
        searches = []
        with HistoryDBInterface() as histIf:
            rows = histIf.getRows('SELECT id, user, search, replace, directory, searchSubDirs FROM searches WHERE user = ? ORDER BY id DESC LIMIT ?', (userIdNum, count))
            for row in rows:
                search = SearchObject(*(row[1:]), False)
                search._id = row[0]
                results = histIf.getRows('SELECT fileFound, fileRename FROM results WHERE searchID = ? ORDER BY id DESC', (row[0],))
                for result in results:
                    search._matches += (result[0],)
                    search._newnames += (result[1],)
                searches += [search]
        return searches

    '''adds a single match - throws error is previously added any renames!!'''
    def addMatchOnly(self, matchFileName):
        if self._newnames:
            raise AddedMatchOnlyWithRenamesPresent
        self._matches += [matchFileName]
        self._addMatchesToDB([matchFileName])

    '''adds list of matches - throws error is previously added any renames!!'''
    def addMatchesOnly(self, matchedFileNames):
        if self._newnames:
            raise AddedMatchOnlyWithRenamesPresent
        self._matches += matchedFileNames
        self._addMatchesToDB(matchedFileNames)

    '''adds a renamed pair - throws error if previously added a match only'''
    def addRenamePair(self, matchedFileName, newFileName):
        if len(self._matches) != len(self._newnames):
            raise AddedRenameWithMatchesOnlyPresent
        self._matches += [matchedFileName]
        self._newnames += [newFileName]
        self._addMatchesToDB([matchedFileName], [newFileName])

    '''adds renamed pairs - throws error if previously added a match only or if list of matches does not have same count as list of new file names'''
    def addRenamePairs(self, matchedFileNames, newFileNames):
        if len(self._matches) != len(self._newnames):
            raise AddedRenameWithMatchesOnlyPresent
        if len(matchedFileNames) != len(newFileNames):
            raise MatchesAndRenamesCountNotMatching
        self._matches += [matchedFileNames]
        self._newnames += [newFileNames]
        self._addMatchesToDB(matchedFileNames, newFileNames)

    def _addMatchesToDB(self, matches, renames = None):
        with HistoryDBInterface() as histIf:
            for i in range(0, len(matches)):
                if renames:
                    histIf.upsert('INSERT INTO results(searchID, fileFound, fileRename) values(?, ?, ?)', (self._id, matches[i], renames[i]), False)
                else:
                    histIf.upsert('INSERT INTO results(searchID, fileFound) values(?, ?)', (self._id, matches[i]), False)
            histIf.commit()

    @property
    def userIdNum(self):
        return self._userIdNum

    @property
    def searchString(self):
        return self._searchString

    @property
    def replacementString(self):
        return self._replaceStr

    @property
    def directory(self):
        return self._dir

    @property
    def includeSubDirectories(self):
        return self._incSubDirs

    @property
    def matchedFiles(self):
        return tuple(self._matches)

    @property
    def renamedPairs(self):
        toRet = []
        for i in range(0, len(self._matches)):
            toRet += [(self._matches[i], self._newnames[i])]
        return tuple(toRet)
