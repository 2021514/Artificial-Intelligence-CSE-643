import pandas as pd
import bnlearn as bn

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
    discretized_data[col] = pd.qcut(data[col], 3, labels=False, duplicates='drop')

# Learn the structure
model_structure = bn.structure_learning.fit(discretized_data, methodtype="hc")
model_A = bn.parameter_learning.fit(model_structure, discretized_data)
print(discretized_data['Alcohol'].unique())

# Case 1
query_variable_1 = 'Class'
evidence_1 = {'Alcohol': 0, 'Malic_Acid': 2}
posterior_probabilities_case1 = bn.inference.fit(model_A, variables=[query_variable_1], evidence=evidence_1, verbose=0)

# Case 2
query_variable_2 = 'Color_intensity'
evidence_2 = {'Flavanoids': 0, 'Hue': 2}
posterior_probabilities_case2 = bn.inference.fit(model_A, variables=[query_variable_2], evidence=evidence_2, verbose=0)

# Case 3
query_variable_3 = 'Proline'
evidence_3 = {'Alcohol': 2, 'Total_phenols': 0}
posterior_probabilities_case3 = bn.inference.fit(model_A, variables=[query_variable_3], evidence=evidence_3, verbose=0)

# Case 4
query_variable_4 = 'Magnesium'
evidence_4 = {'Ash': 2, 'Hue': 1}
posterior_probabilities_case4 = bn.inference.fit(model_A, variables=[query_variable_4], evidence=evidence_4, verbose=0)

print(f"Posterior probabilities for {query_variable_1} given evidence: {posterior_probabilities_case1}")
print(f"Posterior probabilities for {query_variable_2} given evidence: {posterior_probabilities_case2}")
print(f"Posterior probabilities for {query_variable_3} given evidence: {posterior_probabilities_case3}")
print(f"Posterior probabilities for {query_variable_4} given evidence: {posterior_probabilities_case4}")
