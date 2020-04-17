from mdl_tree import *
import pandas as pd

def buildTree(data):  
    tree = Leaf(data=data) #, attrs_left=allAttributes)
    notAllPure = True
    availableAttributes = allAttributes
    
    while (notAllPure):
        print("Entering 1")
        leaves = tree.getAllLeaves()
        print(tree)
        print(leaves)
        print([leaf.isPure() for leaf in tree.getAllLeaves()])
        print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
        print()
        notAllPure = False
        for leaf in leaves:
            if availableAttributes == []:
                notAllPure = False
                break
            print("Entering 2")
            if not leaf.isPure():
                print(f"Impure leaf {leaf}")
                notAllPure = True
                lowestCost = None
                bestNode = None
                node_attrs_left = availableAttributes.copy()
                for attr in availableAttributes:
                    # print(f"==={attr.name}===")
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
                availableAttributes.remove(bestNode.attribute)
                print(availableAttributes)
                if isinstance(tree, Leaf):
                    tree = bestNode
                else:
                    tree.switchLeaf(leaf, bestNode)
                print(tree)
                print([leaf.isPure() for leaf in tree.getAllLeaves()])
                print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
        # print("End of 1")
    print(f"End with tree: {tree}")
    print(f"End with leaves: {tree.getAllLeaves()}")
    print([leaf.isPure() for leaf in tree.getAllLeaves()])
    print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
    print(tree.getNoData())
    print(tree.getNoExceptions())
    print(tree.getErrorRate())
    return tree

def pruneTree(tree):
    return tree

if __name__ == "__main__":
    shroom_data = pd.read_csv('data/mushrooms.csv')
    # print(shroom_data)
    buildTree(shroom_data)
