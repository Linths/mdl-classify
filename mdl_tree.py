import numpy as np
from enum import IntEnum
from scipy.special import comb
import math
import pandas as pd
from classify_shrooms import CHOOSE_SHROOM, PARAM_C

class ClassLabel(IntEnum):
    EDIBLE = 0,
    POISONOUS = 1,
    EMPTY = 0

class Attribute:
    def __init__(self, name, values):
        # super().__init__()
        self.name = name
        self.values = values

    def getDescribeCost(self, attrs_left):
        return np.log2(len(attrs_left))
        # bits = self.toBits(attrs_left)
        # return binaryStringComplexity(len(bits), bits.count('1'))

    def toBits(self, attrs_left):
        bitsNeeded = int(np.ceil(np.log2(len(attrs_left))))
        index = [attr.name for attr in attrs_left].index(self.name)
        return format(index, f'0{bitsNeeded}b')

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()

class Tree:
    def __init__(self):
        super().__init__()

class DecisionNode(Tree):
    def __init__(self, attribute, attrs_left, data=None, children=None, depth=None):
        super().__init__()
        self.attribute = attribute
        self.attrs_left = attrs_left # Includes attribute
        self.data = data
        self.depth = depth
        if children == None:
            self.bearChildren()
        else:
            self.children = children
    
    def bearChildren(self):
        leaves = []
        for value in self.attribute.values:
            leaf_data = self.data.loc[self.data[self.attribute.name] == value]
            attrs_left_child = self.attrs_left.copy()
            attrs_left_child.remove(self.attribute)
            leaf = Leaf(data=leaf_data, depth=self.depth+1, attrs_left=attrs_left_child)
            leaves.append(leaf)
        self.children = leaves

    def switchLeaf(self, oldLeaf, newNode):
        d = oldLeaf.depth
        newNode.depth = d
        for i, child in enumerate(self.children):
            if child == oldLeaf:
                self.children[i] = newNode
            elif isinstance(child, DecisionNode):
                child.switchLeaf(oldLeaf, newNode)

    def removeNode(self, node):
        if node == self:
            return self, Leaf(data=node.data, attrs_left=node.attrs_left)
        leaf = None
        for i, child in enumerate(self.children):
            if child == node:
                leaf = Leaf(data=node.data, attrs_left=node.attrs_left)
                self.children[i] = leaf
                return self, leaf
            elif isinstance(child, DecisionNode):
                self.children[i], leaf = child.removeNode(node)
                if leaf != None:
                    return self, leaf
        return self, leaf

    def classify(self, entry):
        value = entry[self.attribute.name]
        index = self.attribute.values.index(value)
        next_step = self.children[index]
        # print(f"{value} {index}")
        return next_step.classify(entry)

    def getErrorRate(self):
        return self.getNoExceptions() / self.getNoData()

    def getNoExceptions(self):
        return sum([child.getNoExceptions() for child in self.children])

    def getNoData(self):
        return sum([child.getNoData() for child in self.children])

    def getAllLeaves(self):
        leaves = []
        for child in self.children:
            leaves.extend(child.getAllLeaves())
        return leaves

    def countDecisionNodes(self):
        # count = 1
        return 1 + sum([child.countDecisionNodes() for child in self.children if isinstance(child, DecisionNode)])
           

    def getAllLeafParents(self):
        parents = []
        includeMe = True
        for child in self.children:
            if isinstance(child, DecisionNode):
                includeMe = False
                parents.extend(child.getAllLeafParents())
        if includeMe:
            parents = [self]
        return parents #[child for child in self.children if isinstance(child, DecisionNode)]

    def getTotalCost(self):
        # print(f"t = {self.getDescribeCost()}, d = {self.getExceptionsCost()}")
        return self.getDescribeCost() + PARAM_C * self.getExceptionsCost()

    def getDescribeCost(self):
        # return 1 + self.attribute.getDescribeCost(self.attrs_left) + sum([child.getDescribeCost() for child in self.children])
        bits = self.toBits()
        return binaryStringComplexity(len(bits), bits.count('1'))

    def getExceptionsCost(self):
        return sum([child.getExceptionsCost() for child in self.children])
    
    '''Bit string: 1 + <attr-bit-string> + <children-bit-strings>'''
    def toBits(self):
        return '1' + self.attribute.toBits(self.attrs_left) + ''.join([child.toBits() for child in self.children])

    def __str__(self):
        return f"1 {self.attribute.__str__()} [" + ' '.join([child.__str__() for child in self.children]) + "]"

    def __repr__(self):
        return self.__str__()

