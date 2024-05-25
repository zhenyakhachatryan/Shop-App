## Shop App 
Welcome to the Shop App! This application is a fully functional e-commerce platform that allows users to browse products, register, log in, and manage their shopping experience. The app supports both user and admin roles, enabling a comprehensive shopping experience and backend management.

## Features

- **User Registration and Login**: Users can register and log in securely using their email and password.
- **Google Authentication**: Users can also log in using their Google accounts.
- **Password Reset**: Users can reset their passwords if they forget them.
- **Admin Panel**: Admins have access to a dedicated panel to manage the application.
- **Product Management**: Admins can add, edit, and remove products from the database.
- **SSL Security**: The application uses SSL certificates to ensure secure communication.
- **Server Configuration**: The app includes setup instructions for running a secure server.


## Technologies Used

- **Frontend Template**: The frontend template was downloaded from the internet and integrated with our backend.
- **Backend**: The backend was developed using Flask.
- **Authentication**: Secure user authentication using OAuth and Flask-Login.
- **Database**: SQLite with SQLAlchemy ORM.
- **SSL**: Secure Sockets Layer (SSL) for encrypted communication.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/zhenyakhachatryan/Shop-App.git 
   cd Shop-App

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```bash
      source venv/bin/activate
      ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up your environment variables. Create a `.env` file in the root directory and add your API key:

    ```plaintext
    FLASK_APP=app.py
    SECRET_KEY = Your_secret_key
    MAIL_SERVER= SMTP_server_address
    MAIL_PORT=SMTP_server_port
    MAIL_USE_TLS=Use TLS encryption (True/False)
    MAIL_USERNAME=Your_SMTP_username
    MAIL_PASSWORD= Your_SMTP_password
    MAIL_DEFAULT_SENDER=Default_sender_email
    GOOGLE_CLIENT_ID=Your_Google OAuth_client ID
    GOOGLE_CLIENT_SECRET=Your_Google OAuth_client secret
    ```
6. Obtain SSL Certificates
   
7.Configure SSL 

8. Run the application:

    ```bash
    flask run
    ```

9. Open your browser and go to `http://127.0.0.1:5000`.

## Usage
For Users

- Register: Create a new account using your email and password or Google account.
- Login: Access your account using your credentials.
- Password Reset: Reset your password if you forget it.
- Browse Products: Explore and search for products available in the shop.

  
For Admins

- Admin Panel: Log in to the admin panel to manage the application.
- Product Management: Add, edit, and delete products in the database.
- User Management: View and manage registered users.

##Contact

For questions or support, please contact me at khachatryanzhenya3@gmail.com.

Thank you for using Shop App!

