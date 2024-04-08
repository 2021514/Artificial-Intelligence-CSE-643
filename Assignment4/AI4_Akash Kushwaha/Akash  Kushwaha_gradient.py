import numpy as np
X = np.arange(-20, 20, 0.1)
np.random.shuffle(X)
eps = np.random.rand(400)*10
y = 23*X + 43 + eps

W = 0
b = 0

learning_rate = 0.001
iterations = 100

for i in range(iterations):
    for i in range(len(X)):
        y_pred = W*X[i]+b
        
        grad_w = -2 * X[i] * (y[i] - y_pred)
        grad_b = -2 * (y[i] - y_pred)

        W-= learning_rate*grad_w
        b-= learning_rate*2*grad_b
print(W,b)