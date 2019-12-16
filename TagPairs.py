import sys
import io
import re

"""
Allow user specified tag pairs, since much variability is seen in this area in published yin files.

For example:

<organization>
<text>Text describing the organization.</text>
</organization>

might be in the form:

<organization>
<info>Text describing the organization.</info>
</organization>

A text file in the form:

organization=info;
contact=info;
...

is read and stored in a dictionary in this class, by the __init__ function,
where, in the case of the first line, organization is the key
and info is the value.

When the tag organization is encountered in processing,
getInnerTag is called, e.g.:

inner = getInnerTag('organization')

to return inner set to 'info'.

"""

class TagPairs:

    def __init__(self, tagpairFile):
        self.tagpairDict = {}
        if (tagpairFile == None):
            return

        handletagpairfile = io.open(tagpairFile, "r", encoding="utf-8")
        tagpairfilecontents = handletagpairfile.read()
        compiledRegex = re.compile(r'(.*)=(.*);\s*')
        index = 0
        stringlen = len(tagpairfilecontents)
        while (index < stringlen):
            matchy = compiledRegex.match(tagpairfilecontents[index:])
            if (matchy):
                endofstring = (index + matchy.end())
                self.tagpairDict[matchy.group(1)] = matchy.group(2)
                index += matchy.end()
            else:
                break
        handletagpairfile.close()

    def getInnerTag(self, key):
        if ((key == None) or (len(self.tagpairDict) == 0)):
            return 'name'
        try:
            retVal = self.tagpairDict[key]
        except KeyError:
            retVal = 'name'
        return retVal
