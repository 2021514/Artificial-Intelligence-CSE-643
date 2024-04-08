import pandas as pd
import bnlearn as bn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load your data
data = pd.read_csv('wine.csv')

# Define column names
column_names = ['Class', 'Alcohol', 'Malic_Acid', 'Ash', 'Alcalinity_of_Ash', 
                'Magnesium', 'Total_phenols', 'Flavanoids', 'Nonflavanoid_phenols', 
                'Proanthocyanins', 'Color_intensity', 'Hue', 'OD280_OD315', 'Proline']
data.columns = column_names

# Discretize the data if needed
discretized_data = data.copy()
for col in data.columns[1:]:
    discretized_data[col] = pd.qcut(data[col], 4, labels=False, duplicates='drop')
# Split the data into features (X) and target variable (y)
X = discretized_data.drop('Class', axis=1)
y = discretized_data['Class']

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
train_set = pd.concat([X_train,y_train],axis=1)
test_set = pd.concat([X_test,y_test],axis=1)
# Define hyperparameter values to search
structure_methods = ['tan', 'hc'] 
parameter_methods = ['bayes','ml'] 
best_accuracy = 0.0
best_params = {}
s = []
# Grid Search
for structure_method in structure_methods:
    for parameter_method in parameter_methods:
        if structure_method=="tan":
            model_structure = bn.structure_learning.fit(train_set, methodtype=structure_method, scoretype='bic', root_node="Alcohol", class_node="Class")
            model_parameters = bn.parameter_learning.fit(model_structure, train_set, methodtype=parameter_method)
            y_pred = bn.predict(model_parameters, X_test, variables='Class')
            accuracy = accuracy_score(y_test, y_pred['Class'])
        else:
            model_structure = bn.structure_learning.fit(train_set, methodtype=structure_method, scoretype='bic')
            new_test = X_test.drop('Ash',axis=1)
            model_parameters = bn.parameter_learning.fit(model_structure, train_set, methodtype=parameter_method)
            y_pred = bn.predict(model_parameters, new_test, variables='Class')
            accuracy = accuracy_score(y_test, y_pred['Class'])

        s.append(accuracy)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_params = {
                'structure_method': structure_method,
                'parameter_method': parameter_method,
            }
print(s)
print(f"Best Accuracy: {best_accuracy}")
print("Best Parameters:", best_params)
