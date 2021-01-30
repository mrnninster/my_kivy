# Imports
import re
import bcrypt
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

    # Verify User Data
    verify(email, password)

    # Validate User
    # try:
    #     # Query Database
    #     # Verify Credentials
    #     # Store Vefified Credentials for auto login
    #     Manager_info = Managers.query.filter_by(Email=email).all()
    #     password = bytes(str(password), 'utf-8')

    #     if bcrypt.checkpw(password, Manager_info[0].Password):
    #         print('Succefully Logged In ' +
    #                 str(Manager_info[0].Author_Name))
    #         session.permanent = True
    #         session['Activity_Manager_Name'] = Manager_info[0].Author_Name
    #         session['Email'] = Manager_info[0].Email
    #         session['Activity_Manager'] = Manager_info[0].Phone_Num
    #         session['Manager_mail_hash'] = hash_mail
    #         session["Balance"] = Manager_info[0].Current_Balance

    #         Balance = session['Balance']
    #         all_zones = pytz.all_timezones
    #         return(redirect(url_for("today")))
    #     else:
    #         info = 'Unable To Verify Password'
    #         return render_template('demo1.html', info=info)
    # except:
    #     return "Inavlid Username or password"

    print(email, password)


# Register User With Web Server
def register_user(first_name, last_name, company, email, phone_number, regpassword, vregpassword, usecase):
    # url = "http://127.0.0.1:5000/mobile_create_manager"

    # hash_pass = bcrypt.hashpw(
    #     bytes(str(regpassword), 'utf-8'), bcrypt.gensalt())

    # payload = {"first_name": first_name,
    #            "last_name": last_name,
    #            "company": company,
    #            "email": email,
    #            "phone_number": phone_number,
    #            "password": hash_pass,
    #            "use_case": usecase}
    # files = [

    # ]
    # headers = {}

    # response = requests.request(
    #     "POST", url, headers=headers, data=payload, files=files)

    # print(response.text)

    url = "http://127.0.0.1:5000/mobile_create_manager"

    hash_pass = bcrypt.hashpw(
        bytes(str(regpassword), 'utf-8'), bcrypt.gensalt())
    hash_pass = bcrypt.hashpw(
        bytes(str(Password), 'utf-8'), bcrypt.gensalt())

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

    print("POST", url, headers, payload, files)
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    res = response.text


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
