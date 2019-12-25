import sys
import io
import re

from GeneralTreeNode import GeneralTreeNode
from GeneralTreeToYin import GeneralTreeToYin
from DebugLog import DebugLog
from LevelIndent import LevelIndent
from ArgcArgvProcess import ArgcArgvProcess
from YangImport import YangImport
from enum import Enum

"""
    The following will define a state machine

    rfc 7950
6.3.  Statements

   A YANG module contains a sequence of statements.  Each statement
   starts with a keyword, followed by zero or one argument, followed by
   either a semicolon (";") or a block of substatements enclosed within
   braces ("{ }"):

     statement = keyword [argument] (";" / "{" *statement "}")

   The argument is a string, as defined in Section 6.1.2.

6.1.2.  Tokens

   A token in YANG is either a keyword, a string, a semicolon (";"), or
   braces ("{" or "}").  A string can be quoted or unquoted.  A keyword
   is either one of the YANG keywords defined in this document, or a
   prefix identifier, followed by a colon (":"), followed by a language
   extension keyword.  Keywords are case sensitive.  See Section 6.2 for
   a formal definition of identifiers.

"""

class KeywordType(Enum):
    NONE       = 0
    TEXT       = 1
    ALLTHEREST = 2

class StringStart(Enum):
    NO           = 0 
    QUOTESTART   = 1
    NOQUOTESTART = 2

class StatementState(Enum):
    KEYWORD  = 1
    ARGUMENT = 2

