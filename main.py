import flask


# TODO: change this to your academic email
AUTHOR = "shafaam@wharton.upenn.edu"


app = flask.Flask(__name__)


# This is a simple route to test your server


@app.route("/")
def hello():
    return f"Hello from my Password Validator! &mdash; <tt>{AUTHOR}</tt>"


# This is a sample "password validator" endpoint
# It is not yet implemented, and will return HTTP 501 in all situations

@app.route("/v1/checkPassword", methods=["POST"])
def check_password():
    data = flask.request.get_json() or {}
    pw = data.get("password", "")
    
    errors = []
    
    if len(pw) < 8:
        errors.append("Password must be at least 8 characters long.")

    uppercase_count = sum(1 for c in pw if c.isupper())
    if uppercase_count < 2:
        errors.append("Password must contain at least 2 uppercase letters.")
    
    digit_count = sum(1 for c in pw if c.isdigit())
    if digit_count < 2:
        errors.append("Password must contain at least 2 digits.")
    
    special_chars = set("!@#$%^&*")
    special_count = sum(1 for c in pw if c in special_chars)
    if special_count < 1:
        errors.append("Password must contain at least 1 special character (!@#$%^&*).")
    
    valid = len(errors) == 0
    reason = "" if valid else " ".join(errors)
    
    return flask.jsonify({"valid": valid, "reason": reason}), 200

