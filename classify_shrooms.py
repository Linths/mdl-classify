from mdl_tree import *
import pandas as pd

def buildTree(data):  
    tree = Leaf(data=data, attrs_left=allAttributes)
    notAllPure = True
    
    while (notAllPure):
        print("Entering 1")
        leaves = tree.getAllLeaves()
        print(tree)
        print(leaves)
        print([leaf.isPure() for leaf in tree.getAllLeaves()])
        print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
        print()
        for leaf in leaves:
            print("Entering 2")
            notAllPure = False
            if not leaf.isPure():
                print(f"Impure leaf {leaf}")
                notAllPure = True
                lowestCost = None
                bestNode = None
                for attr in leaf.attrs_left:
                    print(f"==={attr.name}===")
                    node_attrs_left = leaf.attrs_left.copy()
                    node = DecisionNode(attr, attrs_left=node_attrs_left, data=data)
                    # print(node.toBits())
                    # print(node)
                    # print(node.getExceptionsCost())
                    # print(node.getDescribeCost())
                    cost = node.getDescribeCost() + node.getExceptionsCost()
                    if lowestCost == None or cost < lowestCost:
                        lowestCost = cost
                        bestNode = node
                # leaf.parent = node
                print("\nWinner")
                print(lowestCost)
                print(bestNode.attribute.name)
                if isinstance(tree, Leaf):
                    tree = bestNode
                else:
                    tree.switchLeaf(leaf, bestNode)
                print(tree)
                print([leaf.isPure() for leaf in tree.getAllLeaves()])
                print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
    print(f"End with tree: {tree}")
    print(f"End with leaves: {leaves}")
    print([leaf.isPure() for leaf in tree.getAllLeaves()])
    print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
    return tree

def pruneTree(tree):
    return tree

if __name__ == "__main__":
    shroom_data = pd.read_csv('data/mushrooms.csv')
    # print(shroom_data)
    buildTree(shroom_data)
