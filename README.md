# Bayesian Perceptual Estimation (Efficient Observer Model)

This project implements an **efficient Bayesian observer model** to explain 
orientation-dependent perceptual bias and variability in human vision.

---

## 🎯 Problem

Human observers show systematic distortions when estimating orientation:

- **Repulsive bias**: estimates are biased *away* from cardinal orientations (0°, 90°)
- **Oblique effect**: variability is higher at oblique orientations

These phenomena are well-documented in behavioral experiments  
(e.g., Appelle, 1972; Wei & Stocker, 2015).

📄 Assignment based on: Bayesian observer modeling task (orientation estimation)

---

## 🧠 Key Idea: Efficient Bayesian Observer

Standard Bayesian models predict **attractive bias toward the prior**.

However, real data shows the opposite (**repulsive bias**).

This model explains it using:

> **Efficient coding → non-uniform Fisher information → asymmetric likelihood**

- Natural environments contain more **cardinal orientations**
- The brain allocates more encoding precision to frequent stimuli
- This creates **stimulus-dependent Fisher information**
- Result: likelihood becomes **asymmetric**
- → posterior shifts **away from prior** (repulsive bias)

This follows the framework of Wei & Stocker (2015)

---
## 🔍 My Contribution & Understanding

This project is not a direct implementation of a standard Bayesian model.

I specifically focused on understanding and reproducing the **anti-Bayesian percept**
reported in Wei & Stocker (2015).

Key points I implemented and verified:

- Constructed a **non-uniform prior** reflecting natural orientation statistics
- Implemented **stimulus-dependent encoding** using cumulative mapping F(θ)
- Verified that **non-uniform Fisher information leads to asymmetric likelihood**
- Confirmed that this asymmetry produces **repulsive bias**, not attractive bias

Through this project, I understood that:

> Perceptual bias is not determined only by the prior,  
> but by how the stimulus is encoded before Bayesian decoding.

This connects efficient coding with Bayesian inference.

---

## 📐 Model

### Likelihood

$$
p(m|\theta) = \mathcal{N}(m; \theta, \sigma^2)
$$

---

### Prior

$$
p(\theta)
$$

(encodes higher probability near cardinal orientations)

---

### Posterior

$$
p(\theta|m) \propto p(m|\theta) p(\theta)
$$

---

### Estimation

$$
\hat{\theta} = \mathbb{E}[\theta | m]
$$

---

## 📊 Fisher Information

\[
J(\theta) = \int \left( \frac{\partial}{\partial \theta} \log p(m|\theta) \right)^2 p(m|\theta)\,dm
\]
- In this model, Fisher information is **non-uniform**
- Higher near cardinal orientations
- Drives asymmetric likelihood

---

## 🛠 Methods

- Circular statistics (orientation space: [0, π])
- Von Mises–like likelihood in sensory space
- Bayesian decoding via circular mean
- Simulation with repeated sampling

---

## 🔬 Simulation

- 24 orientations (7.5° spacing)
- 100 trials per stimulus
- 100 repetitions for stability

Bias and variability computed as:

- Bias: circular mean error
- Variability: \(1 - R\) (resultant vector length) :contentReference[oaicite:3]{index=3}

---

## 📈 Results

We examined how perceptual bias and variability change as a function of the concentration parameter (κ).

As κ increases, prior concentration strengthens, leading to increased bias and reduced variability.

---

### κ = 4 (relatively weak prior)

![kappa_4](images/kappa_4.png)

Bias is relatively weak, and variability remains high.

---

### κ = 8 (moderate prior)

![kappa_8](images/kappa_8.png)

Bias begins to emerge near cardinal orientations, while variability starts to decrease.

---

### κ = 12 (strong prior)

![kappa_12](images/kappa_12.png)

Repulsive bias becomes more pronounced, and variability is further reduced.

---

### κ = 20 (very strong prior)

![kappa_20](images/kappa_20.png)

Strong prior influence leads to clear repulsive bias and low variability.

---

*Figure: Bias and variability as a function of stimulus orientation for different values of κ.*

---

### Key Findings

- Repulsive bias emerges with stronger prior
- Oblique effect reproduced (higher variance at oblique angles)
- Model qualitatively matches behavioral data

---
## ⚠️ Limitation

- This model reproduces qualitative patterns only
- No parameter fitting to real datasets
- Further work: model fitting and neural validation
---

## 💻 Implementation

Main components:

- Prior construction (non-uniform)
- Sensory encoding via cumulative mapping \(F(\theta)\)
- Sampling measurements \(m\)
- Bayesian decoding using circular statistics

Example:

```python
theta_hat = 0.5 * np.arctan2(
    np.sum(np.sin(2 * theta_grid) * posterior),
    np.sum(np.cos(2 * theta_grid) * posterior)
)
