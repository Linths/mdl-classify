from mdl_tree import *
import pandas as pd

def buildTree(data):  
    tree = Leaf(data=data)
    not_all_pure = True
    available_attributes = ALL_ATTRIBUTES
    
    while (not_all_pure):
        leaves = tree.getAllLeaves()
        not_all_pure = False
        for leaf in leaves:
            if available_attributes == []:
                not_all_pure = False
                break
            if not leaf.isPure():
                not_all_pure = True
                lowest_cost = None
                best_node = None
                node_attrs_left = available_attributes.copy()
                for attr in available_attributes:
                    node = DecisionNode(attr, attrs_left=node_attrs_left, data=data)
                    cost = node.getTotalCost()
                    if lowest_cost == None or cost < lowest_cost:
                        lowest_cost = cost
                        best_node = node
                available_attributes.remove(best_node.attribute)
                if isinstance(tree, Leaf):
                    tree = best_node
                else:
                    tree.switchLeaf(leaf, best_node)
    print(f"End with tree: {tree}")
    # print(f"End with leaves: {tree.getAllLeaves()}")
    # print([leaf.isPure() for leaf in tree.getAllLeaves()])
    # print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
    # print(tree.getNoData())
    # print(tree.getNoExceptions())
    print(tree.getErrorRate())
    return tree

def pruneTree(tree):
    checked = []
    done = False

    while (not done):
        done = True
        if isinstance(tree, Leaf):
            break
        parents = tree.getAllLeafParents()
        for parent in parents:
            if parent in checked:
                break
            checked.append(parent)
            done = False
            current_cost = tree.getTotalCost()
            current_string = f"{tree}\n{current_cost} = {tree.getDescribeCost()} + {tree.getExceptionsCost()}"
            current_string_costs = f"{current_cost}\t= {tree.getDescribeCost()}\t+ {tree.getExceptionsCost()}"
            tree, leaf = tree.removeNode(parent)
            alt_cost = tree.getTotalCost()
            alt_string = f"{tree}\n{alt_cost} = {tree.getDescribeCost()} + {tree.getExceptionsCost()}"
            alt_string_costs = f"{alt_cost}\t= {tree.getDescribeCost()}\t+ {tree.getExceptionsCost()}"
            if leaf == None:
                print(f"Oops! {parent.attribute}")
            print(parent.attribute.name)
            print(current_string_costs)
            print(alt_string_costs)
            if alt_cost >= current_cost:
                # Update is not better
                tree.switchLeaf(leaf, parent)
            # else:
            #     print()
            #     print(current_string)
            #     print(alt_string)
            #     print(f"Now:\t{tree}")
    print(tree)
    print(tree.getErrorRate())
    return tree

if __name__ == "__main__":
    data = pd.read_csv('data/mushrooms.csv')
    # print(data)
    tree = buildTree(data)
    tree = pruneTree(tree)
