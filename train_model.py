from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import pickle

# Sample: Load your cleaned dataset
car = pd.read_csv("Cleaned_Car_data.csv")
X = car[['name', 'company', 'year', 'kms_driven', 'fuel_type']]
y = car['Price']

# Prepare transformers
ohe = OneHotEncoder()
ohe.fit(X[['name', 'company', 'fuel_type']])
column_trans = make_column_transformer(
    (OneHotEncoder(categories=ohe.categories_), ['name', 'company', 'fuel_type']),
    remainder='passthrough'
)

# Create pipeline
pipe = make_pipeline(column_trans, LinearRegression())

# Train the pipeline
pipe.fit(X, y)

# ✅ Save the model to .pkl
with open('linearRegression.pkl', 'wb') as f:
    pickle.dump(pipe, f)
