'''
Created on Jun 16, 2018

@author: MikeH
This module contains various methods that are useful to all modules written for 
both Paratext CMS and Development modes.
'''
import sys
import codecs

def isCms():
    """ Returns true if module is running in Paratext CMS environment.
    """
    if sys.argv[0]:
        return False
    else:
        return True

def openUtf8(filename, mode='r'):
    """ Open a file with utf-8 encoding. Permissible modes:
    'r' - read, 'w' - write, 'a' - append, 'r+' - read/write
    """
    f = codecs.open(filename, mode, 'utf-8')
    return f 

def say(strText):
    """ Write strText to stderr
    """
    strNL = '' if strText[-1] == '\n' else '\n'
    sys.stderr.write(strText + strNL)

def booleanize(strYN):
    if strYN:
        if strYN.lower() in ['yes', 'y', 'true', 't']:
            return True
        elif strYN.lower() in ['no', 'n', 'false', 'f']:
            return False
        else:
            return strYN.lower()
    else:
        return False
    
def settingsDirectory():
    """ Find the directory with Paratext 8 projects using the windows registry """
    from _winreg import OpenKey, EnumValue, HKEY_LOCAL_MACHINE

    strPath = r"SOFTWARE\WOW6432Node\Paratext\8"
    try:
        aKey = OpenKey(HKEY_LOCAL_MACHINE, strPath)
        for i in [0,1,2,3,4,5]:
            aName, aValue, irrelevant = EnumValue(aKey,i)
            if aName == 'Settings_Directory':
                return aValue
        return None
    
    except WindowsError:
        # The registry key was not found
        return None
    except:
        raise   