class YangParse:

    def commentFunc(self, matchy):
        self.debug.debugPrint("YangParse, commentFunc", matchy.group(1))

    def whitespaceFunc(self, matchy):
        self.debug.debugPrint("YangParse, whitespaceFunc")

    def semicolonFunc(self, matchy):
        self.debug.debugPrint("YangParse, semicolonFunc")
        self.debug.debugPrint(self.keyword, self.argument, ';')
        data = (self.keyword, self.argument, ';', self.level, self.keywordtype)
        # print("debug general tree insert", self.keyword, self.argument, ';', self.level, self.keywordtype)
        node = GeneralTreeNode(data)
        self.nodeCount += 1
        self.parent.addGeneralTreeChildNode(node)

        self.keyword = None
        self.argument = None
        self.stringstart = StringStart.NO
        self.keywordtype = KeywordType.NONE
        self.statementstate = StatementState.KEYWORD

    def openBraceFunc(self, matchy):
        self.debug.debugPrint("YangParse, openBraceFunc")
        if ((self.keyword != None) and (self.argument != None)):
            self.debug.debugPrint(self.keyword, self.argument, '{')
        data = (self.keyword, self.argument, '{', self.level, self.keywordtype)
        # print("debug general tree insert", self.keyword, self.argument, '{', self.level, self.keywordtype)
        node = GeneralTreeNode(data)
        self.nodeCount += 1
        self.parent.addGeneralTreeChildNode(node)
        self.parent = node
        self.level += 1
        if (self.maxlevel < self.level):
            self.maxlevel = self.level

        self.keyword = None
        self.argument = None
        self.stringstart = StringStart.NO
        self.keywordtype = KeywordType.NONE
        self.statementstate = StatementState.KEYWORD

    def closeBraceFunc(self, matchy):
        self.debug.debugPrint("YangParse, closeBraceFunc")
        self.debug.debugPrint('}')
        self.level -= 1
        data = (None, None, '}', self.level, KeywordType.NONE)
        # print("debug general tree insert", '}', self.level)
        node = GeneralTreeNode(data)
        self.nodeCount += 1
        self.parent.addGeneralTreeChildNode(node)
        self.parent = node.parent

        self.keyword = None
        self.argument = None
        self.stringstart = StringStart.NO
        self.keywordtype = KeywordType.NONE
        self.statementstate = StatementState.KEYWORD

    def keywordTextFunc(self, matchy):
        self.debug.debugPrint("YangParse, keywordYangFunc", matchy.group(1))
        self.keyword = matchy.group(1)
        self.keywordtype = KeywordType.TEXT
        self.statementstate = StatementState.ARGUMENT

    def keywordAllTheRestFunc(self, matchy):
        self.debug.debugPrint("YangParse, keywordYangFunc", matchy.group(1))
        self.keyword = matchy.group(1)
        self.keywordtype = KeywordType.ALLTHEREST
        self.statementstate = StatementState.ARGUMENT

    def prefixExtensionFunc(self, matchy):
        self.debug.debugPrint("YangParse, prefixExtensionFunc", matchy.group(0))
        self.keyword = matchy.group(0)
        self.keywordtype = KeywordType.ALLTHEREST
        self.statementstate = StatementState.ARGUMENT

    def unquotedStringFunc(self, matchy):
        self.debug.debugPrint("YangParse, unquotedStringFunc", matchy.group(1))
        if (self.stringstart == StringStart.NO):
            self.argument = matchy.group(1)
            self.stringstart = StringStart.NOQUOTESTART

    def quotedStringFunc(self, matchy):
        self.debug.debugPrint("YangParse, quotedStringFunc", matchy.group(1))
        if ((self.stringstart == StringStart.NO) and  (self.argument == None)):
            self.argument = matchy.group(1)
            self.stringstart = StringStart.QUOTESTART
        elif (self.stringstart == StringStart.QUOTESTART):
            self.argument += matchy.group(1)

    def __init__(self, argvtest):
        self.argvtest = argvtest
        self.debug = DebugLog(argvtest.debugFileGet())
        self.yinParse = GeneralTreeToYin(self.debug, argvtest)

        self.keyword = None
        self.argument = None
        self.stringstart = StringStart.NO
        self.keywordtype = KeywordType.NONE
        self.statementstate = StatementState.KEYWORD

        self.yangRegularExpressions = [(r'(/\*.*?\*/)', re.DOTALL, self.commentFunc),
                          (r'(//.*?\n)', 0,  self.commentFunc),
                          (r'\s+', 0, self.whitespaceFunc),
                          (r';', 0, self.semicolonFunc),
                          (r'{', 0, self.openBraceFunc),
                          (r'}', 0, self.closeBraceFunc),
                          (r'(contact|description|fraction-digits|must|organization|presence|reference)', 0, self.keywordTextFunc),
                          (r'(action|anydata|anyxml|argument|augment|base|belongs-to|bit|case|choice|config|container|default|deviate|deviation|enum|error-app-tag|error-message|extension|feature|grouping|identity|if-feature|import|include|input|key|leaf-list|leaf|length|list|mandatory|max-elements|min-elements|modifier|module|namespace|notification|ordered-by|output|path|pattern|position|prefix|range|refine|require-instance|revision-date|revision|rpc|status|submodule|typedef|type|unique|units|uses|value|when|yang-version|yin-element)', 0, self.keywordAllTheRestFunc),
                          (r'([_A-Za-z][._\-A-Za-z0-9]*):([_A-Za-z][._\-A-Za-z0-9]*)', 0, self.prefixExtensionFunc),
                          (r'([^\s\'\";{}]+)', re.DOTALL,  self.unquotedStringFunc), # additional filtering required of comment sequences
                          (r'\'(.*?)\'', re.DOTALL, self.quotedStringFunc),
                          (r'\"(.*?)\"', re.DOTALL, self.quotedStringFunc)
                         ]
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

        self.yangimport = YangImport(self.debug, self.inputfilecontents, argvtest.yangDirsGet())
        self.root = None
        self.makeGeneralTree()

    def __del__(self):
        self.handleoutputfile.close()

    def makeGeneralTree(self):
        index = 0
        stringlen = len(self.inputfilecontents)
        self.level = 0
        self.maxlevel = self.level
        data = "root", None, ';', self.level, KeywordType.NONE
        self.parent = GeneralTreeNode(data)
        self.nodeCount = 1
        self.root = self.parent
        while (index < stringlen):
            for regularExpressionIndex in range(self.reCount):

                if ((self.statementstate == StatementState.ARGUMENT) and 
                    ((self.yangRegularExpressions[regularExpressionIndex][2] == self.keywordTextFunc) or
                     (self.yangRegularExpressions[regularExpressionIndex][2] == self.keywordAllTheRestFunc) or
                     (self.yangRegularExpressions[regularExpressionIndex][2] == self.prefixExtensionFunc))):
                    continue

                self.debug.debugPrint("tokenize: regularExpressionIndex", str(regularExpressionIndex), self.yangRegularExpressions[regularExpressionIndex][0])
                matchy = self.reCompiled[regularExpressionIndex].match(self.inputfilecontents[index:])
                if (matchy):
                    endofstring = (index + matchy.end())
                    if (matchy.end() == 0):
                        sys.exit(1)
                    index += matchy.end()
                    self.yangRegularExpressions[regularExpressionIndex][2](matchy)
                    break
                else:
                    self.debug.debugPrint("tokenize: regular expression didn't match")

            if (matchy == None):
                self.debug.debugPrint("ERROR: Exit, no regular expression match", self.inputfilecontents[index:])
                return
        self.debug.debugPrint("tokenize finished successfully maxlevel", str(self.maxlevel))

    def makeYin(self):
        root = self.root
        breadthList = root.breadthFirstTraversal()
        self.debug.debugPrint('breadthFirstTraversal')
        for node in breadthList:
            keyword      = node.data[0]
            argument     = node.data[1]
            statementEnd = node.data[2]
            treeLevel    = node.data[3]
            keywordType  = node.data[4]

            if (keyword == 'root'):
                self.debug.debugPrint("root node")
            elif ((statementEnd == ';') and (keyword != None) and (argument != None) and (keywordType == KeywordType.TEXT)):
                self.yinParse.yinTextSet(keyword, argument)
            elif ((statementEnd == ';') and (keyword != None) and (argument != None) and (keywordType == KeywordType.ALLTHEREST)):
                self.yinParse.yinTwoParamsWithSemicolonSet(keyword, argument)
            elif ((statementEnd == '{') and (keyword != None) and (argument != None) and (keyword == "module") and self.argvtest.t14Get()):
                self.yinParse.yinModuleSet(self.yangimport.getYinModuleStringWithImports())
            elif ((statementEnd == '{') and (keyword != None) and (argument != None)):
                self.yinParse.yinTwoParamWithBracePairSet(keyword, argument)
            elif ((statementEnd == '{') and (keyword != None) and (argument == None)):
                self.yinParse.yinOneParamWithBracePairSet(keyword)
            elif (statementEnd == '}'):
                self.yinParse.yinCloseBraceSet()

        yinFile = self.yinParse.yinStringGet()
        self.debug.debugPrint("yinStringGet for file write attempt ", yinFile) 
        if (yinFile != None):
            self.debug.debugPrint("YangParse, tokenize, About to write yin file.", yinFile)
            self.handleoutputfile.write(yinFile)
            self.handleoutputfile.flush() # mysterious fix for problem seen only in patterntest.yang test, where nothing was written to the yin file.

    def makeTreeOutputFormat(self):
        root = self.root
        breadthList = root.breadthFirstTraversal()
        self.debug.debugPrint('breadthFirstTraversal')
        indent = LevelIndent(1, self.debug)

        for node in breadthList:
            keyword      = node.data[0]
            argument     = node.data[1]
            statementEnd = node.data[2]
            treeLevel    = node.data[3]
            keywordType  = node.data[4]
            indent.setLevel(treeLevel)
            # print("debug general tree walk", keyword, argument, statementEnd, treeLevel, keywordType)
            if (keyword == 'root'):
                self.debug.debugPrint("root node")
            elif (keyword != None) and (argument != None):
                print(indent.indent() + keyword, argument, statementEnd)
            elif (keyword != None):
                print(indent.indent() + keyword, statementEnd)
            else:
                print(indent.indent() + statementEnd)
