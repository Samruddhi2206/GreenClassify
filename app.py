import os
import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Load the trained model
def load_trained_model():
    model_path = os.path.join("model", "final_model.h5")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return load_model(model_path)

# Load class labels
def load_class_names():
    data_dir = os.path.join("data", "vegetables")
    return sorted([
        folder for folder in os.listdir(data_dir)
        if os.path.isdir(os.path.join(data_dir, folder))
    ])

# Preprocess the image
def preprocess_image(img: Image.Image, target_size=(128, 128)):
    img = img.resize(target_size)
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# Load model and classes once
model = load_trained_model()
class_names = load_class_names()

# Routes for each page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict-page')
def predict_page():
    return render_template('prediction.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Image prediction endpoint (called by JavaScript)
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        img = Image.open(file.stream).convert('RGB')
        input_arr = preprocess_image(img)
        predictions = model.predict(input_arr)[0]

        class_id = int(np.argmax(predictions))
        confidence = float(predictions[class_id])
        predicted_class = class_names[class_id].title()

        if confidence < 0.5:
            predicted_class = "Not Detected"
            confidence = 0.0

        # Convert image to base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence,
            'image': img_str
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
