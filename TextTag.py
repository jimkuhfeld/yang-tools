import sys
import io
import re

"""
Some yin files use values other than <text>.
For example:
  <organization>
    <text>IETF NETMOD (NETCONF Data Modeling Language) Working Group</text>
  </organization>

might be

<organization>
<info> IETF IPCDN Working Group </info>
</organization>

A text file in the form:

organization=info;
contact=info;

is read and stored in a dictionary in this class.

When, for example, organization is processed,
setCurrentKey('organization') is called.
When processing reaches the text block,
getText is called to, in this case, get 'info'.

"""

class TextTag:

    def __init__(self, yinspecFile):
        self.textDict = {}
        if (yinspecFile == None):
            return

        handleyinspecfile = io.open(yinspecFile, "r", encoding="utf-8")
        yinspecfilecontents = handleyinspecfile.read()
        compiledRegex = re.compile(r'(.*)=(.*);\s*')
        index = 0
        stringlen = len(yinspecfilecontents)
        while (index < stringlen):
            matchy = compiledRegex.match(yinspecfilecontents[index:])
            if (matchy):
                endofstring = (index + matchy.end())
                self.textDict[matchy.group(1)] = matchy.group(2)
                index += matchy.end()
            else:
                break
        handleyinspecfile.close()

    def getText(self, key):
        if ((key == None) or (len(self.textDict) == 0)):
            return 'text'
        retVal = self.textDict[key]
        if (retVal != None):
            return retVal
        return 'text'
