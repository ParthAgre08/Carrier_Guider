import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Imports and config
content = content.replace('from flask import Flask,render_template,request,redirect, session,url_for', 
'''from flask import Flask, jsonify, request, redirect, session, url_for
from flask_cors import CORS''')

content = content.replace('app.secret_key = "super_secret_key"\n# Without this → session will not work.',
'''app.secret_key = "super_secret_key"
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])''')

content = content.replace('database="carrier_guider" )', 'database="carrier_guide" )')

# 2. Starting, login, register, main
# We'll just replace everything up to the assessment route.
idx_assessment = content.find('@app.route("/assessment" , methods =["GET","POST"])')

new_top = '''#We then use the route() deco    rator to tell Flask what URL should trigger our function.
@app.route("/")
def starting():
    return jsonify({"message": "API is running"})

@app.route("/login", methods=["POST"])
def already_register():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")

    cur.execute("SELECT * FROM USERS WHERE Email=%s AND Password=%s", (email, password))
    user = cur.fetchone()
    if user:
        session["user"] = user[1]
        session["email"] = email
        session["education"] = user[4]
        return jsonify({"success": True, "name": user[1], "greeting": "Welcome back", "education": user[4]})
    else:
        return jsonify({"success": False, "error": "Incorrect Password"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    education = data.get("education")

    cur.execute("SELECT * FROM USERS WHERE Email = %s", (email,))
    user = cur.fetchone()
    if user:
        return jsonify({"success": False, "error": "Email is already registered"}), 400

    cur.execute("INSERT INTO USERS (name,email,password,education) VALUES (%s,%s,%s,%s)", (name,email,password,education))
    connector.commit()
    session["user"] = name
    session["email"] = email
    session["education"] = education
    return jsonify({"success": True, "name": name, "greeting": "Welcome to Carrier Guider"})

@app.route("/main", methods=["GET"])
def main():
    if "user" in session:
        return jsonify({"success": True, "name": session["user"], "education": session.get("education")})
    return jsonify({"success": False, "error": "Not logged in"}), 401

@app.route("/assessment", methods=["POST"])
def assessment():
   education = session.get("education")
   if not education:
       return jsonify({"success": False, "error": "No education set in session"}), 400
   
   data = request.json or {}
'''

# Now extract the assessment block and replace request.form with data.get
end_idx_assessment = content.find('@app.route("/personality_assessment"', idx_assessment)
assessment_block = content[idx_assessment:end_idx_assessment]

# Clean up assessment block:
assessment_block = assessment_block.replace('@app.route("/assessment" , methods =["GET","POST"])\ndef assessment():\n   education = session.get("education")\n\n   if(request.method == "POST"):', '')
assessment_block = assessment_block.replace('request.form.get', 'data.get')
assessment_block = re.sub(r'request\.form\["(.*?)"\]', r'data.get("\1", 0)', assessment_block)
# remove the trailing `else:` and return statements at the end of assessment
assessment_block = re.sub(r'return render_template.*', r'', assessment_block)
assessment_block = assessment_block.replace('else:\n      if(education == \'Grade 10\'):', '')
assessment_block = re.sub(r'elif\(education == \'Grade.*?\):', '', assessment_block)
assessment_block = assessment_block.replace('elif(education == \'Diploma/Polytechnic\'):', '')
assessment_block = assessment_block.replace('elif(education == \'UG\'):', '')

# add return at end of assessment
assessment_block = assessment_block.strip()
# It will have dangling code from the else block. Let's just do it manually by regex.
# Actually, the python block replacing is tricky.
'''

with open('patch_full.py', 'w', encoding='utf-8') as f:
    f.write(code)
