import pandas as pd
import bnlearn as bn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the data
data = pd.read_csv('wine.csv')

# Define column names
column_names = ['Class', 'Alcohol', 'Malic_Acid', 'Ash', 'Alcalinity_of_Ash', 
                'Magnesium', 'Total_phenols', 'Flavanoids', 'Nonflavanoid_phenols', 
                'Proanthocyanins', 'Color_intensity', 'Hue', 'OD280_OD315', 'Proline']
data.columns = column_names

# Discretize the data
discretized_data = data.copy()
for col in data.columns[1:]:
    discretized_data[col] = pd.qcut(data[col], 4, labels=False, duplicates='drop')

# Learn the structure
X = discretized_data.drop('Class', axis=1)
y = discretized_data['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_set = pd.concat([X_train,y_train],axis=1)
test_set = pd.concat([X_test,y_test],axis=1)

model = bn.structure_learning.fit(train_set, methodtype="hc")
model_A = bn.parameter_learning.fit(model, train_set)

# Split the dataset into training and test sets
newtest = X_test.drop('Ash',axis=1)

# Perform predictions on the test set
y_pred = bn.predict(model_A, newtest, variables='Class')

# Print the predicted values
# print(y_pred['Class'])
# print(y_test)
# # Calculate accuracy
# for i in y_pred:
#     print(i)
accuracy = accuracy_score(y_test, y_pred['Class'])
print(f"Accuracy: {accuracy}")
