import sys
from collections import deque

class GeneralTreeNode():

    def __init__(self, data):
        self.data = data 
        self.children = []
        self.parent = None

    def __str__(self):
        return str(self.data)
 
    def addGeneralTreeChildNode(self, child):
        self.children.append(child)
        child.parent = self

    def preorderTraversal(self):
        lifo = deque()
        nodeList = []
        lifo.append(self)
        while(len(lifo)):
            node = lifo.pop()
            nodeList.append(node)
            reverso = reversed(node.children)
            for child in reverso:
                lifo.append(child)
        return nodeList
 
    def breadthFirstTraversal(self):
        fifo = deque()
        nodeList = []
        root = self
        while (root):
            nodeList.append(root) 
            for child in root.children:
                fifo.append(child)
            if len(fifo) != 0:
                root = fifo.popleft()
            else:
                root = None
        return nodeList



