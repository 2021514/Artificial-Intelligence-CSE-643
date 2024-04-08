import pandas as pd
import bnlearn as bn
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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


# model = bn.structure_learning.fit(discretized_data, methodtype='hc')

DAG = bn.structure_learning.fit(discretized_data, methodtype='hc')

# Then, learn the parameters (CPDs) of the Bayesian network
model = bn.parameter_learning.fit(DAG, discretized_data)

# Now you can access the CPDs from the 'model'
cpds = model['model'].cpds
for cpd in cpds:
    print(cpd)
    variable = cpd.variable
    cpd_table = cpd.values
    if cpd_table.ndim == 2:  # We can only plot 2D distributions easily
        plt.figure(figsize=(10, 6))
        ax = sns.heatmap(cpd_table, annot=True, fmt='.2f')
        ax.set_title(f"CPD of {variable}")
        ax.set_ylabel('States of ' + variable)
        ax.set_xlabel('States of Parent(s)')
        plt.show()