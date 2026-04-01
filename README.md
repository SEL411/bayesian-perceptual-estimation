# Bayesian Perceptual Estimation

This project implements a Bayesian observer model for perceptual estimation, developed during a research internship focused on computational modeling.

## Objective

- Investigate orientation-specific perceptual bias and variability  
- Reproduce key behavioral phenomena:
  - Repulsive bias (away from cardinal orientations)
  - Oblique effect (increased variability at oblique orientations)

## Methods

- Bayesian inference with prior and likelihood distributions  
- Circular statistics for modeling orientation space  
- Simulation of perceptual estimation under noise  

## Simulation

- 24 evenly spaced orientation stimuli (7.5° intervals)  
- Repeated sampling for each stimulus  
- Bias and variability curves computed across orientations  
- Multiple simulations performed to examine stability  

## Results

- Repulsive bias observed near cardinal orientations  
- Increased variability at oblique orientations  
- Model successfully captures key perceptual patterns  

## Notes

- Inspired by Wei & Stocker (2015)  
- Implemented in Python using numpy and matplotlib  
