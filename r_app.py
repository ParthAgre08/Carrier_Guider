from flask import Flask, jsonify, request, redirect, session, url_for
from flask_cors import CORS
import requests
import pymysql
from datetime import datetime
from stream_profiles import STREAM_PROFILES
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

connector = pymysql.connect(
host="localhost",
user="flaskuser",
password="12345",
database="carrier_guide" )
cur = connector.cursor()

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

    cur.execute("INSERT INTO USERS (name, email, password, education) VALUES (%s, %s, %s, %s)", (name, email, password, education))
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
    
    if education == 'Grade 10':
        english = int(data.get("english", 0))
        math = int(data.get("math", 0))
        science = int(data.get("science", 0))
        socialscience = int(data.get("socialscience", 0))
        secondlanguage = int(data.get("secondlanguage", 0))

        n_eng = int(data.get("n_eng", 0) or 0)
        if n_eng: english = (english*0.85) + (n_eng*0.15)
        n_math = int(data.get("n_math", 0) or 0)
        if n_math: math = (math*0.85) + (n_math*0.15)
        n_sci = int(data.get("n_sci", 0) or 0)
        if n_sci: science = (science*0.85) + (n_sci*0.15)
        n_social = int(data.get("n_social", 0) or 0)
        if n_social: socialscience = (socialscience*0.85) + (n_social*0.15)
        n_second = int(data.get("n_second", 0) or 0)
        if n_second: secondlanguage = (secondlanguage*0.85) + (n_second*0.15)
         
        session["English"] = english
        session["Math"] = math
        session["Science"] = science
        session["Social Science"] = socialscience
        session["Second Language"] = secondlanguage
        session["Language"] = ((english*0.7)+(secondlanguage*0.3))

        session["student_vector"] = {"Math": math/100, "Science": science/100, "Social": socialscience/100, "Language": session["Language"]/100}

        email = session.get('email')
        cur.execute("INSERT INTO student_marks (email,education,subject,marks) VALUES (%s, %s, 'Language', %s)", (email, education, session['Language']))
        cur.execute("INSERT INTO student_marks (email,education,subject,marks) VALUES (%s, %s, 'Math', %s)", (email, education, math))
        cur.execute("INSERT INTO student_marks (email,education,subject,marks) VALUES (%s, %s, 'Science', %s)", (email, education, science))
        cur.execute("INSERT INTO student_marks (email,education,subject,marks) VALUES (%s, %s, 'Social Science', %s)", (email, education, socialscience))
        connector.commit()

    return jsonify({"success": True, "message": "Assessment recorded"})


