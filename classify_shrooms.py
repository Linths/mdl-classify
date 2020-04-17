from mdl_tree import *
import pandas as pd

def buildTree(data):
    # popularClass = getPopularClass(data)
    # if data['class'].mode().values[0] == 'e':
    #     popularClass = ClassLabel.EDIBLE
    # else:
    #     popularClass = ClassLabel.POISONOUS
    # print(popularClass)
    # print(data['class'].value_counts())
    
    tree = Leaf(data=data)
    print(tree.default_class)

    # print(data.loc[data["cap-shape"] == 'b'])

    # print(tree.toBits())
    if not tree.isPure():
        lowestCost = None
        bestAttr = None
        for attr in allAttributes:
            print(f"==={attr.name}===")
            temp_tree = DecisionNode(attr, attrs_left=allAttributes, data=data)
            # print(temp_tree.toBits())
            print(temp_tree.toString())
        

    return tree

def pruneTree(tree):
    return tree

if __name__ == "__main__":
    shroom_data = pd.read_csv('data/mushrooms.csv')
    # print(shroom_data)
    buildTree(shroom_data)
