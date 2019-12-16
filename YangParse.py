import sys
import io
import re

from GeneralTreeNode import GeneralTreeNode
from GeneralTreeToYin import GeneralTreeToYin
from DebugLog import DebugLog
from ArgcArgvProcess import ArgcArgvProcess
from YangImport import YangImport

class YangParse:

    def commentFunc(self, node):
        self.debug.debugPrint("comment ")

    def commentSingleLineFunc(self, node):
        self.debug.debugPrint("commentSingleLine ")

    def moduleFunc(self, node):
        if (self.argvtest.t14Get()):
            self.yinParse.yinModuleSet(self.yangimport.getYinModuleStringWithImports())
        else:
            self.yinParse.yinTwoParamWithBracePairSet(node.data[1].group(1), node.data[1].group(2))

    def yangSemicolonFunc(self, node):
        self.debug.debugPrint("semicolon ")

    def unhandledReError(self, node):
        self.debug.debugPrint("ERROR:", node.data[1].group(1), "not handled as part of a full statement")
        sys.exit(1)

    def yangBraceCloseFunc(self, node):
        self.debug.debugPrint("BraceClose ")
        self.yinParse.yinCloseBraceSet()

    def whitespaceFunc(self, node):
        self.debug.debugPrint("whitespace ")

    def complexStringConcatenate(self, input):
        print("complexStringConcatenate:" + input)
        stringlen = len(input)
        index = 0
        result = ''
        while (index < stringlen):
            matchy = self.testreSearch(input[index:], r'\"(.*?)\"', re.DOTALL)
            if (matchy != None):
                result = result + matchy.group(1)
                print("partial result:" + result)
                index += matchy.end()
            else:
                result = result + '\"'
                break
        print("complexStringConcatenate final result:" + result)
        return result

    def complexStringCheck(self, input):
        complex = re.search('"\s+\+\s+"', input)
        if (complex):
            lengthComplex = len(input)
            if ((lengthComplex > 2) and (input[0] != '"') and (input[(lengthComplex - 1)] != '"')):
                input = '"' + input + '"'
            print("COMPLEX:", input)
            return self.complexStringConcatenate(input)
        else:
            return input

    def textFunc(self, node):
        self.debug.debugPrint("text ")
        self.yinParse.yinTextSet(node.data[1].group(1), self.complexStringCheck(node.data[1].group(2)))

    def twoParamWithBraceFunc(self, node):
        self.debug.debugPrint("two params with brace ")
        self.yinParse.yinTwoParamWithBracePairSet(node.data[1].group(1), self.complexStringCheck(node.data[1].group(2)))

    def oneParamWithBraceFunc(self, node):
        self.yinParse.yinOneParamWithBracePairSet(node.data[1].group(1))

    def twoParamWithSemicolon(self, node):
        self.debug.debugPrint("two params with semicolon ")
        self.yinParse.yinTwoParamsWithSemicolonSet(node.data[1].group(1), self.complexStringCheck(node.data[1].group(2)))

    def testreSearch(self, stringToParse, regExString, flags):
        self.debug.debugPrint("\nBegin testreSearch string to parse: ", stringToParse, " regular expression: ", regExString)
        compiledRe = re.compile(regExString, flags)
        matchy = compiledRe.search(stringToParse)
        if (matchy):
            self.debug.debugPrint("Match: regExString " + str(matchy.start()) + str(matchy.end()) + str(matchy.groups()))
            return matchy
        else:
            return None

    def patternComplex(self, node):
        pattern = node.data[1].group(2)
        self.debug.debugPrint("patternComplex:" + pattern)
        stringlen = len(pattern)
        index = 0
        result = ''
        while (index < stringlen):
            matchy = self.testreSearch(pattern[index:], r'\'(.*?)\'', re.DOTALL)
            if (matchy != None):
                result = result + matchy.group(1)
                self.debug.debugPrint("partial result:" + result)
                index += matchy.end()
            else:
                result = result + '\''
                break
        self.debug.debugPrint("patternComplex final result:" + result)
        self.yinParse.yinTwoParamsWithSemicolonSet('pattern', result)

    def keyFunc(self, node):
        self.debug.debugPrint("key ")
        self.yinParse.yinKeySet(node.data[1].group(2))

    def prefixExtensionFunc(self, node):
        self.debug.debugPrint("prefixExtension ")
        self.yinParse.yinTwoParamsWithSemicolonSet(node.data[1].group(1)+node.data[1].group(2)+node.data[1].group(3), node.data[1].group(4))

    def __init__(self, argvtest):
        self.argvtest = argvtest
        self.debug = DebugLog(argvtest.debugFileGet())
        self.yinParse = GeneralTreeToYin(self.debug, argvtest)

        self.yangRegularExpressions = [(r'/\*.*?\*/', re.DOTALL, self.commentFunc, 0),
                          (r'//.*?\n', 0,  self.commentSingleLineFunc, 0),
                          (r';', 0, self.yangSemicolonFunc, 0),
                          (r'({)', 0, self.unhandledReError, 1),
                          (r'}', 0, self.yangBraceCloseFunc, -1),
                          (r'(module)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.moduleFunc, 1),
                          (r'\s+', 0, self.whitespaceFunc, 0),
                          (r'(namespace)\s+(\".*?\");', 0, self.twoParamWithSemicolon, 0),
                          (r'(import)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(organization)\s+\"(.*?)\"',  re.DOTALL, self.textFunc, 0),
                          (r'(contact)\s+\"(.*?)\"',  re.DOTALL, self.textFunc, 0),
                          (r'(description)\s+\"(.*?)\"',  re.DOTALL, self.textFunc, 0),
                          (r'(reference)\s+\"(.*?)\"',  re.DOTALL, self.textFunc, 0),
                          (r'(presence)\s+\"(.*?)\"',  re.DOTALL, self.textFunc, 0),
                          (r'(status)\s+(current|deprecated|obsolete*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(range)\s+\"(.*?)\";', 0, self.twoParamWithSemicolon, 0),
                          (r'(leaf-list)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(choice)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(case)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(enum)\s+(.*?)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(enum)\s+"(.*?)";',  0, self.twoParamWithSemicolon, 0),
                          (r'(enum)\s+(.*?);',  0, self.twoParamWithSemicolon, 0),
                          (r'(notification)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(feature)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(identity)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(container)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(leaf)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(grouping)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(list)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(typedef)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(type)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s*{', 0, self.twoParamWithBraceFunc, 1), # SNMPv2-TC.yang, type string{
                          (r'(type)\s+([_A-Za-z][._\-A-Za-z0-9]*:[_A-Za-z][._\-A-Za-z0-9]*)\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(type)\s+([_A-Za-z][._\-A-Za-z0-9]*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(type)\s+([_A-Za-z][._\-A-Za-z0-9]*)\s+;', 0, self.twoParamWithSemicolon, 0),
                          (r'(type)\s+([_A-Za-z][._\-A-Za-z0-9]*:[_A-Za-z][._\-A-Za-z0-9]*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(revision)\s+([0-9]{4}-[0-9]{2}-[0-9]{2})\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(revision)\s+\"([0-9]{4}-[0-9]{2}-[0-9]{2})\"\s+{', 0, self.twoParamWithBraceFunc, 1),
                          (r'(config)\s+(true|false*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(key)\s+(\".*?\");', re.DOTALL, self.keyFunc, 0),
                          (r'(key)\s+(.*?);', re.DOTALL, self.keyFunc, 0),
                          (r'(value)\s+"(\d*)";', 0, self.twoParamWithSemicolon, 0),
                          (r'(value)\s+(\d*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(position)\s+(\d*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(if-feature)\s+(.*?);',  0, self.twoParamWithSemicolon, 0),
                          (r'(uses)\s+(.*?);',  0, self.twoParamWithSemicolon, 0),
                          (r'(uses)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(mandatory)\s+(.*?);',  0, self.twoParamWithSemicolon, 0),
                          (r'(base)\s+(.*?);',  0, self.twoParamWithSemicolon, 0),
                          (r'(path)\s+(\".*?\");',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(min-elements)\s+(\d*);', 0, self.twoParamWithSemicolon, 0),
                          (r'(augment)\s+(\".*?\")\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(input)\s+{',  re.DOTALL, self.oneParamWithBraceFunc, 1),
                          (r'(output)\s+{',  re.DOTALL, self.oneParamWithBraceFunc, 1),
                          (r'(anyxml)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(bit)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(rpc)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(prefix)\s+\"(.*?)\";', 0, self.twoParamWithSemicolon, 0),
                          (r'(prefix)\s+(.*?);', 0, self.twoParamWithSemicolon, 0),
                          (r'(default)\s+(.*?);', 0, self.twoParamWithSemicolon, 0),
                          (r'(units)\s+(.*?);', 0, self.twoParamWithSemicolon, 0),
                          (r'(length)\s+\"(.*?)\";', 0, self.twoParamWithSemicolon, 0),
                          (r'(pattern)\s+\"(.*?)\";', re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(pattern)\s+(\'.*?\');', re.DOTALL, self.patternComplex, 0),
                          (r'([_A-Za-z][._\-A-Za-z0-9]*)(:)([_A-Za-z][._\-A-Za-z0-9]*)\s+(\".*?\")', 0, self.prefixExtensionFunc, 0),
                          (r'(action)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(action)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(anydata)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(anydata)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(argument)\s+\"(.*?)\"\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(argument)\s+\"(.*?)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(belongs-to)\s+\"(.*?)\"\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(deviate)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(deviate)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(deviation)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(deviation)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(error-app-tag)\s+\"(.*?)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(submodule)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(error-message)\s+\"(.*?)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(extension)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(fraction-digits)\s+(.*?);',  re.DOTALL, self.textFunc, 0),
                          (r'(include)\s+(.*?)\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(include)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(max-elements)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(modifier)\s+(invert-match);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(must)\s+\"(.*?)\"\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(must)\s+\"(.*?)\";',  re.DOTALL, self.textFunc, 0),
                          (r'(must)\s+\'(.*?)\';',  re.DOTALL, self.textFunc, 0),
                          (r'(ordered-by)\s+\"(system|user)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(refine)\s+\"(.*?)\"\s+{',  re.DOTALL, self.twoParamWithBraceFunc, 1),
                          (r'(require-instance)\s+\"(true|false)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(revision-date)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(unique)\s+\"(.*?)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(when)\s+(\".*?\");',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(yang-version)\s+(.*?);',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r'(yin-element)\s+\"(true|false)\";',  re.DOTALL, self.twoParamWithSemicolon, 0),
                          (r"([_A-Za-z][._\-A-Za-z0-9]*)", 0, self.unhandledReError, 0)
                         ]
        """
        regular expression issues in yang to yin translation

        rfc6020 shows
         prefix "acfoo";
       <prefix value="acfoo"/>

       rfc7223 and a yin translation found on the internet shows
     prefix if;
  <prefix value="if"/>

        Two regular expression variations of prefix will be added.

        """
        self.reCompiled = []
        self.reCount = len(self.yangRegularExpressions)
        for index in range(self.reCount):
            data = self.yangRegularExpressions[index]
            regex = data[0]
            flags = data[1]
            refunc = re.compile(regex, flags)
            self.reCompiled.append(refunc)

        self.inputFile = argvtest.yangFileGet()
        self.outputFile = argvtest.yinoutFileGet()
        self.handleinputfile = io.open(self.inputFile, "r", encoding="utf-8")
        self.handleoutputfile = io.open(self.outputFile, "w", encoding="utf-8")
        self.inputfilecontents = self.handleinputfile.read()
        self.handleinputfile.close()

        self.yangimport = YangImport(self.inputfilecontents, argvtest.yangDirsGet())
        self.levelIndent = "                                                                                                                                                                                                "
        self.levelIndentLen = len(self.levelIndent)
        self.root = None

    def __del__(self):
        self.handleoutputfile.close()

    def levelIndentPrint(self, treeLevel):
        if (treeLevel < self.levelIndentLen):
            self.debug.debugPrint(self.levelIndent[0:treeLevel])

    def printGeneralTree(self):
        root = self.root
        breadthList = root.breadthFirstTraversal()
        self.debug.debugPrint('breadthFirstTraversal')
        for node in breadthList:
            regularExpressionIndex = node.data[0]
            matchy                 = node.data[1] # regular expression match object, 
            startOfString          = node.data[2]
            endOfString            = node.data[3]
            treeLevel              = node.data[4]
            if (regularExpressionIndex == 256):
                self.debug.debugPrint("root node")
            else:
                self.levelIndentPrint(treeLevel)
                self.yangRegularExpressions[regularExpressionIndex][2](node)
                self.debug.debugPrint(" match object info start ", str(matchy.start()), " end ",  str(matchy.end()), " ", str(matchy.groups()))
                self.debug.debugPrint( " tree level ", str(treeLevel),  " file index start ", str(startOfString), " end ", str(endOfString))
                self.debug.debugPrint(" ", self.inputfilecontents[startOfString:endOfString])
            self.debug.debugPrint("")
        yinFile = self.yinParse.yinStringGet()
        self.debug.debugPrint("yinStringGet for file write attempt ", yinFile) 
        if (yinFile != None):
            self.handleoutputfile.write(self.yinParse.yinStringGet())

    def tokenize(self):
        index = 0
        stringlen = len(self.inputfilecontents)
        level = 1
        data = 256, None, 0, 0, level
        parent = GeneralTreeNode(data)
        nodeCount = 1
        self.root = parent
        level = 2
        maxlevel = level
        while (index < stringlen):
            for regularExpressionIndex in range(self.reCount):
                matchy = self.reCompiled[regularExpressionIndex].match(self.inputfilecontents[index:])
                if (matchy):
                    endofstring = (index + matchy.end())
                    data = (regularExpressionIndex, matchy, index, endofstring, level)
                    node = GeneralTreeNode(data)
                    nodeCount = nodeCount + 1
                    parent.addGeneralTreeChildNode(node)
                    if (self.yangRegularExpressions[regularExpressionIndex][3] == 1):
                        level = level + 1
                        if (level > maxlevel):
                          maxlevel = level
                        parent = node
                    elif (self.yangRegularExpressions[regularExpressionIndex][3]  == -1):
                        level = level - 1
                        parent = node.parent
                    index += matchy.end()
                    break
            if (matchy == None):
                self.debug.debugPrint("ERROR: Exit, no regular expression match", self.inputfilecontents[index:])
                return
        self.debug.debugPrint("tokenize finished successfully maxlevel", str(maxlevel), str(nodeCount))
