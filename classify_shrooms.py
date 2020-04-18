from mdl_tree import *
from c45 import *
import pandas as pd

class MDL:
    def __init__(self):
        super().__init__()

    def buildTree(self, data):  
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
        # print(f"End with tree: {tree}")
        # print(f"End with leaves: {tree.getAllLeaves()}")
        # print([leaf.isPure() for leaf in tree.getAllLeaves()])
        # print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
        # print(tree.getNoData())
        # print(tree.getNoExceptions())
        print(f"After building {tree.getErrorRate()}")
        return tree

    def pruneTree(self, tree):
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
                # print(parent.attribute.name)
                # print(current_string_costs)
                # print(alt_string_costs)
                if alt_cost >= current_cost:
                    # Update is not better
                    tree.switchLeaf(leaf, parent)
                # else:
                #     print()
                #     print(current_string)
                #     print(alt_string)
                #     print(f"Now:\t{tree}")
        # print(tree)
        print(f"After pruning {tree.getErrorRate()}")
        return tree

    def trainTree(self, data):
        tree = self.buildTree(data)
        return self.pruneTree(tree)

    def fit(self, train_data, train_labels):
        train_data["class"] = train_labels
        tree = self.trainTree(train_data)
        self.tree = tree

    def predict(self, X):
        return ['e' if self.tree.classify(row) == ClassLabel.EDIBLE else 'p' for i, row in X.iterrows()]
    
    def get_params(self, deep=False):
        return {} #{'type' : 'mdl'}

def trainAndTest(data, ratio=4/5):
    split = int(len(data) * ratio)
    train_data = data.iloc[:split]
    test_data = data.iloc[split:]
    test_labels = [ClassLabel.EDIBLE if x == 'e' else ClassLabel.POISONOUS for x in test_data["class"]]
    # tree = MDL.trainTree(train_data)
    # predicted = [tree.classify(row) for i, row in test_data.iterrows()]
    # print("Accuracy: ", metrics.accuracy_score(test_labels, predicted))
    labels = data["class"]
    data.drop("class", axis=1)
    print(cross_val_score(MDL(), data, labels, cv=10, scoring='accuracy'))

if __name__ == "__main__":
    data = pd.read_csv('data/mushrooms.csv')
    # print(data)
    # tree = buildTree(data)
    # tree = pruneTree(tree)
    trainAndTest(data)
    # one_entry = data.iloc[-1]
    # # print(one_entry)
    # print(tree.classify(one_entry))