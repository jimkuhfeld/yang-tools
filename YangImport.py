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

    def __init__(self, yangfilecontents, yangdirs):
        namespaceRe = re.compile(r'module\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{.*?namespace\s+(.*?);.*?prefix\s+(.*?);', re.DOTALL)

        namespace = namespaceRe.search(yangfilecontents)
        if (namespace == None):
            self.moduleString = ""
            return

        print("YangImport, __init__, namespaceRe.search:", namespace, namespace.group(1), namespace.group(2), namespace.group(3))
        self.moduleString = '<module name="' + namespace.group(1) + '"\n        xmlns="urn:ietf:params:xml:ns:yang:yin:1"\n        xmlns:' + namespace.group(3) + '=' + namespace.group(2)

        importList = re.findall(r'import\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{.*?prefix\s+(.*?);.*?}', yangfilecontents, re.DOTALL)
        print("YangImport,  __init__, importList:", importList)

        print("YangImport init:", yangdirs)
        for imp in importList:
            print("inside for imp in importList, with imp:", imp, "yangdirs:", yangdirs)
            for directory in yangdirs:
                print("inside for directory in yangdirs, with directory:", directory)
                filename = directory + imp[0] + '.yang'
                print(filename)
                try:
                    filehandle = io.open(filename, "r", encoding="utf-8")
                except FileNotFoundError:
                    print("Couldn't open", filename)
                    continue
                filecontents = filehandle.read()
                filehandle.close()
                namespace = namespaceRe.search(filecontents)
                prefix = namespace.group(3)
                prefixLen = len(prefix)
                if ((prefixLen > 2) and (prefix[0] == '"') and (prefix[(prefixLen-1)] == '"')):
                    prefix = prefix[1:(prefixLen-1)]
                    print("prefix fix:", prefix)
                self.moduleString += '\n        xmlns:' + prefix + '=' + namespace.group(2)
                print(namespace)
                break
        self.moduleString += '>\n'
        print(self.moduleString)

    def getYinModuleStringWithImports(self):
        return self.moduleString

