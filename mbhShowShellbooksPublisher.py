# encoding: utf-8
'''
Created on Feb 1, 2018
Associated with ShellbooksToPublisher.cms

@author: MikeH
'''
import sys
import codecs
import mbhShellBooks
from mbhCommon import booleanize


aShellBookText = None
Params = dict()

if __name__=="__main__":
    from mbhScriptureObjects import Reference, ScriptureText
    from mbhParatext_tools import BibleBooks
    SettingsDirectory = "C:\\My Paratext 8 Projects\\"
    Project = "ShlBkEn"
    bb = BibleBooks()
    Books = bb.addBooks('0000', ['XXA'])
    OutputFile = SettingsDirectory + "cms\\checktext.txt"
    Encoding = "65001"
    TextFilter = 'AS0013'   # optionName in .cms file
    ShowEmpty = 'NO'    # optionName in .cms file
    Test_Mode = True
    HidePageNumbers = 'YES' # optionName in .cms file
    RecognizeTraditionalNumbers = 'YES'  # optionName in .cms file

    
else:
    from ScriptureObjects import ScriptureText
    Test_Mode = False

Params['SettingsDirectory'] = SettingsDirectory
Params['Project'] = Project
Params['Books'] = Books
Params['OutputFile'] = OutputFile
Params['Encoding'] = Encoding
Params['TextFilter'] = TextFilter
Params['ShowEmpty'] = ShowEmpty
Params['HidePageNumbers'] = booleanize(HidePageNumbers)
Params['RecognizeTraditionalNumbers'] = booleanize(RecognizeTraditionalNumbers)

SB = mbhShellBooks.ShellBookText(Params) 

def commonClose():
    pass
    #say("\n\nFinished Text\n")
    #
    
def processChapter(chapRef, strChapter):
    for strReference in SB.formattedVerses(chapRef, strChapter):
        strIndent = getIndent(strReference, 79, '=')
        writeout("\r\n%s %s %s" % (strIndent, strReference, strIndent ))
        
        strIndent = getIndent(SB.StoryFirstRem, 79, ' ')
        writeout("\r\n%s %s" % (strIndent, SB.StoryFirstRem ))
        
        writeLabeledDivider('title')
        writeout("\r\n%s" % SB.StoryTitle)

        listBalloon = []
        blnFirstM = True
        for index, (strMarker, strText) in enumerate(SB.StoryLinesList):
            if strMarker == 'm':    #new page
                strPageNum, strText2 = SB.paging(strText)
                if blnFirstM:
                    writeLabeledDivider(strPageNum)
                    writeout("\r\n%s" % strText2)
                elif index == len(SB.StoryLinesList) - 1 and strText == "":
                    pass    # ignore. It is probably \m before \v
                else:
                    writeout("\f%s" % strText2)
                blnFirstM = False
            elif strMarker == 'p':  # New paragraph on same page
                writeout("\r%s" % strText)
            elif strMarker == 'pm': #speech balloon
                strPageNum, strText2 = SB.paging(strText)
                if blnFirstM:
                    writeLabeledDivider(strPageNum)
                    writeout("\r\n%s\r\n" % strText2)
                    blnFirstM = False
                else:
                    writeout("\r\n\f%s\r\n" % strText2)
            else:
                pass    # ingnore unknown marker
        
#         for strText in listBalloon:
#             strPageNum, strText2 = SB.paging(strText)
#             writeLabeledDivider(strPageNum)
#             writeout("\r\n%s" % strText2)
            
def say(strText):
    sys.stderr.write(strText)
    
def writeout(strText):
    Params['StdOut'].write(strText)
    
def writeLabeledDivider(strLabel):
    writeout("\r\n---[%s]-------" % strLabel)
    
def getIndent(strText, intPageWidth, strChar):
    intIndent = (intPageWidth-len(strText)) // 2
    if intIndent < 2:
        intIndent = 2
    return strChar * intIndent

def cms():
    sys.stdout = codecs.open(OutputFile,'w', 'utf-8')
    Params['StdOut'] = sys.stdout
    
    scr = ScriptureText(Project) # open input project
    for reference, text in scr.chapters(Books): # process all chapters
        # reference is "BBB CC:VV", text is entire text of one chapter
        processChapter(reference, text)
    commonClose()
    #sys.stdout.close()
    
def test():
    FileProxyStdout = codecs.open(OutputFile,'w', 'utf-8')
    Params['StdOut'] = FileProxyStdout
    writeout("Project is " + Project )   
    
    scr = ScriptureText(Project) # open input project
    for reference, text in scr.chapters(Books): # process all chapters
        # reference is "BBB CC:VV", text is entire text of one chapter
        processChapter(reference, text)
    
#     # reference is "BBB CC:VV", text is entire text of one chapter
#     reference = "XXB 4:12"
#     text = Chapter4
#     processChapter(reference, text)
    FileProxyStdout.close()
    
Chapter4 = r"""\c 4
\m
\v 12
\rem HL0012 Treating Ringworm
\rem SH HL0012o_A4L AG MM p 2013-12-30
\s Avaravari
\m p.3 Fomxnx nana ameragho otari avaravari iti.
\m p.5 Utughun mavxnx, a rxmarxa rxkxrir amigh rxmxn garxxq nigha zee. Ka mbxkarxsia aghevir rxmxn garxxq mbxkarxsi utui Aram ana sxxqna aghuuqra.
\m p.7 Arxmarxa rxkxrir amigh utughun puniiq ko mbxketavxn zava rxmxn garxxq ee aghevi. Iqaaran mav kara ikavxrei iti.
\m p.9 Arxmarxa rxkxrir amigh inaghamuuq mbikemi. A rxmxn sisxr non saari rako avagha akui mbxsasi aghuighiri.
\m p.11 Arxmarxa rxkxrir amigh ivxra kamaghxusue, nxx mbxkarigh inderasi patx. Nxx mxghasxgha aghaera aghuira amxva maghxra sovxn urutima avaravari nom zeghem patx.
\m
\v 26
\rem HL0026 Dangerous Things
\rem SH HL0026o_A4L AG MM p 2013-12-29
\s Iuwein Niaghagh
\m 3. Iuwei non rxpenan itima, ana arxmaghani aqgi ghuisima, a daeqgava arive irxsima, ariv aqn sii.
\m 5. A nomtegha uruaqn zui ma, uvuigha mbxqar aqna akaaq mbxtx.
\m 7. Gumughxn Iuwei guavka avaram mbxkeeqn irx.
\m 9. Ana avaram mbxkeeqn irima, kana akum ana agharo utuu.
\m 11. Igharisirx utughun, a usua asigha kana otxvarx asaraghav itima darigh aqgi ivi.
\m 13. A nomtegha uqun guavtima, tinan arxmagh aqna aqgaria rutu.
\m 15. Iuwei guavtima, apari kana afaman i kegha aqgi ivi.
\m 17. Ana apan amba oqanisima, a no rxpenan andxrxghan itaaqre irx.
\m 19. Gumaghan mav ana nigha gua aaq rxpenan ana atx.
\m 21. A irxghavtima afugh rxpenan ipxn ikegha irava aqn navo utusima, ana afugh kxghavxre irxghav iti.
\p 1. Teghxn Iuwei rafaravaghi?
\p 2. Gena tiq Iuwei amuisi afaravaghara amuighti?
\p 3. Ee man magh ka osxmdxsi ighaaq tii? 
"""

if __name__=="__main__":
    test()
else:
    cms()