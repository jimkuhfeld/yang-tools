import sys
import io
import re

"""
example
<module name="ietf-microwave-radio-link"
        xmlns="urn:ietf:params:xml:ns:yang:yin:1"
        xmlns:mrl="urn:ietf:params:xml:ns:yang:ietf-microwave-radio-link"
        xmlns:yang="urn:ietf:params:xml:ns:yang:ietf-yang-types"
        xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type"
        xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces"
        xmlns:ifprot="urn:ietf:params:xml:ns:yang:ietf-interface-protection"
        xmlns:mw-types="urn:ietf:params:xml:ns:yang:ietf-microwave-types">

"""
class YangImport:

    def __init__(self, debug, yangfilecontents, yangdirs):
        self.debug = debug
        namespaceRe = re.compile(r'module\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{.*?namespace\s+(.*?);.*?prefix\s+(.*?);', re.DOTALL)

        namespace = namespaceRe.search(yangfilecontents)
        if (namespace == None):
            self.moduleString = ""
            return

        self.debug.debugPrint("YangImport, __init__, namespaceRe.search:" + namespace.group(1) + namespace.group(2) + namespace.group(3))
        self.moduleString = '<module name="' + namespace.group(1) + '"\n        xmlns="urn:ietf:params:xml:ns:yang:yin:1"\n        xmlns:' + namespace.group(3) + '=' + namespace.group(2)

        importList = re.findall(r'import\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{.*?prefix\s+(.*?);.*?}', yangfilecontents, re.DOTALL)
        self.debug.debugPrint("YangImport,  __init__, importList:" + str(importList))

        for imp in importList:
            self.debug.debugPrint("inside for imp in importList, with imp:" + str(imp))
            for directory in yangdirs:
                self.debug.debugPrint("inside for directory in yangdirs, with directory:" + directory)
                filename = directory + imp[0] + '.yang'
                self.debug.debugPrint(filename)
                try:
                    filehandle = io.open(filename, "r", encoding="utf-8")
                except FileNotFoundError:
                    self.debug.debugPrint("Couldn't open" + filename)
                    continue
                filecontents = filehandle.read()
                filehandle.close()
                namespace = namespaceRe.search(filecontents)
                prefix = namespace.group(3)
                prefixLen = len(prefix)
                if ((prefixLen > 2) and (prefix[0] == '"') and (prefix[(prefixLen-1)] == '"')):
                    prefix = prefix[1:(prefixLen-1)]
                    self.debug.debugPrint("prefix fix:" + prefix)
                self.moduleString += '\n        xmlns:' + prefix + '=' + namespace.group(2)
                break
        self.moduleString += '>\n'
        self.debug.debugPrint(self.moduleString)

    def getYinModuleStringWithImports(self):
        return self.moduleString

