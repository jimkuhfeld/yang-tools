import sys
from collections import deque
from DebugLog import DebugLog
from LevelIndent import LevelIndent
from TagPairs import TagPairs
import re

class YinOutput:

    def __init__(self, debug, argvtest):
        self.debug = debug
        self.level = LevelIndent(2, self.debug)
        self.yinState = None
        self.lifo = deque()
        self.tagpairs = TagPairs(argvtest.fixyinFileGet())
        self.t1 = argvtest.t1Get()
        self.t2 = argvtest.t2Get()
        self.t3 = argvtest.t3Get()
        self.t4 = argvtest.t4Get()
        self.t5 = argvtest.t5Get()
        self.t6 = argvtest.t6Get()
        self.t7 = argvtest.t7Get()
        self.t8 = argvtest.t8Get()
        self.t9 = argvtest.t9Get()
        self.t10 = argvtest.t10Get()
        self.t11 = argvtest.t11Get()
        self.t12 = argvtest.t12Get()
        self.t13 = argvtest.t13Get()
        self.t14 = argvtest.t14Get()
        self.t15 = argvtest.t15Get()
        self.t16 = argvtest.t16Get()
        self.t17 = argvtest.t17Get()
        self.t18 = argvtest.t18Get()
        self.t19 = argvtest.t19Get()
        self.crlfRe = re.compile('\n', re.DOTALL)
        if (self.t13 == False):
            self.yinString = None
        else:
            self.yinString = '<?xml version="1.0" encoding="UTF-8"?>\n'


    def addQuote(self, param):
        length = len(param)
        missing = 0
        if (length < 3):
            missing = 1
        elif ((param[0] != '\"') and (param[(length - 1)] != '\"')):
            missing = 1
        if (missing == 1):
            # print("addQuote manual add", '\"' + param + '\"')
            return ('\"' + param + '\"')
        else:
            # print("addQuote no change", param)
            return param

    def removeQuote(self, param):
        length = len(param)
        if (length < 3):
            return param

        if ((param[0] == '\"') and (param[(length - 1)] == '\"')):
            return param[1:(length-1)]
        else:
            return param

    """
    if -t1 is disabled return False
    if -t1 is enabled and there is no crlf in description return True,  indicating crlf is not printed after an opening text tag
    -f -t1 is enabled and there is  a crlf in description return False, indicating crlf is     printed after an opening text tag 
    """
    def t1Test(self, description):
        if (self.t1 == False):
            self.debug.debugPrint("t1Test", description, "returned False since -t1 was not on the command line")
            return False
        matchy = self.crlfRe.search(description)
        if (matchy == None):
            self.debug.debugPrint("t1Test", description, "returned True, -t1 enabled and no crlf in text")
            return True
        else:
            self.debug.debugPrint("t1Test", description, "returned False, -t1 enabled but there is one or more crlf in text")
            return False
 
    def xmlSubstitution(self, param):
        if (self.t2 == True):
            param = re.sub('&', '&amp;', param)
        if (self.t3 == True):
            param = re.sub('<', '&lt;', param)
        if (self.t4 == True):
            param = re.sub('>', '&gt;', param)
        if (self.t5 == True):
            param = re.sub('\'', '&apos;', param)
        if (self.t6 == True):
            param = re.sub('\"', '&quot;', param)
        if (self.t7 == True):
            param = re.sub('\s+', ' ', param)
        return param

    def yinStackPush(self, closeString):
        self.lifo.append(closeString)
        self.level.incrementLevel()
        self.debug.debugPrint("yinStackPush ", closeString, "length of self.lifo is ", str(len(self.lifo)), str(self.level.getLevel()))

    def yinStateSet(self, newState):
        self.debug.debugPrint("yinStateSet")
        self.yinState = newState

    def yinStateGet(self):
        self.debug.debugPrint("yinStateGet")
        return self.yinState

    def yinStringAppend(self, newString):
        if (self.t9 == False):
            indentedString = newString
        else:
            indentedString = self.level.indent() + newString
        self.debug.debugPrint("yinStringAppend" + indentedString)
        if (self.yinString == None):
            self.yinString = indentedString
        else:
            self.yinString = self.yinString + indentedString

    def yinStringGet(self):
        self.debug.debugPrint("yinStringGet")
        return self.yinString

    def yinTwoParamWithBracePairSet(self, param1, param2):
        self.debug.debugPrint("yinTwoParamWithBracePairSet ", param1, " ", param2)
        inner = self.tagpairs.getInnerTag(param1)
        self.yinStringAppend('<' + param1 + ' ' + inner + '=' + self.addQuote(param2) + '>\n')
        self.yinStackPush('</' + param1 + '>')

    def yinModuleSet(self, moduleString):
        self.debug.debugPrint("yinModuleSet", moduleString)
        self.yinStringAppend(moduleString)
        self.yinStackPush('</module>')

    def yinOneParamWithBracePairSet(self, param1):
        self.debug.debugPrint("yinTwoParamWithBracePairSet ", param1)
        self.yinStringAppend('<' + param1 + '>\n')
        self.yinStackPush('</' + param1 + '>')

    def yinTwoParamsWithSemicolonSet(self, param1, param2):
        self.debug.debugPrint("yinTwoParamsWithSemicolonSet")
        inner = self.tagpairs.getInnerTag(param1)
        if (param1 == "key"):
             param2 = re.sub('\n', ' ', param2)
        self.yinStringAppend('<' + param1 + ' ' + inner + '=' + self.addQuote(param2) + '/>\n')

    def yinTextSet(self, type, description):
        self.debug.debugPrint("input yang text field:" + description)

        if (len(description) == 0):
            working = '<' + type + '>\n' 
            self.yinStringAppend(working)
            self.level.incrementLevel()
            nextchunk = '<' + self.tagpairs.getInnerTag(type) + '/>\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            self.level.decrementLevel()
            nextchunk = '</' + type + '>\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            self.debug.debugPrint("yinTextSet empty:" + working)
            return

        if (self.t10 and (type == 'organization')):
            working = '<' + type + '>\n' 
            self.yinStringAppend(working)
            self.level.incrementLevel()
            nextchunk = '<' + self.tagpairs.getInnerTag(type) + '>'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            nextchunk = self.xmlSubstitution(description) + '</' + self.tagpairs.getInnerTag(type) + '>\n'
            self.yinStringAppend(nextchunk)
            working += nextchunk
            self.level.decrementLevel()
            nextchunk = '</' + type + '>\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            self.debug.debugPrint("yinTextSet t10:" + working)
            return

        if (self.t8 and (type == 'reference')):
            working = '<' + type + ' ' + self.tagpairs.getInnerTag(type) + '="' + self.xmlSubstitution(description) + '"/>\n'
            self.debug.debugPrint("yinTextSet t8:" + working)
            self.yinStringAppend(working)
            return

        if (self.t11 and (type == 'presence')):
            working = '<' + type + ' ' + self.tagpairs.getInnerTag(type) + '="' + self.xmlSubstitution(description) + '"/>\n'
            self.debug.debugPrint("yinTextSet t11:" + working)
            self.yinStringAppend(working)
            return

        if (self.t15 and (type == 'fraction-digits')):
            working = '<' + type + ' ' + self.tagpairs.getInnerTag(type) + '="' + self.xmlSubstitution(description) + '"/>\n'
            self.debug.debugPrint("yinTextSet t15:" + working)
            self.yinStringAppend(working)
            return

        if (self.t16 and (type == 'must')):
            working = '<' + type + ' ' + self.tagpairs.getInnerTag(type) + '="' + self.xmlSubstitution(description) + '"/>\n'
            self.debug.debugPrint("yinTextSet t16:" + working)
            self.yinStringAppend(working)
            return

        singleLine = self.t1Test(description)
        if (singleLine == True):
            working = '<' + type + '>\n' 
            self.yinStringAppend(working)
            self.level.incrementLevel()
            nextchunk = '<' + self.tagpairs.getInnerTag(type) + '>'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            nextchunk = self.xmlSubstitution(description) + '</' + self.tagpairs.getInnerTag(type) + '>\n'
            self.yinStringAppend(nextchunk)
            working += nextchunk
            self.level.decrementLevel()
            nextchunk = '</' + type + '>\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            self.debug.debugPrint("yinTextSet t1:" + working)
            return

        if (self.t12 == True):
            working = '<' + type + '>\n' 
            self.yinStringAppend(working)
            self.level.incrementLevel()
            nextchunk = '<' + self.tagpairs.getInnerTag(type) + '>'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            nextchunk = '\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            nextchunk = self.xmlSubstitution(description)
            working += nextchunk
            self.yinStringAppend(nextchunk)
            nextchunk = '\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            nextchunk = '</' + self.tagpairs.getInnerTag(type) + '>\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            self.level.decrementLevel()
            nextchunk = '</' + type + '>\n'
            working += nextchunk
            self.yinStringAppend(nextchunk)
            self.debug.debugPrint("yinTextSet t12:" + working)
            return

        # The default case adds no crlf after the text tags

        working = '<' + type + '>\n' 
        self.yinStringAppend(working)
        self.level.incrementLevel()
        nextchunk = '<' + self.tagpairs.getInnerTag(type) + '>'
        working += nextchunk
        self.yinStringAppend(nextchunk)
        nextchunk = self.xmlSubstitution(description)
        working += nextchunk
        self.yinStringAppend(nextchunk)
        nextchunk = '</' + self.tagpairs.getInnerTag(type) + '>\n'
        working += nextchunk
        self.yinStringAppend(nextchunk)
        self.level.decrementLevel()
        nextchunk = '</' + type + '>\n'
        working += nextchunk
        self.yinStringAppend(nextchunk)
        self.debug.debugPrint("yinTextSet default:" + working)

    def yinCloseBraceSet(self):
         self.debug.debugPrint("yinCloseBraceSet len(self.lifo) is ", str(len(self.lifo)))
         if (len(self.lifo) != 0):
             closeBraceString = self.lifo.pop()
             self.debug.debugPrint("yinCloseBraceSet ", closeBraceString)
             self.level.decrementLevel()
             self.yinStringAppend(closeBraceString + '\n')
             self.debug.debugPrint("Yin Output\n", self.yinStringGet())

    def yinKeySet(self, keyName):
         self.debug.debugPrint("yinKeySet")
         keyNameSingleLine = re.sub('\n', ' ', keyName)
         self.yinStringAppend('<key value=' + self.addQuote(keyNameSingleLine) + '/>\n')