class Leaf(Tree):
    def __init__(self, attrs_left, default_class=None, data=None, depth=None):
        # super().__init__()
        self.depth = depth
        self.attrs_left = attrs_left
        if isinstance(data, pd.DataFrame):
            self.data = data
            self.no_all = data.shape[0]
        # self.attrs_left = attrs_left
        if default_class == None:
            self.setDefaultClass()
        else:
            self.default_class = default_class

    def setDefaultClass(self):
        self.no_e = len(self.data.loc[self.data['class'] == 'e'].values)
        self.no_p = len(self.data.loc[self.data['class'] == 'p'].values)
        if self.data.empty:
            self.default_class = ClassLabel.EMPTY
            self.no_exceptions = 0
            self.no_good = 0
        elif self.data['class'].mode().values[0] == 'e':
            self.default_class = ClassLabel.EDIBLE
            self.no_good = self.no_e
            self.no_exceptions = self.no_p
        else:
            self.default_class = ClassLabel.POISONOUS
            self.no_good = self.no_p
            self.no_exceptions = self.no_e
        # print(f"{self.no_good} ({self.no_exceptions}) ({self.no_all})")

    def classify(self, entry):
        return self.default_class

    def getErrorRate(self):
        return self.getNoExceptions() / self.getNoData()

    def getNoExceptions(self):
        assert self.no_exceptions != None
        return self.no_exceptions

    def getNoData(self):
        assert self.no_all != None
        return self.no_all

    def countDecisionNodes(self):
        return 0

    def getAllLeaves(self):
        return [self]

    def getTotalCost(self):
        return self.getDescribeCost() + PARAM_C * self.getExceptionsCost()

    def getDescribeCost(self):
        # return 2
        bits = self.toBits()
        result = binaryStringComplexity(len(bits), bits.count('1'))
        # print(result)
        return result

    def getExceptionsCost(self):
        return binaryStringComplexity(self.no_all, self.no_exceptions)

    def isPure(self):
        if self.data.empty:
            return True
        return len(self.data['class'].value_counts().values) < 2

    def getEntropy(self):
        return makeEntropyTerm(self.no_e, self.no_all) + makeEntropyTerm(self.no_p, self.no_p)

    def toBits(self):
        return '0' + format(self.default_class, 'b')

    def __str__(self):
        if self.no_e != None and self.no_p != None:
            return f"0{self.default_class} ({self.no_e}|{self.no_p})"
        return f"0{self.default_class}"
    
    def __repr__(self):
        return self.__str__()
    
def binaryStringComplexity(n, k):
    b = np.ceil((n+1)/2)
    assert k <= b
    return n

def makeEntropyTerm(sel_items, all_items):
    if sel_items == 0 or all_items == 0:
        return 0
    return -(sel_items/all_items) * np.log2(sel_items/all_items)

def logComb(n, k):
    if k == 0:
        return np.log2(1)
    pos = sum([np.log2(x) for x in range(n-k+1,n+1)])
    neg = sum([np.log2(x) for x in range(1,k+1)])
    return pos - neg

if CHOOSE_SHROOM:
    ALL_ATTRIBUTES = [
        Attribute("cap-shape", ['b','c','x','f', 'k','s']),
        Attribute("cap-surface", ['f','g','y','s']),
        Attribute("cap-color", ['n','b','c','g','r','p','u','e','w','y']),
        Attribute("bruises", ['t','f']),
        Attribute("odor", ['a','l','c','y','f','m','n','p','s']),
        Attribute("gill-attachment", ['a','d','f','n']),
        Attribute("gill-spacing", ['c','w','d']),
        Attribute("gill-size", ['b','n']),
        Attribute("gill-color", ['k','n','b','h','g', 'r','o','p','u','e','w','y']),
        Attribute("stalk-shape", ['e','t']),
        Attribute("stalk-root", ['b','c','u','e','z','r','?']),
        Attribute("stalk-surface-above-ring", ['f','y','k','s']),
        Attribute("stalk-surface-below-ring", ['f','y','k','s']),
        Attribute("stalk-color-above-ring", ['n','b','c','g','o','p','e','w','y']),
        Attribute("stalk-color-below-ring", ['n','b','c','g','o','p','e','w','y']),
        Attribute("veil-type", ['p','u']),
        Attribute("veil-color", ['n','o','w','y']),
        Attribute("ring-number", ['n','o','t']),
        Attribute("ring-type", ['c','e','f','l','n','p','s','z']),
        Attribute("spore-print-color", ['k','n','b','h','r','o','u','w','y']),
        Attribute("population", ['a','c','n','s','v','y']),
        Attribute("habitat", ['g','l','m','p','u','w','d'])
    ]
else:
    ALL_ATTRIBUTES = [
        Attribute("V1", ['x','o','b']),
        Attribute("V2", ['x','o','b']),
        Attribute("V3", ['x','o','b']),
        Attribute("V4", ['x','o','b']),
        Attribute("V5", ['x','o','b']),
        Attribute("V6", ['x','o','b']),
        Attribute("V7", ['x','o','b']),
        Attribute("V8", ['x','o','b']),
        Attribute("V9", ['x','o','b'])
    ]

if __name__ == "__main__":
    attr1 = ALL_ATTRIBUTES[3]
    attr2 = ALL_ATTRIBUTES[5]
    leaf1 = Leaf(ClassLabel.EDIBLE)
    leaf2 = Leaf(ClassLabel.POISONOUS)
    node = DecisionNode(attr1, ALL_ATTRIBUTES, children=[leaf1, leaf2])
    assert attr1.toBits(ALL_ATTRIBUTES) == '00011'
    assert attr1.toBits(ALL_ATTRIBUTES[:8]) == '011'
    assert leaf1.toBits() == '00'
    assert leaf2.toBits() == '01'
    bits = node.toBits()
    assert node.toBits() == '1000110001'
    assert logComb(6,2) == 3.906890595608518
    print("Test passed for basic MDL class functionality.")
    # print(logComb(2,1))
    # print(logComb(2,0))