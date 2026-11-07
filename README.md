# 331-Lab04-Danner Hill
Lab Assignment 4: Expanded Security Analysis of Password-Based Authentication
Scenario
I have developed a more secure password-based authentication application that allows users to register and log in using a username and password.

# The system provides the following functionality:
1. User registration
2. User login
3. Encrypted password storage
4. Password reset
5. Lockout capabilities after 3 failed attempts

# System Contains:
The password-based authentication system that includes the following components.
1. User Registration
The system allows a user to:
● Enter a username.
● Enter a password.
● Confirm the password.
● Create an account.
● Users may choose their own username during registration. The system ensures that
each username is unique.
● Users may choose their own password during registration. The password must be at least 8 characters in length, with no specific characters required.
2. User Login
The system allows registered users to log in using:
● Username
● Password
Login protection:
● If authentication fails, a generic error message is displayed ("Invalid username or password."). It does not reveal whether the username or the password was wrong.
● After three consecutive failed login attempts, the account is temporarily locked for 60 seconds. While the account is locked, even the correct password is rejected.
● A successful login resets the failed-attempt counter.
3. Password Storage
● The system stores user credentials (username and hashed password) in a database.
● Passwords are not stored in plaintext. Each password is hashed with bcrypt using a unique, random salt.
● The database also tracks each account's failed login attempts and lock expiry time.
4. Password Reset
● Users can reset their password by entering their username and a new password on the reset page.
● The new password is hashed with bcrypt before it is stored.
● The reset page does not verify the user's identity. This is a known limitation described in the Question 1 write-up.

# Implementation
● The program uses the python language with flask importation to implement a simple web interface to run the program
● To run the program the user must run 'python main.py' to begin the program and from there the terminal will provide the web address to use the program from there
● templates provides all of the html files for each section of this program
● Static provides the css styling for the web interface
● users.db is the SQLite database for storing usernames and passwords