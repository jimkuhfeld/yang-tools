import sys
import io

class DebugLog:

    def __init__(self, outputFile):
        if outputFile == None:
            self.handleoutputfile = None
        else:
            self.handleoutputfile = io.open(outputFile, "w", encoding="utf-8")

    def __del__(self):
        if self.handleoutputfile != None:
            self.handleoutputfile.close()

    def debugPrint(self, *argv):
        if self.handleoutputfile == None:
            return
        for arg in argv:  
            self.handleoutputfile.write(arg)
            self.handleoutputfile.write(" ")
        self.handleoutputfile.write("\n")
