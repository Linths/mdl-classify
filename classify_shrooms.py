from mdl_tree import *
import pandas as pd

def buildTree(data):
    if data['class'].mode().values[0] == 'e':
        popularClass = ClassLabel.EDIBLE
    else:
        popularClass = ClassLabel.POISONOUS
    print(popularClass)
    # print(data['class'].value_counts())
    
    tree = Leaf(popularClass)
    print(tree.toBits())
    return tree

def pruneTree(tree):
    return tree

if __name__ == "__main__":
    shroom_data = pd.read_csv('data/mushrooms.csv')
    print(shroom_data)
    buildTree(shroom_data)
