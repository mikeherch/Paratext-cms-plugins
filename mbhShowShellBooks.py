# encoding: utf-8
'''
Created on Oct 24, 2017

@author: MikeH
'''
import sys
import codecs
import mbhShellBooks
from mbhShellBooks import booleanize


aShellBookText = None
Params = dict()

if __name__=="__main__":
    SettingsDirectory = "C:\\My Paratext 8 Projects\\"
    Project = "zzAkgUni"
    # Book XXB
    Books = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
    OutputFile = SettingsDirectory + "cms\\checktext.txt"
    Encoding = "65001"
    TextFilter = 'HL'   # optionName in .cms file
    ShowEmpty = 'NO'    # optionName in .cms file
    Test_Mode = True
    HidePageNumbers = 'YES'

    
else:
    from ScriptureObjects import ScriptureText

Params['SettingsDirectory'] = SettingsDirectory
Params['Project'] = Project
Params['Books'] = Books
Params['OutputFile'] = OutputFile
Params['Encoding'] = Encoding
Params['TextFilter'] = TextFilter
Params['ShowEmpty'] = ShowEmpty
Params['HidePageNumbers'] = booleanize(HidePageNumbers)

SB = mbhShellBooks.ShellBookText(Params) 

# def OpenShellBookText(fileOut):
#     global SB
#     SB = 
#     SB.TextFilter = TextFilter
#     SB.ShowEmpty = ShowEmpty
#     SB.OutputFile = fileOut


def commonClose():
    pass
    #say("\n\nFinished Text\n")
    #
    
def processChapter(chapRef, strChapter):
    for strReference in SB.formattedVerses(chapRef, strChapter):
        iIndent = (78-len(strReference)) // 2
        writeout("\r\n%s %s %s" % ("="*iIndent, strReference, "="*iIndent ))
        iIndent = (78-len(SB.StoryFirstRem)) // 2
        if iIndent < 2:
            iIndent = 2
        writeout("\r\n%s %s %s" % (" "*iIndent, SB.StoryFirstRem, " "*iIndent ))
        #sys.stdout.write("\n BOOK: " + strText)
        iIndent = (78-len(SB.StoryTitle)) // 2
        if iIndent < 2:
            iIndent = 2
        writeout("\r\n%s %s" % (" "*iIndent, SB.StoryTitle))
        
        for strMarker, strText in SB.StoryLinesList:
            if strMarker in ['m', 'p', 'pm']:
                strPageNum, strText2 = SB.paging(strText)
                writeout("\r\n%s" % strText2)
            else:
                pass


def say(strText):
    sys.stderr.write(strText)
    
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
    global FileProxyStdout

    FileProxyStdout = codecs.open(OutputFile,'w', 'utf-8')
    Params['StdOut'] = FileProxyStdout
    writeout("Project is " + Project )
    
    # reference is "BBB CC:VV", text is entire text of one chapter
    reference = "XXB 4:12"
    text = Chapter4
    processChapter(reference, text)
    FileProxyStdout.close()
    
def writeout(strText):
    Params['StdOut'].write(strText)

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