@app.route("/personality_assessment", methods=["POST"])
def inrest():
    data = request.json or {}
    total_r = total_i = total_a = total_s = total_e = total_c = 0
    for i in range(1, 7):
        total_r += int(data.get(f"q{i}_r", 0))
        total_i += int(data.get(f"q{i}_i", 0))
        total_a += int(data.get(f"q{i}_a", 0))
        total_s += int(data.get(f"q{i}_s", 0))
        total_e += int(data.get(f"q{i}_e", 0))
        total_c += int(data.get(f"q{i}_c", 0))

    r, i_s, a, s, e, c = total_r/25, total_i/25, total_a/25, total_s/25, total_e/25, total_c/25
    session["riasec_vector"] = {"R": r, "I": i_s, "A": a, "S": s, "E": e, "C": c}
    
    cur.execute("INSERT INTO riasec_vector (email,R, I, A, S, E, C) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (session.get('email'), r, i_s, a, s, e, c))
    connector.commit()
    return jsonify({"success": True, "message": "Personality assessment recorded"})


@app.route("/interest_assessment", methods=["POST"])
def intrest_assesment():
    education = session.get("education")
    if education == 'Grade 10':
        data = request.json or {}
        math_interest = int(data.get("interest_math", 0))
        science_interest = int(data.get("interest_science", 0))  
        buisness_interest = int(data.get("interest_business", 0)) 
        creativity_interest = int(data.get("interest_creative", 0))
        social_interest = int(data.get("interest_social", 0))

        session["intrest_vector"] = {
            "Math": math_interest/5, "Science": science_interest/5, "Business": buisness_interest/5,
            "Creativity": creativity_interest/5, "Social": social_interest/5
        }
    return jsonify({"success": True, "message": "Interest assessment recorded"})


@app.route("/generate_career_profile", methods=["GET"])
def generate_career_profile():
    academic_dict = session.get("student_vector")
    if not academic_dict:
        return jsonify({"success": False, "error": "Missing assessment data"}), 400
        
    ability_student = np.array([academic_dict["Math"], academic_dict["Science"], academic_dict["Social"], academic_dict["Language"]]).reshape(1, -1)
    
    riasec_dict = session.get("riasec_vector")
    riasec_student = np.array([riasec_dict["R"], riasec_dict["I"], riasec_dict["A"], riasec_dict["S"], riasec_dict["E"], riasec_dict["C"]]).reshape(1, -1)

    interest_dict = session.get("intrest_vector")
    intrest_student = np.array([interest_dict["Math"], interest_dict["Science"], interest_dict["Business"], interest_dict["Creativity"], interest_dict["Social"]]).reshape(1, -1)

    scores = {}
    for stream , profile in STREAM_PROFILES.items():
        stream_ability = np.array(profile["academic"]).reshape(1,-1)
        stream_personality = np.array(profile["personality"]).reshape(1,-1)
        stream_intrest = np.array(profile["interest"]).reshape(1,-1)

        stream_academic_similarity = cosine_similarity(ability_student,stream_ability)[0][0]
        stream_personality_similarity = cosine_similarity(riasec_student,stream_personality)[0][0]
        stream_interest_similarity = cosine_similarity(intrest_student,stream_intrest)[0][0]

        scores[stream] = float((stream_academic_similarity*0.5) + (stream_personality_similarity*0.3) + (stream_interest_similarity*0.2))
        
    best_stream = max(scores, key=scores.get)
    confidence_level = f"{round(scores[best_stream]*100,2)}%"
    session["best_stream"] = best_stream
    session["confidence_level"] = confidence_level
    session["scores"] = scores

    return jsonify({"success": True, "best_stream": best_stream, "scores": scores, "confidence_level": confidence_level})


def inference(prompt):
    print("Thinking ......")
    try:
        r = requests.post("http://localhost:11434/api/generate",json={"model":"llama3.2", "prompt":prompt, "stream":False})
        return r.json()
    except Exception as e:
        return {"response": f"Error contacting AI: {str(e)}"}


@app.route("/career_roadmap", methods=["GET"])
def career_roadmap():
    if not session.get("best_stream"):
        return jsonify({"success": False, "error": "No career profile generated"}), 400
        
    prompt = f'''You are an AI Career Guidance Expert.\nYou do not change the predicted stream.\nYou do not override the scoring engine.\nYou only explain and expand on the recommendation.\nYou provide structured, practical, realistic guidance.\nYou never force the student to choose a stream.\nYou suggest, justify, and provide roadmap steps \n Student Profile Data:\n\n    Best Recommended Stream: { session.get("best_stream") }\n    Confidence Level: { session.get("confidence_level") }\n\n    All Stream Scores:\n    Science: { session.get("scores")["Science"] }\n    Commerce: { session.get("scores")["Commerce"] }\n    Arts: { session.get("scores")["Arts"] }\n\n    Academic Strength Vector (0-1 scale):\n    Math: { session.get("student_vector")["Math"] }\n    Science: { session.get("student_vector")["Science"] }\n    Social Science: { session.get("student_vector")["Social"] }\n    Language: {session.get("student_vector")["Language"] }\n\n    RIASEC Personality Scores (0-1 scale):\n    Realistic: { session.get("riasec_vector")["R"] }\n    Investigative: { session.get("riasec_vector")["I"] }\n    Artistic: { session.get("riasec_vector")["A"] }\n    Social: { session.get("riasec_vector")["S"] }\n    Enterprising: { session.get("riasec_vector")["E"] }\n    Conventional: { session.get("riasec_vector")["C"] }\n\n    Interest Scores (0-1 scale):\n    Mathematics: { session.get("intrest_vector")["Math"] }\n    Science: { session.get("intrest_vector")["Science"] }\n    Business: { session.get("intrest_vector")["Business"] }\n    Creative: { session.get("intrest_vector")["Creativity"] }\n    Social: { session.get("intrest_vector")["Social"] }\n\n\n    Instructions:\n\n    1. Explain why the recommended stream is suitable based on academic strengths, personality, and interests.\n    2. Mention the second-best stream and explain briefly why it is also a possible option.\n    3. Provide a 3-year roadmap (11th, 12th, Entrance Exams preparation).\n    4. Suggest 5 career options after graduation.\n    5. Suggest skill improvement areas based on weaker dimensions.\n    6. Keep tone encouraging and practical.\n    7. Do not contradict the predicted stream.\n    8. Format response in clear sections with headings.'''
    
    response_data = inference(prompt)
    response_text = response_data.get("response", "No response generated")
    
    return jsonify({"success": True, "roadmap": response_text})


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
