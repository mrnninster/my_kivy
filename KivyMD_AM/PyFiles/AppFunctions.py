# Imports
import re
import bcrypt

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
            return "Enter A Valid Email"

        # For Password
        if (password == ''):
            return "Password Cannot Be Empty"

        # Password Length Check
        if (len(password) < 10):
            return "Use a minimum of 10 Characters"

        # Lowercase Checks
        lc_match = passlc.search(password)
        if (not lc_match):
            return "Include Lower case letters"

        # Uppercase Checks
        Uc_match = passuc.search(password)
        if (not Uc_match):
            return "Include Upper Case Letters"

        # Numeric Checks
        no_match = passno.search(password)
        if (not no_match):
            return "Include a number in your password"

        # Special Characters Checks
        sc_match = passsc.search(password)
        if (not sc_match):
            return "Add a special character to spice up that password"

    except:
        return "Data Authentication Failed"


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


# Check For Empty Fields
def empty_check(field_content):
    if field_content == "":
        return(["Failed", "Please fill all required fields"])
    else:
        return([""])


# Verify Phone Number
def verify_phonenumber(phonenumber):
    if(phonenumber[0] != "+"):
        return(["Failed", "Use International Format, add the '+' sign "])

    elif(len(phonenumber) < 12):
        return(["Failed", "The length of your phone number is not valid"])

    else:
        return([""])


# Verify Name Length
def name_length(first_name, last_name):
    if (first_name < 2) | | (last_name < 2):
        return(["Failed", "The length of the name entered is to short"])
    else:
        return([""])


# Same Password Check
def same_password(regpassword, vregpassword):
    if (regpassword != vregpassword):
        return(["Failed", "Password Mismatch"])
