# Imports
import re
import json
import bcrypt
import sqlite3
import requests
import datetime

# Colours In Use
primaryColor = "#0d0d0d"
primaryLightColor = "#0d0d0d"
primaryDarkColor = "#000000"
secondaryColor = "#531489"
secondaryLightColor = "#8444ba"
secondaryDarkColor = "#20005b"
primaryTextColor = "#ffffff"
secondaryTextColor = "#ffffff"

def connect_db():
    # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

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


# Task Table In database
def Task_Table():
    # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

    # Make Task Table
    try:
        c.execute(""" CREATE TABLE  Local_Tasks(
            id INTEGER NOT NULL PRIMARY KEY,
            Task_Name TEXT NOT NULL,
            Task_Describe TEXT NOT NULL,
            Recipients TEXT NOT NULL,
            Manager_Name TEXT NOT NULL,
            Manager_No TEXT NOT NULL,
            Manager_Email TEXT NOT NULL,
            TaskID TEXT NOT NULL,
            Feedback TEXT NOT NULL,
            Go_Live_Time timestamp
        )""")
    except:
        return(["Failed","Unable To Create Local Task Service"])

# Update User Signed In State
def Status_Update(email,password):

    # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

    try:
        c.execute("""UPDATE userInfo SET status = :status WHERE email = :email AND password = :password""",
            {"email":email, "password":password, "status":1})

        # commit db transactions
        conn.commit()

        # close connection
        conn.close()
    
    except Exception as e:
        print(str(e))
        return["Failed", "Unable to Complete Set Up"]


# Revert User Signed In Status
def Status_Revert(email,password):

    # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

    c.execute("""UPDATE userInfo SET status = :status WHERE email = :email AND password = :password""",
        {"email":email, "password":password, "status":0})

    # commit db transactions
    conn.commit()

    # close connection
    conn.close()


# Save To Local DB
def Local_Save(first_name,last_name,company,email,phone_number,password,usecase="",status=0):
    
     # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

    # Populate UserInfo Table
    c.execute(f"INSERT INTO userInfo VALUES {first_name, last_name, company, email, phone_number, password, usecase, status}")

    # commit db transactions
    conn.commit()

    # close connection
    conn.close()


# Fetch All Todays From Local Storage
def Today_Local():
    # db connection
    conn = sqlite3.connect("user.db")

    # create cursor
    c = conn.cursor()

    # Fetch Tasks
    try:    
        # Select Current Users Local Tasks
        Task_query = c.execute("""SELECT * FROM Local_Tasks WHERE Manager_Name=:managerName AND Manager_No=:managerNo""",{"managerName":managerName,"managerNo":managerNo})
    
    except Exception as e:
        return(["Failed","Unable To Access Task For Today"])

    else:
        # Filter For Todays Tasks
        Today = list()
        for Task in Task_query:
            if Task.Go_Live_Time == datetime.date():
                Today.append(Task)
        
        # All Tasks For Today
        return Today


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
            return (["Failed", "Enter A Valid Email"])

        # For Password
        if (password == ''):
            return (["Failed", "Password Cannot Be Empty"])

        # Password Length Check
        if (len(password) < 10):
            return (["Failed", "Password must be minimum of 10 Characters"])

        # Lowercase Checks
        lc_match = passlc.search(password)
        if (not lc_match):
            return (["Failed", "Include Lower case letters in password"])

        # Uppercase Checks
        Uc_match = passuc.search(password)
        if (not Uc_match):
            return (["Failed", "Include Upper Case Letters in password"])

        # Numeric Checks
        no_match = passno.search(password)
        if (not no_match):
            return (["Failed", "Include a number in password"])

        # Special Characters Checks
        sc_match = passsc.search(password)
        if (not sc_match):
            return (["Failed", "Add a special character to spice up that password"])
        else:
            return([""])

    except:
        return (["Failed", "Data Authentication Failed"])



# Sign In Function
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
                "SELECT * FROM userInfo WHERE Email=:email AND password=:password",{"email":email, "password":password})

        except:
            return(["Failed", "Invalid Email or Password, Verify and Try Again"])

        else:
            # Try Fetching UserInfo
            try:
                # Offline Query
                user=c.fetchone()

                # Online Query
                if user == None:

                    # Connect To Server and Return Response
                    try:
                        user=server_query(email, password)

                    # If there is an exception in the code
                    except:
                        return(["Failed", "Unable To Connect To Server, Internet Connection Required"])

                    # Query Response
                    else:

                        # If The Email Is Invalid
                        if user == None:
                            return(["Failed", "Invalid Email"])
                        
                        else:
                            user = user.json()
                            # User Credential Failure
                            if user["status"] == "Failed" and user["response"] != "Invalid Password":
                                return(["Failed","Invalid Credentials"])
                            
                            # If Password Fails
                            elif user["status"] == "Failed" and user["response"] == "Invalid Password":
                                return(["Failed","Invalid Password"])
                            
                            # On Success
                            elif user["status"] == "Success":
                                full_name = user["Name"]
                                names = full_name.split(" ")
                                phone_number = f"+{user['Number']}"
                                Local_Save(names[0],names[1],user["Company"],user["Email"],phone_number,password,user["Use_Case"])
                                return(["Success",{names[0],names[1],user["Company"],user["Email"],phone_number,password,user["Use_Case"],0}])
                
                # If User Exist On Local DB
                else:
                    return(["Success",user])

            except Exception as e:
                print(str(e))
                return(["Failed", "App Error, kindly report to support@agroai.farm, \nThanks."])

    except:
        return(["Failed", "Verify Email and Try Again"])


# Register User With Web Server
def register_user(first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase):
    url="http://127.0.0.1:5000/mobile_create_manager"

    hash_pass=bcrypt.hashpw(
        bytes(str(regpassword), 'utf-8'), bcrypt.gensalt())

    payload={"first_name": first_name,
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
        "POST", url, headers = headers, data = payload, files = files)

    return response


# Query Server For User Info
def server_query(email, password):
    url="http://127.0.0.1:5000/mobile_check_manager"

    hash_pass=password

    payload={"email": email, "password": hash_pass}

    files=[]

    headers={}

    response=requests.request(
        "POST", url, headers = headers, data = payload, files = files)

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
