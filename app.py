from flask import Flask, request, jsonify, send_from_directory, url_for, render_template
from flask_cors import CORS
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="redhat",
    database="image_sharing"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify(success=False, message="No file part")
    file = request.files['image']
    if file.filename == '':
        return jsonify(success=False, message="No selected file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('uploaded_file', filename=filename)
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO images (image_url) VALUES (%s)", (file_url,))
        db.commit()
        
        return jsonify(success=True, message="File uploaded successfully")
    return jsonify(success=False, message="File type not allowed")

@app.route('/images', methods=['GET'])
def get_images():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()
    return jsonify(images=images)

@app.route('/like/<int:image_id>', methods=['POST'])
def like_image(image_id):
    cursor = db.cursor()
    cursor.execute("UPDATE images SET likes = likes + 1 WHERE id = %s", (image_id,))
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify(success=False, message="Image not found")
    return jsonify(success=True, message="Image liked successfully")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
