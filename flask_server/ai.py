from flask import jsonify, Flask, request, send_file
from flask_cors import CORS
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import random
import string


app = Flask(__name__)
CORS(app)

@app.route("/prediction", methods=["GET"])
def get_prediction():
    # Load the uploaded file into a DataFrame
    file_name = os.listdir('uploads')[0]  # Get the name of the uploaded file
    df = pd.read_excel(os.path.join('uploads', file_name), engine='openpyxl')

    # Data preprocessing
    print(df.head())  # Check the actual data
    df.columns = ['Date', 'Egg Production']
    df['Date'] = pd.to_datetime(df['Date'], format='%b-%y')
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df = df.drop(columns=['Date'])

    # Split data into features (X) and target (y)
    X = df[['Month', 'Year']]
    y = df['Egg Production']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = rf_model.predict(X_test)

    # Evaluate the model performance
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Plot actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.values, label='Actual Egg Production', marker='o')
    plt.plot(y_pred, label='Predicted Egg Production', marker='x')
    plt.title('Actual vs Predicted Egg Production')
    plt.xlabel('Test Set Index')
    plt.ylabel('Egg Production')
    plt.legend()
    plt.grid(True)

    # Save the plot with a random filename
    os.makedirs('ai_results', exist_ok=True)
    filename_generated = f"result_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}.png"
    random_filename = f"ai_results/{filename_generated}"
    plt.savefig(random_filename)
    plt.close()

    # Calculate accuracy percentage
    accuracy = (np.round(y_pred) == np.round(y_test)).mean() * 100

    # Return the results as JSON
    return jsonify({
        "mse": mse,
        "r2": r2,
        "accuracy": accuracy,
        "plot_url": random_filename,
        "filename": filename_generated,
        "mse": mse,
        "r2": r2,
        "accuracy": accuracy,
        "actual": y_test.values.tolist(),
        "predicted": y_pred.tolist()
    })

@app.route("/get-images/<filename>", methods=["GET"])
def get_images(filename):
    try:
        images_folder = './ai_results'
        image_files = [f for f in os.listdir(images_folder) if f.endswith('.png')]
        if filename in image_files:
            return send_file(os.path.join(images_folder, filename), mimetype='image/png')
        else:
            return jsonify({"error": "The file does not exist."}), 404
    except FileNotFoundError:
        return jsonify({"error": "The 'ai_results' folder does not exist."}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
