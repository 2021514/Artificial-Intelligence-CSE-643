import pandas as pd
import bnlearn as bn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest, f_classif

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

# Feature Selection
X = discretized_data.drop('Class', axis=1)
y = discretized_data['Class']

selector = SelectKBest(f_classif, k=2)
X_new = selector.fit_transform(X, y)
print(X_new)
# Get the names of the selected features
selected_features = X.columns[selector.get_support(indices=True)]

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2, random_state=42)

# Convert X_train and X_test back to DataFrame with proper column names
X_train_df = pd.DataFrame(X_train, columns=selected_features)
X_test_df = pd.DataFrame(X_test, columns=selected_features)

# Combine with 'Class' column for training
train_set = pd.concat([X_train_df, y_train.reset_index(drop=True)], axis=1)
print(train_set)
# Learn the structure and parameters
model = bn.structure_learning.fit(train_set, methodtype="hc")
model_A = bn.parameter_learning.fit(model, train_set)

# Perform predictions on the test set
test_set_for_prediction = X_test_df
y_pred = bn.predict(model_A, test_set_for_prediction, variables='Class')

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred['Class'])
print(f"Accuracy: {accuracy}")
print("Selected features:", selected_features.tolist())

