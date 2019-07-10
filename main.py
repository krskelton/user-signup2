from flask import Flask, request, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

#index page loads the form template
@app.route("/")
def index():
    return render_template('form.html', username_errors='', password_errors='', v_password_errors='', email_errors='')
    
#When the form submits the validate method is called
@app.route("/", methods=['POST', 'GET'])
def validate():
    username_errors = ''
    password_errors = ''
    v_password_errors = ''
    email_errors = ''

    #Get inputs from form
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    #FORM VALIDATION
    #username checks for an empty string and whether the string is valid
    if empty_string(username) or not valid_string(username):
        username_errors='Not a valid username'
    
    #password checks for an empty string and whether the string is valid
    if empty_string(password) or not valid_string(password):
        password_errors='Not a valid password'
    
    #verify password checks for an empty string and whether the password input and the verify password match. If they are not equal, it will display an error to the user.
    if empty_string(verify_password) or not is_equal(password,verify_password):
        v_password_errors='Passwords don\'t match'
    
    #First this checks if the user entered an email and then checks if it is valid
    if email and not valid_email(email):
        email_errors='Not a valid email'

    
    
    #If there are no errors, load the welcome page and pass it the username or load the form again with the errors and reset the password fields
    if not username_errors and not password_errors and not v_password_errors and not email_errors:
        return welcome(username)
    else:
        return render_template('form.html', username_errors=username_errors, password_errors=password_errors, v_password_errors=v_password_errors, email_errors=email_errors, username=username, password='', verify_password='', email=email)


#The welcome page loads the welcome template and passes it the username
@app.route("/welcome", methods=['POST'])
def welcome(username):
    return render_template('welcome.html', username=username)


#BELOW ARE THE FUNCTIONS THAT ARE USED FOR THE FORM VALIDATIONS
#Test if a return value is an empty string
def empty_string(value):
    if(len(value) == 0):
        return True
    else:
        return False

#Test whether two variables are equal to one another
def is_equal(variable1, variable2):
    if variable1 == variable2:
        return True
    else:
        return False

#Test whether the text inputs are valid, meaning they are 3 or more characters but 20 or less and do not contain spaces
def valid_string(value):
    if len(value) >= 3 and len(value) <= 20:
        if not " " in value:
            return True
    else:
        return False

#Test whether the email is valid. The email is valid if it contains an @, ., no spaces and is 3 or more characters but 20 or less characters.
def valid_email(email):
    if valid_string(email) and '@' in email and '.' in email:
        return True
    else:
        return False

app.run()