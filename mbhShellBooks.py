'''
Created on Jan 9, 2018

@author: MikeH
'''
import re 
ShellBookCategories = ['AG', 'AS', 'BA', 'BG', 'BS', 'CG', 'CM', 'CO', 'DS', 'EN', 
                       'FG', 'FO', 'HL', 'HR', 'HT', 'LM', 'LS', 'MT', 'NG', 'NO', 
                       'NT', 'OT', 'PD', 'PE', 'S', 'S-', 'SB', 'SC', 'SG', 
                       'TG', 'TO', 'OR', 'ST']
class Category:
    def __init__(self, strBookNumber):
        aMatch = re.match(r"c?([A-Z][A-Z])", strBookNumber)
        if aMatch:
            self.Abbr = aMatch.group(1)
        else:
            aMatch = re.match(r"S\-?", strBookNumber)
            if aMatch:
                self.Abbr = aMatch.group(0)
            else:
                self.Abbr = ''
                
    def isShellBook(self):
        return self.Abbr in ShellBookCategories
    
    def isValid(self):
        return self.Abbr > ''
    
    def shellBookChapter(self):
        for i, strAbbr in enumerate(ShellBookCategories):
            if strAbbr == self.Abbr:
                return i+1
        else:
            return -1
        
class ShellBookText:
    def __init__(self, dictParams):
        self.Params = dictParams
        self.ShowEmpty = self.getParam('ShowEmpty')
#         self.OutputMode = 'toText'
        self.TextFilter = self.getParam('TextFilter')
        self.StoryTitle = ''
        self.StoryFirstRem = ''
        self.StoryLinesList = []

    def formattedVerses(self, reference, strChapter):
        if len(strChapter) > 0:
            for strVerse, strVerseNum in self.verseTexts(strChapter):
                if len(strVerse) > 0:
                    blnHasContent = self.formatVerse(strVerse)
                    if self.passFilter(self.StoryFirstRem):
                        if blnHasContent or self.ShowEmpty.upper() == 'YES':
                            iColon = reference.find(':')
                            strBookChap = reference[0:iColon+1]
                            strReference = strBookChap + strVerseNum
                            yield (strReference)
        
           
    def formatVerse(self, strVerse):
        self.StoryLinesList = list()
        self.StoryTitle = ''
        self.StoryFirstRem = ''
        iRemCount = 0
        blnHasContent = False
        
        for strMarker, strText in self.getMarkers(strVerse):
            if strMarker == "v":
                pass
            elif strMarker == "rem":
                iRemCount += 1
                if iRemCount == 1:
                    self.StoryFirstRem = strText
            elif strMarker == "s":
                if len(strText) > 5:
                    blnHasContent = True
                self.StoryTitle = strText
                #sys.stdout.write("\n TITLE: " +  strText)
            elif strMarker in ["m", "p"]:
                if len(strText) > 5:
                    blnHasContent = True
                self.StoryLinesList.append((strMarker, strText))
            else:
                self.StoryLinesList.append((strMarker, strText))
        return blnHasContent
        
    def paging(self, strText):
        aMatch = re.match(r"p\.\d+\s", strText)
        if aMatch: # found a page number
            strPageNum = aMatch.group(0).strip()
        elif self.getParam('RecognizeTraditionalNumbers', False):
            aMatch = re.match(r"\d+\.", strText)
            if aMatch:
                strPageNum = aMatch.group(0).strip()
        if aMatch:
            if self.getParam('HidePageNumbers', False):
                strRestOfText = strText[aMatch.end(0):]
                return strPageNum, strRestOfText
            else:
                return strPageNum, strText
        else:
            return '', strText  # No page number found
        
    def passFilter(self, strRem):
        strFilter = self.TextFilter.upper()
        if strFilter == 'ALL':
            return True
        if len(strFilter) == 2:
            return strFilter in strRem.upper()[0:4]
        if strFilter in ['S', 's']:
            return 'S0' == strRem[0:2]
        if strFilter in strRem.upper():
            return True

    def verseTexts(self, strChapterText):
        """A generator that reads through a Paratext chapter and yields a sequence
        of tuples, each consisting of a Paratext verse and a verse number. A verse 
        starts with \v and continues up to the next
        \v or end of the chapter.
        """
        intCurVerse = strChapterText.find("\\v ",0)
        while True:
            # first get verse number
            iDigit = intCurVerse + 3
            strVerseNum = ''
            while strChapterText[iDigit] in '1234567890-':
                strVerseNum += strChapterText[iDigit]
                iDigit += 1
            
            # find beginning of next verse
            intNextVerse = strChapterText.find("\\v", intCurVerse + 3)
            if intNextVerse == -1:
                yield strChapterText[intCurVerse:len(strChapterText)], strVerseNum
                return
            yield strChapterText[intCurVerse:intNextVerse],strVerseNum
            intCurVerse = intNextVerse
    
    def getMarkers(self, strText):
        if len(strText) > 0:
            intFieldStart = 1
            strMarker = ""
            strContent = ""
            i = intFieldStart
            while True:
                while (i < len(strText)) and strText[i].isalnum():
    #                say("i=%i, char=%s\n" % (i, strText[i]))
                    i += 1
                strMarker = strText[intFieldStart:i]
                i=i+1
                iContentStart = i
                while (i < len(strText)) and strText[i] != "\\":
                    i += 1 
                strContent = strText[iContentStart:i].strip()
    #            say("iContentStart=%s\n" % (iContentStart))
                yield strMarker, strContent
    #            say("%s: i=%i, iContentStart=%i, current char=%s, marker=%s\n" % (strText[0:5], i, iContentStart, strText[i], strMarker))
                i=i+1   # look past \\   
                intFieldStart = i               
                if i >= len(strText):
                    break
    def getParam(self,strParam, zero=''):
        if strParam in self.Params:
            return self.Params[strParam]
        else:
            return zero
        
def booleanize(strYN):
    if strYN:
        return strYN.lower() in ['yes', 'y', 'true', 't']
    else:
        return False
    
def categoryFromBN(strBookNumber):
    # Given a book number, return the category
    aMatch = re.match(r"c?([A-Z][A-Z])", strBookNumber)
    if aMatch:
        return aMatch.group(1)
    
    aMatch = re.match(r"S\-?", strBookNumber)
    if aMatch:
        return aMatch.group(0)

    else:
        return ''
    
