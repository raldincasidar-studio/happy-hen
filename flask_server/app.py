from flask import Flask, jsonify, request, send_file
import sqlite3
import os
import datetime
import random
import string
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from dateutil.relativedelta import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/hello-world", methods=["GET"])
def hello_world():
    
    return jsonify({"message": "Hello World"})



# secret key for jwt
SECRET_KEY = "secretkey"

# database path
DATABASE = "./database.db"


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401


    
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    cursor.execute("UPDATE users SET token=? WHERE id=?", (token, user[0]))
    conn.commit()

    payload = {
        "user_id": user[0],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    cursor.execute("SELECT * FROM users WHERE id=?", (user[0],))
    user = cursor.fetchone()
    return jsonify({"token": token, "user": user}), 200


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE token=?", (request.headers.get("Authorization"),))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    if not file:
        return jsonify({"error": "Missing file"}), 400
    file.save(os.path.join("uploads", file.filename))
    return jsonify({"message": "File uploaded"}), 200

@app.route("/get-files", methods=["GET"])
def get_files():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE token=?", (request.headers.get("Authorization"),))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    
    uploads_folder = './uploads'

    try:
        files = os.listdir(uploads_folder)
        return jsonify({"files": files})
    except FileNotFoundError:
        return jsonify({"error": "The 'uploads' folder does not exist."}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route("/delete-file", methods=["POST"])
def delete_file():
    filename = request.json.get("filename", None)
    if not filename:
        return jsonify({"error": "Missing filename"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE token=?", (request.headers.get("Authorization"),))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    
    uploads_folder = './uploads'
    file_path = os.path.join(uploads_folder, filename)

    try:
        if not os.path.exists(file_path):
            return jsonify({"error": f"The file '{filename}' does not exist."}), 404
        os.remove(file_path)
        return jsonify({"message": f"The file '{filename}' has been deleted."})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


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
    plt.ioff()
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
    plt.savefig(random_filename, bbox_inches='tight')
    plt.close()

    # Calculate accuracy percentage
    accuracy = (np.round(y_pred) == np.round(y_test)).mean() * 100

    # Return the results as JSON
    return jsonify({
        "mse": mse,
        "r2": r2,
        "plot_url": random_filename,
        "filename": filename_generated,
        "mse": mse,
        "r2": r2,
        # "accuracy": accuracy,
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




@app.route("/generate-prediction", methods=["POST"])
def generate_prediction():
    months_advance = int(request.json.get("months", 1))

    print(months_advance);

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

    # Generate prediction month advance from current date
    current_date = datetime.date.today()
    future_date = current_date
    y_pred = []
    for _ in range(months_advance):
        future_date = future_date + relativedelta(months=+1)
        future_month = future_date.month
        future_year = future_date.year

        # Prepare data for prediction
        X_pred = pd.DataFrame([[future_month, future_year]], columns=['Month', 'Year'])

        # Initialize and train the Random Forest model
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X, y)

        # Make predictions on the test set
        y_pred.append(rf_model.predict(X_pred)[0])

    # Plot actual vs predicted values
    plt.ioff()
    plt.figure(figsize=(10, 6))
    plt.plot(y.values, label='Actual Egg Production', marker='o')
    plt.plot(list(range(len(y), len(y) + months_advance)), y_pred, label='Predicted Egg Production', marker='x')
    plt.title('Actual vs Predicted Egg Production')
    plt.xlabel('Test Set Index')
    plt.ylabel('Egg Production')
    plt.legend()
    plt.grid(True)

    # Save the plot with a random filename
    os.makedirs('ai_results', exist_ok=True)
    filename_generated = f"result_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}.png"
    random_filename = f"ai_results/{filename_generated}"
    plt.savefig(random_filename, bbox_inches='tight')
    plt.close()

    # Return the results as JSON
    return jsonify({
        "mse": None,
        "r2": None,
        "plot_url": random_filename,
        "filename": filename_generated,
        "months_advance": months_advance,
        "predictions": y_pred
    })


if __name__ == "__main__":
    app.run(debug=True)
