import sys
import io
import re

ArgcArgvProcessUsage = """
\n
usage: yangparser.py -yang=yang-path -yinout=yinout-path 

and optionally 

-dbg=debug-file-path 

-fixyin=fixyin-file-path 

-yd=yangdir1:yangdir2...

-t1 single line text fields are done on a single line, e.g. <text>single line stuff</text>

-t2 text field substitution where & is changed to &amp;

-t3 text field substitution where < is changed to &lt;

-t4 text field substitution where > is changed to &gt;

-t5 text field substitution where single quote is changed to &apos;

-t6 text field substitution where double quote is changed to &quot;

-t7 text field substitution of white space to a single space

-t8 <reference><info=text/> format,

-t9 indent strings according to level in the yang tree, that is { count not yet closed by } 

-t10 organization text is done in single line format 

-t11 <presence><info=text/> format

-t12 always put a crlf after <text> and  always put a crlf before </text>

The default case is no crlf is added before or after the text tag

-t13 first yin line is always xml version

-t14 module statement yin output includes imports

-t15 <fraction-digits><info=text/> format,

-t16 <must condition=  format

-t17

-t18

-t19

\n
"""
class ArgcArgvProcess:

    def yangFileSet(self, matchy):
        # print("ArgcArgvProcess.yangFileSet", matchy.group(1))
        self.yangFilePath   = matchy.group(1)

    def yinoutFileSet(self, matchy):
        # print("ArgcArgvProcess.yinoutFileSet", matchy.group(1))
        self.yinoutFilePath = matchy.group(1)

    def debugFileSet(self, matchy):
        # print("ArgcArgvProcess.debugFileSet", matchy.group(1))
        self.debugFilePath  = matchy.group(1)

    def fixyinFileSet(self, matchy):
        # print("ArgcArgvProcess.fixyinFileSet", matchy.group(1))
        self.fixyinFilePath = matchy.group(1)

    def yangDirsSet(self, matchy):
        path = (matchy.group(1))
        pathlen = len(path)
        if ((pathlen > 1) and (path[(pathlen-1)] != ':')):
            path = path + ':'
        # print("ArgcArgvProcess.yangDirsSet", path)
        self.yangdirs = ['./']
        pathelems = re.findall(r'(.*?):', path)
        for path in pathelems:
            length = len(path)
            if (path[(length-1)] != '/'):
                self.yangdirs.append((path + '/'))
            else:
                self.yangdirs.append(path)
        # print("ArgcArgvProcess yangDirsSet final:", self.yangdirs)

    def t1Set(self, matchy):
        self.t1 = True

    def t2Set(self, matchy):
        self.t2 = True

    def t3Set(self, matchy):
        self.t3 = True

    def t4Set(self, matchy):
        self.t4 = True

    def t5Set(self, matchy):
        self.t5 = True

    def t6Set(self, matchy):
        self.t6 = True

    def t7Set(self, matchy):
        self.t7 = True

    def t8Set(self, matchy):
        self.t8 = True

    def t9Set(self, matchy):
        self.t9 = True

    def t10Set(self, matchy):
        self.t10 = True

    def t11Set(self, matchy):
        self.t11 = True

    def t12Set(self, matchy):
        self.t12 = True

    def t13Set(self, matchy):
        self.t13 = True

    def t14Set(self, matchy):
        self.t14 = True

    def t15Set(self, matchy):
        self.t15 = True

    def t16Set(self, matchy):
        self.t16 = True

    def t17Set(self, matchy):
        self.t17 = True

    def t18Set(self, matchy):
        self.t18 = True

    def t19Set(self, matchy):
        self.t19 = True

    def yangFileGet(self):
        return self.yangFilePath

    def yinoutFileGet(self):
        return self.yinoutFilePath

    def debugFileGet(self):
        return self.debugFilePath

    def fixyinFileGet(self):
        return self.fixyinFilePath

    def yangDirsGet(self):
        return self.yangdirs

    def t1Get(self):
        return self.t1

    def t2Get(self):
        return self.t2

    def t3Get(self):
        return self.t3

    def t4Get(self):
        return self.t4

    def t5Get(self):
        return self.t5

    def t6Get(self):
        return self.t6

    def t7Get(self):
        return self.t7

    def t8Get(self):
        return self.t8

    def t9Get(self):
        return self.t9

    def t10Get(self):
        return self.t10

    def t11Get(self):
        return self.t11

    def t12Get(self):
        return self.t12

    def t13Get(self):
        return self.t13

    def t14Get(self):
        return self.t14

    def t15Get(self):
        return self.t15

    def t16Get(self):
        return self.t16

    def t17Get(self):
        return self.t17

    def t18Get(self):
        return self.t18

    def t19Get(self):
        return self.t19

    def argParse(self, arg):
        # print("ArgcArgvProcess.argParse(arg)", arg)
        for regularExpressionIndex in range(self.reCount):
            matchy = self.reCompiled[regularExpressionIndex].match(arg)
            if (matchy):
                self.argvRegularExpressions[regularExpressionIndex][1](matchy)
                return
        self.argvErrors += 1

    def __init__(self, argv):
        self.argvRegularExpressions = [
                          (r'-yang=(.*)', self.yangFileSet),
                          (r'-yinout=(.*)', self.yinoutFileSet),
                          (r'-dbg=(.*)', self.debugFileSet),
                          (r'-fixyin=(.*)', self.fixyinFileSet),
                          (r'-yd=(.*)', self.yangDirsSet),
                          (r'-t10', self.t10Set),
                          (r'-t11', self.t11Set),
                          (r'-t12', self.t12Set),
                          (r'-t13', self.t13Set),
                          (r'-t14', self.t14Set),
                          (r'-t15', self.t15Set),
                          (r'-t16', self.t16Set),
                          (r'-t17', self.t17Set),
                          (r'-t18', self.t18Set),
                          (r'-t19', self.t19Set),
                          (r'-t1', self.t1Set),
                          (r'-t2', self.t2Set),
                          (r'-t3', self.t3Set),
                          (r'-t4', self.t4Set),
                          (r'-t5', self.t5Set),
                          (r'-t6', self.t6Set),
                          (r'-t7', self.t7Set),
                          (r'-t8', self.t8Set),
                          (r'-t9', self.t9Set)
                         ]

        self.yangFilePath    = None
        self.yinoutFilePath  = None
        self.debugFilePath   = None
        self.fixyinFilePath  = None
        self.yangdirs        = []
        self.t1              = False
        self.t2              = False
        self.t3              = False
        self.t4              = False
        self.t5              = False
        self.t6              = False
        self.t7              = False
        self.t8              = False
        self.t9              = False
        self.t10             = False
        self.t11             = False
        self.t12             = False
        self.t13             = False
        self.t14             = False
        self.t15             = False
        self.t16             = False
        self.t17             = False
        self.t18             = False
        self.t19             = False

        args = argv[1:]
        argc = len(args)
        self.argvErrors = 0

        self.reCompiled = []
        self.reCount = len(self.argvRegularExpressions)
        for index in range(self.reCount):
            data = self.argvRegularExpressions[index]
            regex = data[0]
            refunc = re.compile(regex)
            self.reCompiled.append(refunc)
        for arg in args:
            self.argParse(arg)

        if ((self.yangFilePath == None) or
            (self.yinoutFilePath == None) or
            (self.argvErrors > 0)):
            print(ArgcArgvProcessUsage)
            sys.exit(1)
