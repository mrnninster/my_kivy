# Imports
import re
import bcrypt
import sqlite3
import requests

# Colours In Use
primaryColor = "#0d0d0d"
primaryLightColor = "#0d0d0d"
primaryDarkColor = "#000000"
secondaryColor = "#531489"
secondaryLightColor = "#8444ba"
secondaryDarkColor = "#20005b"
primaryTextColor = "#ffffff"
secondaryTextColor = "#ffffff"

# Create DataBase


def create_db(first_name, last_name, company, email, phone_number, regpassword, usecase, status):

    # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

    # create User Table
    try:
        c.execute(""" CREATE TABLE  userInfo(
            fname text,
            lname text,
            company text,
            Email text,
            userNumber text,
            password text,
            usecase text,
            status integer
        )""")

    except:
        pass

    # Populate Table
    c.execute(
        f"INSERT INTO userInfo VALUES {first_name, last_name, company, email, phone_number, regpassword, usecase, status}")

    # commit db transactions
    conn.commit()

    # close connection
    conn.close()


# Functions
def verify(email, password, *args):
    # Regex Checks
    pattern = re.compile(r'[a-zA-Z0-9.-_]+[a-zA-Z0-9.-_]\.[a-zA-Z0-9.-_]')
    passlc = re.compile(r'[a-z]+')
    passuc = re.compile(r'[A-Z]+')
    passno = re.compile(r'[0-9]+')
    passsc = re.compile(r'[\.\@\_\-\+\$]+')

    try:
        # For Email
        match = pattern.search(email)
        if (not match):
            return ("Failed", "Enter A Valid Email")

        # For Password
        if (password == ''):
            return ("Failed", "Password Cannot Be Empty")

        # Password Length Check
        if (len(password) < 10):
            return ("Failed", "Password must be minimum of 10 Characters")

        # Lowercase Checks
        lc_match = passlc.search(password)
        if (not lc_match):
            return ("Failed", "Include Lower case letters in password")

        # Uppercase Checks
        Uc_match = passuc.search(password)
        if (not Uc_match):
            return ("Failed", "Include Upper Case Letters in password")

        # Numeric Checks
        no_match = passno.search(password)
        if (not no_match):
            return ("Failed", "Include a number in password")

        # Special Characters Checks
        sc_match = passsc.search(password)
        if (not sc_match):
            return ("Failed", "Add a special character to spice up that password")
        else:
            return([""])

    except:
        return ("Failed", "Data Authentication Failed")


def sign_in_check(email, password, *args):

    # Check for input standard
    verify(email, password)

    # Validate User
    try:
        # db connection
        conn = sqlite3.connect("user.db")

        # create cursor
        c = conn.cursor()

        try:
            # Query Database
            c.execute(
                f"SELECT * FROM userInfo WHERE Email = 'adefolahan.akinsola@agroai.farm'")

        except:
            return{["Failed", "Invalid Email, Verify Email and Try Again"]}

        else:
            # Try Fetching UserInfo
            try:
                # Offline Query
                user = c.fetchone()

                # Online Query
                if user == None:

                    # Connect To Server and Return Response
                    try:
                        user = server_query(email, password)
                        return(user.json())

                    except:
                        return(["Failed", "Unable To Connect To Server, Internet Connection Required"])

                # Query Response
                if user == None:
                    return(["Failed", "Invalid Credentials"])

            except Exception as e:
                return(["Failed", "App Error, kindly report to support@agroai.farm, \nThanks."])

    except Exception as e:
        return{["Failed", "Verify Email and Try Again"]}

# Register User With Web Server


def register_user(first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase):
    url = "http://127.0.0.1:5000/mobile_create_manager"

    hash_pass = bcrypt.hashpw(
        bytes(str(regpassword), 'utf-8'), bcrypt.gensalt())

    payload = {"first_name": first_name,
               "last_name": last_name,
               "company": company,
               "email": email,
               "phone_number": phone_number,
               "password": hash_pass,
               "usecase": usecase}
    files = [

    ]
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return response


# Query Server For User Info
def server_query(email, password):
    url = "http://127.0.0.1:5000/mobile_check_manager"

    hash_pass = password

    payload = {"email": email, "password": hash_pass}

    files = []

    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    return response


# Check For Empty Fields
def empty_check(field_content):
    if field_content == "":
        return(["Failed", "Please fill all required fields"])
    else:
        return([""])


# Verify Phone Number
def verify_phonenumber(phonenumber):
    if(phonenumber[0] != "+"):
        return(["Failed", "Use International Mobile Number Format, add the '+' sign "])

    elif(len(phonenumber) < 12):
        return(["Failed", "The length of your phone number is not valid"])

    else:
        return([""])


# Verify Name Length
def name_length(first_name, last_name):
    if (len(first_name) < 2) or (len(last_name) < 2):
        return(["Failed", "Each Name must be at least 2 letters"])
    else:
        return([""])


# Same Password Check
def same_password(regpassword, vregpassword):
    if (regpassword != vregpassword):
        return(["Failed", "Password Mismatch"])
    else:
        return([""])
