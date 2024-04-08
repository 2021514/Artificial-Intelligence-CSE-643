import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import patsy

# Data Preprocessing using deviation coding
def preprocess_data(df):
    coded_sex = patsy.dmatrix('C(Sex, Treatment(reference="M"))', df, return_type='dataframe')
    
    # Drop the original 'Sex' column and concatenate the coded_sex dataframe
    df = df.drop('Sex', axis=1)
    df = pd.concat([df, coded_sex], axis=1)

    return df
column_names = ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight', 'Rings']
df = pd.read_csv("abalone.csv", header=None, names=column_names)

# Preprocess Data
df = preprocess_data(df)
print(df.head())
X = df.drop('Rings', axis=1)
y = df['Rings']

# Polynomial Transformation and Linear Regression
def create_poly_model(degree):
    polynomial_features = PolynomialFeatures(degree=degree, include_bias=False)
    linear_regression = LinearRegression()
    pipeline = Pipeline([("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
    return pipeline

# Cross Validation
r2_scores = []
for _ in range(20):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=np.random.randint(1000))
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=np.random.randint(1000))
    
    model = create_poly_model(degree=2)
    model.fit(X_train, y_train)
    y_pred_val = model.predict(X_val)
    r2_val = r2_score(y_val, y_pred_val)
    
    if r2_val > 0.56:
        y_pred_test = model.predict(X_test)
        r2_test = r2_score(y_test, y_pred_test)
        r2_scores.append(r2_test)

# Calculate mean and standard deviation
mean_r2 = np.mean(r2_scores)
std_r2 = np.std(r2_scores)

# Full dataset R2 score
model_full = create_poly_model(degree=2)
model_full.fit(X, y)
y_pred_full = model_full.predict(X)
r2_full = r2_score(y, y_pred_full)

# Output
print(f"Full dataset train and eval R2 score: {r2_full:.2f}")
print(f"70-15-15 Cross validation boxplot: mean={mean_r2:.2f}, std={std_r2:.2f}")

# Optional: Box-plot Visualization
plt.boxplot(r2_scores)
plt.title("Boxplot of R2 Scores over 15% Test Dataset")
plt.ylabel("R2 Score")
plt.show()
