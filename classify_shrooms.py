from mdl_tree import *
from c45 import *
import pandas as pd

class MDL:
    def __init__(self):
        super().__init__()

    def buildTree(self, data):
        NO_FEAT = 6
        tree = Leaf(attrs_left=ALL_ATTRIBUTES[:NO_FEAT], data=data, depth=0)
        while (True):
            leaves = tree.getAllLeaves()
            # Disregard leaves that are pure, empty, or from a depth where no attributes are left
            leaves = [leaf for leaf in leaves if leaf.no_all != 0 and (not leaf.isPure()) and leaf.attrs_left != []]
            if leaves == []:
                break
            for leaf in leaves:
                d = leaf.depth
                if leaf.attrs_left == []:
                    continue
                if not leaf.isPure():
                    not_all_pure = True
                    lowest_cost = None
                    best_node = None
                    attrs_left = leaf.attrs_left
                    for attr in attrs_left:
                        node = DecisionNode(attr, attrs_left=attrs_left, data=data, depth=d)
                        cost = node.getTotalCost()
                        if lowest_cost == None or cost < lowest_cost:
                            lowest_cost = cost
                            best_node = node
                    # available_attributes.remove(best_node.attribute)
                    if isinstance(tree, Leaf):
                        tree = best_node
                    else:
                        tree.switchLeaf(leaf, best_node)
                    # print(tree)
                    # print()
        # print(f"End with tree: {tree}")
        # print(f"End with leaves: {tree.getAllLeaves()}")
        # print([leaf.isPure() for leaf in tree.getAllLeaves()])
        # print([leaf.no_exceptions for leaf in tree.getAllLeaves()])
        # print(tree.getNoData())
        # print(tree.getNoExceptions())
        print(f"Tree returned: {tree}")
        print(f"After building\t{tree.getErrorRate()}")
        return tree

    def pruneTree(self, tree):
        checked = []
        done = False

        while (not done):
            done = True
            if isinstance(tree, Leaf):
                print("The whole tree got pruned!")
                break
            parents = tree.getAllLeafParents()
            for parent in parents:
                if parent in checked:
                    break
                checked.append(parent)
                done = False
                current_cost = parent.getTotalCost()
                leaf = Leaf(data=parent.data, attrs_left=parent.attrs_left)
                alt_cost = leaf.getTotalCost()

                if alt_cost < current_cost:
                    # print(f"{current_cost} = {parent.getTotalCost()} + {leaf.getExceptionsCost()}")
                    # print(f"{alt_cost} = {leaf.getTotalCost()} + {leaf.getExceptionsCost()}")
                    tree.removeNode(parent)

                # current_cost = tree.getTotalCost()
                # # current_string = f"{tree}\n{current_cost} = {tree.getDescribeCost()} + {tree.getExceptionsCost()}"
                # # current_string_costs = f"{current_cost}\t= {tree.getDescribeCost()}\t+ {tree.getExceptionsCost()}"
                # tree, leaf = tree.removeNode(parent)
                # alt_cost = tree.getTotalCost()
                # # alt_string = f"{tree}\n{alt_cost} = {tree.getDescribeCost()} + {tree.getExceptionsCost()}"
                # # alt_string_costs = f"{alt_cost}\t= {tree.getDescribeCost()}\t+ {tree.getExceptionsCost()}"
                # if leaf == None:
                #     print(f"Oops! {parent.attribute}")
                # # print(parent.attribute.name)
                # # print(current_string_costs)
                # # print(alt_string_costs)
                # # print(f"Try switch {parent.attribute.name} @{parent.depth}")
                # if alt_cost >= current_cost:
                #     # Update is not better
                #     # print(current_string_costs)
                #     # print(alt_string_costs)
                #     tree.switchLeaf(leaf, parent)
                # else:
                    # print(current_string_costs)
                    # print(alt_string_costs)
                    # print(f"Now:\t{tree}")
        print(tree)
        print(f"After pruning\t{tree.getErrorRate()}")
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
    NO_ROWS = data.shape[0] #5000
    data = data.iloc[:NO_ROWS]
    print(data)
    split = int(len(data) * ratio)
    train_data = data.iloc[:split]
    test_data = data.iloc[split:]
    test_labels = [ClassLabel.EDIBLE if x == 'e' else ClassLabel.POISONOUS for x in test_data["class"]]
    tree = MDL().trainTree(train_data)
    predicted = [tree.classify(row) for i, row in test_data.iterrows()]
    print("Accuracy: ", metrics.accuracy_score(test_labels, predicted))
    labels = data["class"]
    data.drop("class", axis=1)
    # k-fold CV
    accs = cross_val_score(MDL(), data, labels, cv=10, scoring='accuracy')
    print(accs)
    print(np.average(accs))

if __name__ == "__main__":
    data = pd.read_csv('data/mushrooms.csv')
    # print(data)
    # tree = buildTree(data)
    # tree = pruneTree(tree)
    trainAndTest(data)
    # one_entry = data.iloc[-1]
    # # print(one_entry)
    # print(tree.classify(one_entry))