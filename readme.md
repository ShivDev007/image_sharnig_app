# PicShare

PicShare is a web application that allows users to upload and share images. Users can view all uploaded images, and logged-in users can like the images. The application features user authentication, including the ability to sign up, log in, and log out. Only authenticated users can like images.

## Features

- User authentication (signup, login, logout)
- Image upload
- View all uploaded images
- Like images (only for logged-in users)
- Responsive design with a dark theme

## Technologies Used

- Flask (Python)
- MySQL
- Bootstrap
- JavaScript (Fetch API)
- HTML/CSS

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/picshare.git
   cd picshare
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database:**

   - Create a new MySQL database.
   - Run the following SQL commands to create the necessary tables:

     ```sql
     CREATE DATABASE image_sharing;
     USE image_sharing;

     CREATE TABLE users (
         id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(50) NOT NULL UNIQUE,
         password VARCHAR(255) NOT NULL
     );

     CREATE TABLE images (
         id INT AUTO_INCREMENT PRIMARY KEY,
         image_url VARCHAR(255) NOT NULL,
         likes INT DEFAULT 0
     );

     CREATE TABLE likes (
         id INT AUTO_INCREMENT PRIMARY KEY,
         user_id INT NOT NULL,
         image_id INT NOT NULL,
         UNIQUE (user_id, image_id)
     );
     ```

5. **Update the Flask app configuration:**

   - Open `app.py` and update the MySQL database connection settings:

     ```python
     db = mysql.connector.connect(
         host="localhost",
         user="your_mysql_username",
         password="your_mysql_password",
         database="image_sharing"
     )
     ```

   - Replace `your_mysql_username` and `your_mysql_password` with your MySQL credentials.

6. **Run the application:**

   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Usage

1. **Sign Up:**

   - Open the application in your browser.
   - Sign up for a new account by providing a username and password.

2. **Log In:**

   - Log in using your username and password.

3. **Upload Images:**

   - Once logged in, you can upload images using the upload button.

4. **View and Like Images:**

   - All users can view uploaded images.
   - Only logged-in users can like images by clicking the thumbs-up button.

## Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Login Page
![Login Page](screenshots/login.png)

### Sign Up Page
![Sign Up Page](screenshots/signup.png)

### Upload Image
![Upload Image](screenshots/upload.png)

### View Images
![View Images](screenshots/images.png)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)

```

### Summary of Changes
1. **Description**: Added a brief description of the project and its features.
2. **Technologies Used**: Listed the technologies used in the project.
3. **Installation**: Provided step-by-step instructions on how to set up the project locally.
4. **Usage**: Included instructions on how to sign up, log in, upload images, and like images.
5. **Screenshots**: Added placeholders for screenshots of different parts of the application.
6. **License**: Included a section for the license information.
7. **Acknowledgements**: Acknowledged the tools and libraries used in the project.

Feel free to replace the placeholder text and add actual screenshots in the `screenshots` folder.