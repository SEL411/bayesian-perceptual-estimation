#!/usr/bin/env python
# coding: utf-8

# In[46]:


import numpy as np
import matplotlib.pyplot as plt


# In[48]:


N_STIM = 24
stim_angles = np.linspace(0, np.pi, N_STIM, endpoint=False)
N_Trials = 100 


# In[50]:


np.random.seed(0)


# In[52]:


Z = 2  


# In[54]:


def compute_C(Z):
    theta = np.linspace(0, np.pi, 2000)
    integrand = Z - np.abs(np.sin(2 * theta))
    integral = np.trapz(integrand, theta)
    C = 1.0 / integral
    return C

C = compute_C(Z)
print("Z =", Z)
print("C =", C)


# In[56]:


def f(theta):
    return C * (Z - np.abs(np.sin(2 * theta)))


# In[58]:


theta_check = np.linspace(0, np.pi, 2000)
lhs = np.trapz(f(theta_check), theta_check)
print(lhs)


# In[60]:


theta_grid = np.linspace(0, np.pi, 2000)
p_theta = f(theta_grid)   
print(np.trapz(p_theta, theta_grid))


# In[62]:


prior = p_theta
dtheta = theta_grid[1] - theta_grid[0]          
F_theta = np.cumsum(prior) * dtheta             
F_theta /= F_theta[-1]
print(F_theta[0], F_theta[-1])  


# In[64]:


m_grid = theta_grid.copy()
F_m = F_theta.copy()


# In[66]:


kappa = 5


# In[68]:


N = len(theta_grid)


# In[70]:


p_m_given_theta = np.zeros((N, N))

for j, th in enumerate(theta_grid):
    for i, m in enumerate(m_grid):
        diff = F_theta[j] - F_m[i]
        p_m_given_theta[i, j] = np.exp(kappa * np.cos(2 * np.pi * diff))

    p_m_given_theta[:, j] /= np.trapz(p_m_given_theta[:, j], m_grid)


# In[71]:


def find_index(theta_value):
    return np.argmin(np.abs(theta_grid - theta_value))


# In[72]:


print("stim_angles =", stim_angles)
print("len(stim_angles) =", len(stim_angles))

N_REPEATS = 100
bias_runs = []       
var_runs  = []  

def circ_diff(a, b):
    diff = a - b
    diff = (diff + np.pi/2) % np.pi - np.pi/2
    return diff


# In[73]:


for rep in range(N_REPEATS):

    all_estimates = []
    all_true = []
    all_theta_hats_per_stim = [] 

    for theta_true in stim_angles:
        estimates_for_this_stim = []

        j = find_index(theta_true)

        p_m = p_m_given_theta[:, j].copy()
        p_m = p_m / np.sum(p_m)

        print("p_m any negative?", np.any(p_m < 0))
        print("p_m any nan?", np.isnan(p_m).any())
        print("p_m min =", np.min(p_m))
        print("p_m max =", np.max(p_m))
        print("sum p_m =", np.sum(p_m))

        m_samples = np.random.choice(m_grid, size=N_Trials, p=p_m)
    
        for m in m_samples:                   
            i_m = find_index(m)                
            
            likelihood_theta = p_m_given_theta[i_m, :]

            prior_theta = prior

            posterior_unnorm = likelihood_theta * prior_theta
            posterior = posterior_unnorm / np.sum(posterior_unnorm)

            sin_mean_post = np.sum(np.sin(2 * theta_grid) * posterior)
            cos_mean_post = np.sum(np.cos(2 * theta_grid) * posterior)
            theta_hat = 0.5 * np.arctan2(sin_mean_post, cos_mean_post)

            estimates_for_this_stim.append(theta_hat)  
            all_estimates.append(theta_hat)            
            all_true.append(theta_true)    
    
        all_theta_hats_per_stim.append(estimates_for_this_stim)

    print("len(all_estimates) =", len(all_estimates))
    print("len(all_true) =", len(all_true))
    print("len(all_theta_hats_per_stim) =", len(all_theta_hats_per_stim))

    biases_trial = []
    for est, true in zip(all_estimates, all_true):
        d = circ_diff(est, true)
        biases_trial.append(d)

    biases_trial = np.array(biases_trial)
    all_true_arr = np.array(all_true)

    bias_means_per_stim = []
    for theta in stim_angles:
        mask = (all_true_arr == theta)
        d_stim = biases_trial[mask]

        sin_mean = np.mean(np.sin(2 * d_stim))
        cos_mean = np.mean(np.cos(2 * d_stim))
        bias = 0.5 * np.arctan2(sin_mean, cos_mean)  
        bias_means_per_stim.append(bias)

    bias_means_per_stim = np.array(bias_means_per_stim)

    variabilities = []

    for estimates_for_one_stim in all_theta_hats_per_stim:   
        est_array = np.array(estimates_for_one_stim)

        sin_mean = np.mean(np.sin(2 * est_array))
        cos_mean = np.mean(np.cos(2 * est_array))
        R = np.sqrt(sin_mean**2 + cos_mean**2)
        variability = 1 - R
        variabilities.append(variability)
    
    variabilities = np.array(variabilities)     
    
    bias_runs.append(bias_means_per_stim)
    var_runs.append(variabilities)


# In[74]:


bias_runs = np.array(bias_runs)
var_runs  = np.array(var_runs)

print("bias_runs shape =", bias_runs.shape)
print("var_runs shape =", var_runs.shape)


# In[75]:


stim_deg = stim_angles * 180 / np.pi

bias_mean = np.mean(bias_runs, axis=0)          
bias_sem  = np.std(bias_runs, axis=0, ddof=1) / np.sqrt(N_REPEATS)

bias_mean_deg = np.rad2deg(bias_mean)
bias_sem_deg  = np.rad2deg(bias_sem)

var_mean = np.mean(var_runs, axis=0)
var_sem  = np.std(var_runs, axis=0, ddof=1) / np.sqrt(N_REPEATS)


# In[76]:


plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.errorbar(stim_deg, bias_mean_deg, yerr=bias_sem_deg,
             fmt='o-', capsize=3)
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("Stimulus orientation (deg)")
plt.ylabel("Bias (deg)")
plt.title("Bias (θ̂ − θ_true) with CI")
plt.autoscale()

plt.subplot(1, 2, 2)
plt.errorbar(stim_deg, var_mean, yerr=var_sem,
             fmt='o-', capsize=3)
plt.xlabel("Stimulus orientation (deg)")
plt.ylabel("Variability (1 - R)")
plt.title("Variability with CI")
plt.autoscale()  

plt.tight_layout()
plt.show()

