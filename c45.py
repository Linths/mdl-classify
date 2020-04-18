import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

FEATURE_COLS = ["cap-shape","cap-surface","cap-color","bruises","odor","gill-attachment","gill-spacing","gill-size","gill-color","stalk-shape","stalk-root","stalk-surface-above-ring","stalk-surface-below-ring","stalk-color-above-ring","stalk-color-below-ring","veil-type","veil-color","ring-number","ring-type","spore-print-color","population","habitat"]

def applyC45(data, ratio=4/5):
    split = int(len(data) * ratio)

    labels = data["class"]
    train_labels = labels.iloc[:split]
    test_labels = labels.iloc[split:]

    data = data.drop("class", axis=1)
    data = pd.get_dummies(data, FEATURE_COLS)
    train_data = data.iloc[:split]
    test_data = data.iloc[split:]

    # print(train_data.shape)
    print(train_data.head())

    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(train_data, train_labels)
    predicted = clf.predict(test_data)
    print("Accuracy: ", metrics.accuracy_score(test_labels, predicted))

    print(cross_val_score(clf, data, labels, cv=10))


if __name__ == "__main__":
    data = pd.read_csv('data/mushrooms.csv')
    applyC45(data)