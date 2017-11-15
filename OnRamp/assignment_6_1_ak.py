# -*- coding: utf-8 -*-
"""
Determine 4 clusters for OldFaithful glacier eruption data using GMM-EM algorithm

Reference for GMM-EM: 
http://mccormickml.com/2014/08/04/gaussian-mixture-models-tutorial-and-matlab-code/
https://gist.github.com/bistaumanga/6023716
    
@author: Aruna Kumaraswamy
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def log_multivariate(X,mu,covars):
    delta = X-mu
    part1 = np.linalg.det(covars) ** -.5 ** (2 * np.pi) ** (-X.shape[1]/2.)
    part2 = np.dot(np.linalg.inv(covars) , (delta).T).T 
    prob = part1 * np.exp(-.5 * np.einsum('ij, ij -> i',delta,part2))
    
    return prob


# Read Input File
relativePath = os.getcwd()
file_path = relativePath + '/resources/oldFaithful.csv'
df = pd.read_csv(file_path)

X = df.values

num_cluster = 4
num_samples, num_features = X.shape
print 'Shape ',num_samples, num_features

mu = X[np.random.choice(num_samples, num_cluster, False), :]
covars = [np.eye(num_features)] * num_cluster

wt = [0.25, 0.25, 0.25, 0.25]
resp_matrix = np.zeros((num_samples,num_cluster))

current_ll = 0
prev_ll = 0
lr = 0.0001
iter = 0

while  (np.abs(current_ll - prev_ll) < lr):
    iter = iter +1
    # Expectation: Calculate the responsibility matrix and loglikelihood from it
    for k in range(num_cluster):
        resp_matrix[:, k] = wt[k] * log_multivariate(X,mu[k],covars[k])
 
    
    current_ll = np.sum(np.log(np.sum(resp_matrix, axis = 1)))
    
    #Normalized the responsibilty matrix
    resp_matrix = (resp_matrix.T / np.sum(resp_matrix, axis = 1)).T
    num_gauss_points = np.sum(resp_matrix, axis = 0)
    
    
    #Maximization step
    for k in range(num_cluster):
                
                ## calculate mean with adjusted resp matrix
                mu[k] = 1. / num_gauss_points[k] * np.sum(resp_matrix[:, k] * X.T, axis = 1).T
                x_mu = np.matrix(X - mu[k])
                
                ## Recalculate the covariance matrix
                covars[k] = np.array(1 / num_gauss_points[k] * np.dot(np.multiply(x_mu.T,  resp_matrix[:, k]), x_mu))
                
                ## Weights
                wt[k] = 1. / num_samples * num_gauss_points[k]
    if (prev_ll == current_ll):
        print 'Algorithm stopped because of no change to loglikelihood'
        break
    prev_ll = current_ll

print 'EM model has converged, mu, covars, wt ready to be used for prediction'
print 'Convergence at iteration: ',iter

#Prediction - Use the parameters to predict the label
for mu, s, w in zip(mu, covars, wt):
    probs = np.array([w * log_multivariate(X,mu, s)])
    
y = probs

#Display the clusters
fig = plt.figure()
plt.scatter(df['eruptions'], df['waiting'], 24, c=y)
plt.show()