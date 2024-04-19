"""
class BinaryTree:
    node = None
    left = None
    right = None
    level = 0
    
    def __init__(self,nodevalue):
        self.node = nodevalue
        self.level = 0
    
    def SetLeft(self,leftnode):
        self.left = leftnode
        leftnode.level = self.level + 1
        
    def SetRight(self, rightnode):
        self.right = rightnode
        rightnode.level = self.level + 1
        
    def __repr__(self):
        res = ''
        res += str(self.node) + '\n'
        if self.left is not None:
            res += '--|'*self.left.level + str(self.left)
        
        if self.right is not None:
            res += '--|'* self.right.level + str(self.right)
        
    
        return res
    
N0 = BinaryTree('a')
N1 = BinaryTree('b')
N2 = BinaryTree('c')
N3 = BinaryTree('d')
N4 = BinaryTree('e')
N5 = BinaryTree('f')
N6 = BinaryTree('g')


N0.SetLeft(N1)
N0.SetRight(N2)
N1.SetLeft(N3)
N1.SetRight(N4)
N2.SetLeft(N5)
N2.SetRight(N6)

print(N0)
"""

class BinaryTree:
    node = None
    left = None
    right = None
    level = 0
    
    def __init__(self,nodevalue):
        self.node = nodevalue
        self.level = 0
    
    def SetLeft(self,leftnode):
        self.left = leftnode
        leftnode.level = self.level + 1
        
    def SetRight(self, rightnode):
        self.right = rightnode
        rightnode.level = self.level + 1
        
    def __repr__(self):
        res = ''
        res += str(self.node) + '\n'
        if self.left is not None:
            res += '==:'*self.left.level + str(self.left)
        
        if self.right is not None:
            res += '==:'* self.right.level + str(self.right)
    def PrintExp(self):
        res = '('
        
        if self.left is not None:
            res += self.left.PrintExp()
        res += str(self.node)
        if self.right is not None:
            res += self.right.PrintExp()
        res += ')'
        
        
    
        return res
    
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
N1.SetRight(N3)

N3.SetLeft(N2)
N3.SetRight(N7)
    
N2.SetLeft(N5)
N2.SetRight(N6)


print(N0.PrintExp())