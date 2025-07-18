from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('linearRegression.pkl', 'rb'))

# Load dataset
df = pd.read_csv(r"C:\Users\lakha\Desktop\FLASK\ml model\Cleaned_Car_data.csv")


# Precompute groupings for dropdowns
companies = sorted(df['company'].unique())

# Mapping from company → models available
company_to_models = {
    comp: sorted(df[df['company'] == comp]['name'].unique().tolist())
    for comp in companies
}

# Mapping from (company, model) → fuel types available
company_model_fuel = {}
for _, row in df.iterrows():
    key = (row['company'], row['name'])
    company_model_fuel.setdefault(key, set()).add(row['fuel_type'])
company_model_fuel = {k: sorted(v) for k, v in company_model_fuel.items()}

# For years, kms won't vary much; skip filtering for simplicity.

@app.route('/')
def home():
    return render_template('index.html', companies=companies)

# AJAX endpoint to fetch models for selected company
@app.route('/get_models')
def get_models():
    comp = request.args.get('company')
    models = company_to_models.get(comp, [])
    return jsonify(models)

# AJAX endpoint to fetch fuel types for company+model
@app.route('/get_fuels')
def get_fuels():
    comp = request.args.get('company')
    model = request.args.get('model')
    fuels = company_model_fuel.get((comp, model), [])
    return jsonify(fuels)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    name = data['name']
    company = data['company']
    year = int(data['year'])
    kms_driven = int(data['kms_driven'])
    fuel_type = data['fuel_type']

    input_df = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
                            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
    pred = round(model.predict(input_df)[0], 2)
    return render_template('index.html', companies=companies,
                           prediction=pred)

if __name__ == "__main__":
    app.run(debug=True)
