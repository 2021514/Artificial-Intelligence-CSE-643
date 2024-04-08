import bnlearn as bn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Assuming 'model_A' is your Bayesian network model after training
# Assuming 'X_test' is your dataset with the selected features for testing

# Create a DataFrame for testing
C_test = pd.concat([X_test, y_test], axis=1)

# Define the queries for different combinations of evidence values
queries = []
for F1_value in [0, 1, 2]:
    for F2_value in [0, 1, 2]:
        query = bn.inference.fit(model_A, variables=['target'], evidence={'0D280_0D315_of_diluted_wines': F1_value, 'Proline': F2_value})
        queries.append(query.values)

# Reshape the results into a 3D array
Z = np.array(queries).reshape(3, 3, -1)

# Create a meshgrid for plotting
F1, F2 = np.meshgrid([0, 1, 2], [0, 1, 2])

# Plot 3D probability distribution
for i in range(Z.shape[2]):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(F1, F2, Z[:, :, i], cmap='viridis', alpha=0.8)

    if i == 0: 
        plt.title(f"P(target = 0 | 0D280_0D315_of_diluted_wines , Proline)")
    elif i == 1: 
        plt.title(f"P(target = 1 | 0D280_0D315_of_diluted_wines , Proline)")
    elif i == 2: 
        plt.title(f"P(target = 2 | 0D280_0D315_of_diluted_wines , Proline)")

    ax.set_xlabel('0D280_0D315_of_diluted_wines (F1)')
    ax.set_ylabel('Proline (F2)')
    ax.set_zlabel('Probability')
    plt.show()
