from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the path to your trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'breast_cancer_model.pth')

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create the 'uploads' directory if it doesn't exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your breast cancer prediction model (replace this with your actual loading code)
def load_model():
    # Implement your model loading code here
    pass

# Perform breast cancer prediction using the loaded model
def predict_breast_cancer(image_path):
    # Implement your prediction code here
    # This may involve loading the image, pre-processing, and using the model
    pass

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is provided
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'})

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        # Check if the file has an allowed extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file extension'})

        # Save the file to the server
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Perform breast cancer prediction
        model = load_model()
        prediction_result = predict_breast_cancer(file_path)

        # Render the result on the web page
        return render_template('index.html', result=prediction_result, image_path=file_path)

    return render_template('index.html', result=None, image_path=None)

if __name__ == '__main__':
    app.run(debug=True , port=4345)
