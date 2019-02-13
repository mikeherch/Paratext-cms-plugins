# encoding: utf-8
'''
Created on Oct 24, 2017

@author: MikeH
'''
import sys
import codecs
import mbhShellBooks

SB = None
Params = dict()

if __name__=="__main__":
    SettingsDirectory = "C:\\My Paratext 8 Projects\\"
    Project = "zzAkgUni"
    # Book XXB
    Books = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
    OutputFile = SettingsDirectory + "cms\\checktext.txt"
    Encoding = "65001"
    TextFilter = 'ALL'   # optionName in .cms file
    ShowEmpty = 'NO'    # optionName in .cms file
    Test_Mode = True

    
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

SB = mbhShellBooks.ShellBookText(Params) 

def commonClose():
    pass
    #say("\n\nFinished Text\n")
    #
    
def processChapter(chapRef, strChapter):
    for strReference in SB.formattedVerses(chapRef, strChapter):
        writeout("%s\t\t%s\n" % (strReference, SB.StoryFirstRem))

def say(strText):
    sys.stderr.write(strText)
    
def cms():
    sys.stdout = codecs.open(OutputFile,'w', 'utf-8')
    #say("stdout.encounding: " + sys.stdout.encoding +"\n")
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
    writeout("Project is " + Project + '\n')
     
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
\m 3. Fomxnx nana ameragho otari avaravari iti.
\m 5. Utughun mavxnx, a rxmarxa rxkxrir amigh rxmxn garxxq nigha zee. Ka mbxkarxsia aghevir rxmxn garxxq mbxkarxsi utui Aram ana sxxqna aghuuqra.
\m 7. Arxmarxa rxkxrir amigh utughun puniiq ko mbxketavxn zava rxmxn garxxq ee aghevi. Iqaaran mav kara ikavxrei iti.
\m 9. Arxmarxa rxkxrir amigh inaghamuuq mbikemi. A rxmxn sisxr non saari rako avagha akui mbxsasi aghuighiri.
\m 11. Arxmarxa rxkxrir amigh ivxra kamaghxusue, nxx mbxkarigh inderasi patx. Nxx mxghasxgha aghaera aghuira amxva maghxra sovxn urutima avaravari nom zeghem patx.
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