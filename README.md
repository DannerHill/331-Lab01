# 331-Lab01-Danner Hill
Lab Assignment 1: Security Analysis of Password-Based Authentication
Scenario
I have developed a simple password-based authentication application that allows users to register and log in using a username and password.

# The system provides the following functionality:
1. User registration
2. User login
3. Password storage
4. Password reset

# System Contains:
The password-based authentication system that includes the following components.
1. User Registration
The system allows a user to:
● Enter a username.
● Enter a password.
● Create an account.
● Users may choose their own username during registration. The system ensures that
each username is unique.
● Users may choose their own password during registration. The password must be at least 8 characters in length with no specificaitons certain characters needed.
2. User Login
The system should allow registered users to log in using:
● Username
● Password
3. Password Storage
● The system stores user credentials (username and password) in a database.
4. Password Reset
● Users can reset their password if they forget it using a password reset link.

# Implementation
● The program uses the python language with flask importation to implement a simple web interface to run the program
● To run the program the user must run 'python main.py' to begin the program and from there the terminal will provide the web address to use the program from there
● templates provides all of the html files for each section of this program
● Static provides the css styling for the web interface
● users.db is the SQLite database for storing usernames and passwords