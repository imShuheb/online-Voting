# Voting System Web Application

This is a simple web application built with Flask, a Python web framework, designed for conducting online voting. The application provides functionalities for both voters and administrators. It allows voters to register, log in, and cast their votes for candidates, while administrators can manage candidates, view voting results, and perform other administrative tasks.

## Features

- **User Registration and Authentication**: Voters can sign up with their personal details such as name, email, phone number, and Aadhar card number. They receive a one-time password (OTP) via email for authentication.
- **Candidate Management**: Administrators can add, edit, and delete candidate profiles. Each candidate profile includes details such as name, contact information, address, photo, qualification, and vote count.
- **Voting Mechanism**: Registered voters can log in, view a list of candidates, and cast their votes. The system ensures that each voter can only vote once.
- **Result Display**: Administrators can view the voting results, showing the number of votes received by each candidate.
- **Session Management**: The application manages user sessions securely using Flask-Login.
- **Email Notification**: Voters receive an OTP via email for registration and authentication purposes.
- **File Upload**: Administrators can upload candidate photos for their profiles.

## Installation and Setup

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Install Dependencies**: Navigate to the project directory and install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. **Database Setup**: Set up a MySQL database and configure the database URI in `app.config['SQLALCHEMY_DATABASE_URI']` in `app.py`.

4. **Mail Configuration**: Configure your SMTP server details (e.g., Gmail) in the `app.config.update` section of `app.py` to enable email functionality.

5. **Run the Application**: Run the Flask application by executing the following command:

   ```
   python main.py
   ```

6. **Access the Application**: Access the application in your web browser by visiting `http://localhost:5000`.

## Usage

- **User Registration**: Users can sign up by providing their details and receiving an OTP via email.
- **User Authentication**: Users can log in using their Aadhar card number and the OTP received during registration.
- **Candidate Management**: Administrators can add, edit, or delete candidate profiles, including uploading candidate photos.
- **Voting**: Registered users can view the list of candidates and cast their votes. Each user can only vote once.
- **Result Display**: Administrators can view the voting results, showing the number of votes received by each candidate.
- **Session Management**: The application handles user sessions securely, ensuring authenticated access to relevant features.