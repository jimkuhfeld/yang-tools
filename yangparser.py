#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7

import sys
import io
import re

from YangParse import YangParse
from ArgcArgvProcess import ArgcArgvProcess

"""
see testre.py for testing problem regular expressions
"""

"""

Reference rfc6020.txt when constructing regular expressions for yang statements.

Write a parser from scratch based on Principles of Compiler Design, Aho, Ullman.

Chapter 3, Lexical Analysis

Take the yang buffer and keep a pointer to current start.

Test the regular expressions in order, where it must match from the start point in the buffer.
If it fails, try the next regular expression.

Page 103, section 3.7 looks like the section we want to emulate
look into LEX

We need a list of all regular expressions that define the yang language.

"""

def getFileByType(regularExpression, argument):
    compiledRegex = re.compile(regularExpression)
    matchy = compiledRegex.match(argument)
    if (matchy):
        print('getFileByType', matchy.group(2))
        return matchy.group(2)
    else:
        print('Not a', regularExpression, 'file')
        return None

def main():
    argvtest = ArgcArgvProcess(sys.argv) 
    yangparse = YangParse(argvtest)
    yangparse.tokenize()
    yangparse.printGeneralTree()

if __name__ == "__main__":
    main()
