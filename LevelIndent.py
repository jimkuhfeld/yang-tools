import sys
import io

class LevelIndent:

    def __init__(self, spacesPerLevel, debug):
        self.spacesPerLevel = spacesPerLevel
        self.debug = debug
        self.levelIndent = "                                                                                                                                                                                                                "
        self.levelIndentLen = len(self.levelIndent)
        self.level = 0

    def incrementLevel(self):
        self.level = self.level + self.spacesPerLevel
        self.debug.debugPrint("incrementLevel ", str(self.level))

    def decrementLevel(self):
        self.level = self.level - self.spacesPerLevel
        if (self.level < 0):
            self.level = 0
        self.debug.debugPrint("decrementLevel ", str(self.level))

    def setLevel(self, level):
        self.level = level
        self.debug.debugPrint("debugSetLevel ", str(self.level))

    def indent(self):
        if (self.level <= self.levelIndentLen):
            return self.levelIndent[0:self.level]
        else:
            return ""
