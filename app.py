from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for, render_template
from flask_cors import CORS
import mysql.connector
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'  # Replace with a real secret key in production

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
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify(success=False, message="Username already exists")
    
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()
    
    return jsonify(success=True, message="User registered successfully")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return jsonify(success=True, message="Login successful")
    else:
        return jsonify(success=False, message="Invalid username or password")

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify(success=True, message="Logout successful")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in")
    
    if 'image' not in request.files:
        return jsonify(success=False, message="No file part")
    file = request.files['image']
    if file.filename == '':
        return jsonify(success=False, message="No selected file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO images (image_url) VALUES (%s)", (file_url,))
        db.commit()
        
        return jsonify(success=True, message="File uploaded successfully")
    return jsonify(success=False, message="File type not allowed")

@app.route('/images', methods=['GET'])
def get_images():
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()
    return jsonify(images=images)

@app.route('/like/<int:image_id>', methods=['POST'])
def like_image(image_id):
    if 'user_id' not in session:
        return jsonify(success=False, message="User not logged in")
    
    user_id = session['user_id']
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND image_id = %s", (user_id, image_id))
    if cursor.fetchone():
        return jsonify(success=False, message="User already liked this image")
    
    cursor.execute("INSERT INTO likes (user_id, image_id) VALUES (%s, %s)", (user_id, image_id))
    cursor.execute("UPDATE images SET likes = likes + 1 WHERE id = %s", (image_id,))
    db.commit()
    
    return jsonify(success=True, message="Image liked successfully")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
