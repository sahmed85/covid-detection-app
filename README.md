# Covid Detection App
A simple flask web app that takes in patient symptomps and information and stores in DB. It takes symptoms and determines if patient has covid.

## Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


## Weight Logic
The weighted logic in the COVID detection app assigns different weights to each symptom based on its severity and association with COVID-19. For example, more critical symptoms like "fever" or "difficulty breathing" are given higher weights (e.g., 4), while less severe symptoms like "headache" are assigned lower weights (e.g., 1). When a user submits their symptoms, the total score is calculated by summing the weights of the selected symptoms. Based on this total score, the app determines the likelihood of having COVID-19: higher scores indicate a higher likelihood, and lower scores suggest a lower risk. This approach provides a more nuanced and flexible assessment than a simple yes/no evaluation.

## Future Improvements
Use Machine Learning Model: Train a classification model (e.g., Logistic Regression, Decision Trees) using a dataset of symptoms and confirmed COVID-19 cases. Then use the model to predict the likelihood based on user inputs.