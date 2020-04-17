import numpy as np
from enum import IntEnum

class ClassLabel(IntEnum):
    EDIBLE = 0,
    POISONOUS = 1

class Attribute:
    def __init__(self, name, values):
        # super().__init__()
        self.name = name
        self.values = values

    def toBits(self, attrs_left):
        bitsNeeded = int(np.ceil(np.log2(len(attrs_left))))
        index = [attr.name for attr in attrs_left].index(self.name)
        return format(index, f'0{bitsNeeded}b')

class Tree:
    def __init__(self):
        super().__init__()

class DecisionNode(Tree):
    def __init__(self, children, attribute, attrs_left):
        super().__init__()
        self.children = children
        self.attribute = attribute
        self.attrs_left = attrs_left # Includes attribute
    
    '''Bit string: 1 + <attr-bit-string> + <children-bit-strings>'''
    def toBits(self):
        return '1' + self.attribute.toBits(self.attrs_left) + ''.join([child.toBits() for child in self.children])

class Leaf(Tree):
    def __init__(self, default_class):
        # super().__init__()
        self.default_class = default_class

    def toBits(self):
        return '0' + format(self.default_class, 'b')


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
    node = DecisionNode([leaf1, leaf2], attr1, allAttributes)
    print(attr1.toBits(allAttributes))       # = 00011
    print(attr1.toBits(allAttributes[:8]))   # = 011
    print(leaf1.toBits())                    # = 00
    print(leaf2.toBits())                    # = 11
    print(node.toBits())
    