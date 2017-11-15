"""
@author Aruna Kumaraswamy
Assignment 6: sklearn PCA for iris data set
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import os
import matplotlib.pyplot as plt

relativePath = os.getcwd()
dataFilePath = relativePath + "/Resources/iris.csv"
iris_df = pd.read_csv(dataFilePath)
iris_values = iris_df.values
pca = PCA(n_components=2)
pca.fit(iris_values)

plt.figure(figsize=(8, 6), dpi=80)
ax = plt.subplot(1, 1, 1)
colors1 = np.random.rand(4)
colors2 = np.random.rand(4)
Z = pca.transform(iris_values)
print Z
plt.scatter(Z[:, 0], Z[:, 1], c=['g','b'], s=25,
            alpha=.6)
ax.set_title('Iris PCA')
ax.grid(True)
plt.show()

