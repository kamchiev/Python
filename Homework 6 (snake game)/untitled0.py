# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 11:15:57 2022

@author: khayo
"""

class BinaryTree:
    node = None
    left = None
    right = None
    level = None
    def __init__(self,nodevalue):
        self.node = nodevalue
        self.level = 0
    def SetRight(self,rightnode):
        self.right = rightnode
        rightnode.level  = self.level + 1
    
    def SetLeft(self,leftnode):
        leftnode.level = self.level +1
        self.left = leftnode
        
        
    def __repr__(self):
        res = ""
        
        if self.left is not None:
            res += '-->' * self.left.level + str(self.left)
        res+=str(self.node) + '\n'
        if self.right is not None:
            res += '-->' *self.right.level + str(self.right)
        
        
        return res
    def PrintExpr(self):
        
        
        
N0 = BinaryTree('/')
N1 = BinaryTree('+')
N2 = BinaryTree('-')
N3 = BinaryTree('*')
N4 = BinaryTree('a')
N5 = BinaryTree('b')
N6 = BinaryTree('c')
N7 = BinaryTree('d')
N8 = BinaryTree('e')

N0.SetLeft(N1)
N0.SetRight(N8)

N1.SetLeft(N4)
N1.SetRingt(N3)

N3.SetLeft(N2)
N3.SetRight(N7)

N2.SetLeft(N5)
N2.SetRight(N6)





print(N0)
    


#pre-visit ==> print - left - right
#in-vist ==> left-print-right
#post-visit ==> left-right-print 