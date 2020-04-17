import numpy as np
from enum import IntEnum
from scipy.special import comb

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

    def toBits(self, attrs_left):
        bitsNeeded = int(np.ceil(np.log2(len(attrs_left))))
        index = [attr.name for attr in attrs_left].index(self.name)
        return format(index, f'0{bitsNeeded}b')

    def toString(self):
        return self.name

class Tree:
    def __init__(self):
        super().__init__()

class DecisionNode(Tree):
    def __init__(self, attribute, attrs_left, data=None, children=None):
        super().__init__()
        self.attribute = attribute
        self.attrs_left = attrs_left # Includes attribute
        self.data = data
        if children == None:
            self.bearChildren()
        else:
            self.children = children
    
    def bearChildren(self):
        leaves = []
        for value in self.attribute.values:
            leaf_data = self.data.loc[self.data[self.attribute.name] == value]
            leaf = Leaf(data=leaf_data)
            leaves.append(leaf)
        self.children = leaves

    def getDescribeCost(self):
        return 1 + self.attribute.getDescribeCost(self.attrs_left) + sum([child.getDescribeCost() for child in self.children])

    def getExceptionsCost(self):
        return sum([child.getExceptionsCost() for child in self.children])
    
    '''Bit string: 1 + <attr-bit-string> + <children-bit-strings>'''
    def toBits(self):
        return '1' + self.attribute.toBits(self.attrs_left) + ' '.join([child.toBits() for child in self.children])

    def toString(self):
        return f"1 {self.attribute.toString()} " + ' '.join([child.toString() for child in self.children])

class Leaf(Tree):
    def __init__(self, default_class=None, data=None):
        # super().__init__()
        self.data = data
        self.no_all = data.shape[0]
        if default_class == None:
            self.setDefaultClass()
        else:
            self.default_class = default_class

    def setDefaultClass(self):
        if self.data.empty:
            self.default_class = ClassLabel.EMPTY
            self.no_exceptions = 0
        elif self.data['class'].mode().values[0] == 'e':
            self.default_class = ClassLabel.EDIBLE
            self.no_exceptions = len(self.data.loc[self.data['class'] == 'd'].values)
        else:
            self.default_class = ClassLabel.POISONOUS
            self.no_exceptions = len(self.data.loc[self.data['class'] == 'e'].values)
        print(self.no_exceptions)
    
    def getDescribeCost(self):
        return 2

    def getExceptionsCost(self):
        return binaryStringComplexity(self.no_all, self.no_exceptions)

    def isPure(self):
        if self.data.empty:
            return True
        return len(self.data['class'].value_counts().values) < 2

    def toBits(self):
        return '0' + format(self.default_class, 'b')

    def toString(self):
        return f"0{self.default_class}"
    
def binaryStringComplexity(n, k):
    b = int(np.ceil((n-1)/2)) # (n+1)/2
    # print(f"n = {n}, k = {k}, b = {b}")
    # print(f"choose = {comb(n, k)}")
    # print(f"log choose = {np.log2(comb(n, k))}")
    assert k <= b
    return np.log2(b + 1) + np.log2(comb(n, k))

allAttributes = [
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

if __name__ == "__main__":
    attr1 = allAttributes[3]
    attr2 = allAttributes[5]
    leaf1 = Leaf(ClassLabel.EDIBLE)
    leaf2 = Leaf(ClassLabel.POISONOUS)
    node = DecisionNode(attr1, allAttributes, children=[leaf1, leaf2])
    assert attr1.toBits(allAttributes) == '00011'
    assert attr1.toBits(allAttributes[:8]) == '011'
    assert leaf1.toBits() == '00'
    assert leaf2.toBits() == '01'
    assert node.toBits() == '1000110001'
    print("Test passed for basic MDL class functionality.")
    