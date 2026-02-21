from flask import Flask,render_template,request,redirect, session,url_for
import requests
import pymysql
from datetime import datetime
from stream_profiles import STREAM_PROFILES
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


app = Flask(__name__)# __name__ = It tells the Flask application that this file’s location is the main folder where static, templates, and other files are located.


app.secret_key = "super_secret_key"
# Without this → session will not work.

connector = pymysql.connect(
host="localhost",
user="flaskuser",
password="12345",
database="carrier_guider" )
cur = connector.cursor()


#We then use the route() deco    rator to tell Flask what URL should trigger our function.
@app.route("/")
def starting():
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def already_register():
    if request.method == "POST":
       email = request.form["email"]
       password = request.form["password"]

       cur.execute("SELECT * FROM USERS WHERE Email=%s AND Password=%s", (email, password))
       user = cur.fetchone()
       if user:
          print(user)
          session["user"] = user[1]
          session["email"] = email
          session["education"] = user[4]
          return render_template("main.html", name=user[1], greeting="Welcome back")
       else:
          return render_template("login.html",error = "Incorrect Password")

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
   if request.method == "POST":
      name = request.form["name"] 
      email = request.form["email"]    
      password = request.form["password"] 
      education = (request.form["education"])
      print(f"Name :- {name} \nEmail :- {email} \nPassword :- {password} \nEducation :- {education}")
      

      cur.execute(f"SELECT * FROM USERS WHERE Email = '{email}'")
      user = cur.fetchone()
      
      print(f"user :- {user}")

      if user:
         return render_template("register.html",error= "Email is alredy registerd")

      # cur.execute("use carrier_guider;")
      # connector.commit()
      cur.execute(f"INSERT INTO USERS (name,email,password,education) values ('{name}','{email}','{password}','{education}')")
      connector.commit()
      session["user"] = name
      session["email"] = email
      session["education"] = education
      return render_template("main.html",name=name,greeting="Welcome to Carrier Guider")
   return render_template("register.html")
    

@app.route("/main",methods=["GET","POST"])
def main():
   return render_template("main.html")
 

@app.route("/assessment" , methods =["GET","POST"])
def assessment():
   education = session.get("education")
   

   if(request.method == "POST"):
      if(education == 'Grade 10'):
         english = int(request.form.get("english"))
         math = int(request.form.get("math"))
         science = int(request.form.get("science"))
         socialscience = int(request.form.get("socialscience"))
         secondlanguage = int(request.form.get("secondlanguage"))

         n_eng = n_sci =n_math =n_social =n_second = 0
         if(request.form.get("n_eng")): 
            n_eng = int(request.form.get("n_eng"))
            english = (english*0.85) + (n_eng*0.15)
            

         if(request.form.get("n_math")):
            n_math = int(request.form.get("n_math"))
            math = (math*0.85) + (n_math*0.15)
         if(request.form.get("n_sci")):
            n_sci = int(request.form.get("n_sci"))
            science = (science*0.85) + (n_sci*0.15)
         if(request.form.get("n_social")):            
            n_social = int(request.form.get("n_social"))
            socialscience = (socialscience*0.85) + (n_social*0.15)
         if(request.form.get("n_second")):            
            n_second = int(request.form.get("n_second"))
            secondlanguage = (secondlanguage*0.85) + (n_second*0.15)
         
         # storing the marks in session
         session["English"] = english
         session["Math"] = math
         session["Science"] = science
         session["Social Science"] = socialscience
         session["Second Language"] = secondlanguage
         session["Language"] = ((english*0.7)+(secondlanguage*0.3))

         session["student_vector"] = {
            "Math": math/100,
            "Science": science/100,
            "Social": socialscience/100,
            "Language": ((english*0.7)+(secondlanguage*0.3))/100
         }

         # storing the marks in student_marks table 
         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Language', {session['Language']})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Math', {math})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Science', {science})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Social Science', {socialscience})")
         connector.commit()

         # cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Second Language', {secondlanguage})")
         connector.commit()

         print(f"Math :- {math} \nScience :- {science} \nSocial Science :- {socialscience} \nLanguage :- {session['Language']} ")
      
      
      elif(education == 'Grade 12 Science(PCM)'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMathematics :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Grade 12 Science(PCB)'):
         english = request.form["english"]
         biology = request.form["biology"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nBiology :- {biology} \nPhysics :- {physics} \nChemistry :- {chemistry} ")
      
      elif(education == 'Grade 12 Science(PCMB)'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         biology = request.form["biology"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} \nBiology :- {biology}")
      
      elif(education == 'Grade 12 Commerce'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Grade 12 Arts'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Diploma/Polytechnic'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'UG'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
         
      return render_template("personality_assessment.html",Education = education,english=english,math=math,science=science,socialscience=socialscience,secondlanguage=secondlanguage,n_eng=n_eng,n_math=n_math,n_sci=n_sci,n_social=n_social,n_second=n_second)

   else:
      if(education == 'Grade 10'):
         return render_template("grade10.html",Education = education)

      elif(education == 'Grade 12 Science(PCM)'):
         return render_template("grade12pcm.html",Education = education)

      elif(education == 'Grade 12 Science(PCB)'):
         return render_template("grade12pcb.html",Education = education)

      elif(education == 'Grade 12 Science(PCMB)'):
         return render_template("grade12pcmb.html",Education = education)

      elif(education == 'Grade 12 Commerce'):
         return render_template("grade12commerce.html",Education = education)

      elif(education == 'Grade 12 Arts'):
         return render_template("grade12arts.html",Education = education)

      elif(education == 'Diploma/Polytechnic'):
         return render_template("dip_pol.html",Education = education)

      elif(education == 'UG'):
         return render_template("ug.html",Education = education)
   return render_template("assessment.html",Education = education)


@app.route("/personality_assessment",methods=["GET","POST"])
def inrest():
   if request.method == "POST":
      total_r = total_i = total_a = total_s = total_e = total_c = 0
      for i in range(1, 7):
         total_r += int(request.form.get(f"q{i}_r", 0))
         total_i += int(request.form.get(f"q{i}_i", 0))
         total_a += int(request.form.get(f"q{i}_a", 0))
         total_s += int(request.form.get(f"q{i}_s", 0))
         total_e += int(request.form.get(f"q{i}_e", 0))
         total_c += int(request.form.get(f"q{i}_c", 0))

      r = total_r/25
      i = total_i/25
      a = total_a/25
      s = total_s/25
      e = total_e/25
      c = total_c/25
      session["riasec_vector"] = {
            "R": r,
            "I": i,
            "A": a,
            "S": s,
            "E": e,
            "C": c
         }
      cur.execute(f"INSERT INTO riasec_vector (email,R, I, A, S, E, C) VALUES ('{session['email']}', {r}, {i}, {a}, {s}, {e}, {c})")
      connector.commit()
      if(session["education"] == 'Grade 10'):
         return render_template("10th_intrest.html") 
      
      elif(session["education"] == 'Grade 12 Science(PCM)'):
         return render_template("12th_pcm_intrest.html")

      elif(session["education"] == 'Grade 12 Science(PCB)'):
         return render_template("12th_pcb_intrest.html")

      elif(session["education"] == 'Grade 12 Science(PCMB)'):
         return render_template("12th_pcmb_intrest.html")

      elif(session["education"] == 'Grade 12 Commerce'):
         return render_template("12th_commerce_intrest.html")

      elif(session["education"] == 'Grade 12 Arts'):
         return render_template("12th_arts_intrest.html")

      elif(session["education"] == 'Diploma/Polytechnic'):
         return render_template("dip_pol_intrest.html")

      elif(session["education"] == 'UG'):
         return render_template("ug_intrest.html")

   return render_template("personality_assessment.html")


@app.route("/interest_assessment",methods=["GET","POST"])
def intrest_assesment():
   if request.method == "POST":
      if(session["education"] == 'Grade 10'):
         math_interest = int(request.form.get("interest_math"))
         science_interest = int(request.form.get("interest_science"))  
         buisness_interest = int(request.form.get("interest_business")) 
         creativity_interest = int(request.form.get("interest_creative"))
         social_interest = int(request.form.get("interest_social"))

         session["intrest_vector"] = {
            "Math": math_interest/5,
            "Science": science_interest/5,
            "Business": buisness_interest/5,
            "Creativity": creativity_interest/5,
            "Social": social_interest/5
         }

         print(f"Math Interest :- {math_interest} \nScience Interest :- {science_interest} \nBusiness Interest :- {buisness_interest} \nCreativity Interest :- {creativity_interest} \nSocial Interest :- {social_interest}")
         return redirect(url_for("generate_career_profile"))#now jump to the next url after intrest submission to calculate the career profile and send to the web page 
         
      
      
      elif(session["education"] == 'Grade 12 Science(PCM)'): 
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'Grade 12 Science(PCB)'):
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'Grade 12 Science(PCMB)'):
         return render_template("generate_career_profile.html")   
      elif(session["education"] == 'Grade 12 Commerce'): 
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'Grade 12 Arts'):
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'Diploma/Polytechnic'):
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'UG'):
         return render_template("generate_career_profile.html")
        
   
      
   return redirect (url_for("generate_career_profile"))
   # return render_template("generate_career_profile.html")
   

@app.route("/generate_career_profile",methods=["GET","POST"])
def generate_career_profile():
      #we get the student normalize data from the session and we take the values from it because it is save in the dictionary(key values pair) then we convert into the list and then we convert it into the 2d array using numpy becuase cosine similarity expect the 2d array not a list or 1d array 
      academic_dict = session.get("student_vector")
      ability_student = np.array([
         academic_dict["Math"],
         academic_dict["Science"],
         academic_dict["Social"],
         academic_dict["Language"]
      ]).reshape(1, -1)
      
      riasec_dict = session.get("riasec_vector")

      riasec_student = np.array([
         riasec_dict["R"],
         riasec_dict["I"],
         riasec_dict["A"],
         riasec_dict["S"],
         riasec_dict["E"],
         riasec_dict["C"]
      ]).reshape(1, -1)


      interest_dict = session.get("intrest_vector")

      intrest_student = np.array([
         interest_dict["Math"],
         interest_dict["Science"],
         interest_dict["Business"],
         interest_dict["Creativity"],
         interest_dict["Social"]
      ]).reshape(1, -1)


      scores = {}

      #we are finding the matching scores of student ability ,personality ,intrest with the stream vectors int that also we have the ideal probable ability , personality ,intrest vector 
      for stream , profile in STREAM_PROFILES.items():
         stream_ability = np.array(profile["academic"]).reshape(1,-1)
         stream_personality = np.array(profile["personality"]).reshape(1,-1)
         stream_intrest = np.array(profile["interest"]).reshape(1,-1)

         stream_academic_similarity = cosine_similarity(ability_student,stream_ability)[0][0]
         stream_personality_similarity = cosine_similarity(riasec_student,stream_personality)[0][0]
         stream_interest_similarity = cosine_similarity(intrest_student,stream_intrest)[0][0]

         scores[f"{stream}"] = float(
                  (stream_academic_similarity*0.5)+
                  (stream_personality_similarity*0.3)+
                  (stream_interest_similarity*0.2)
         )
         best_stream = max(scores, key=scores.get)
         confidence_level = f"{round(scores[best_stream]*100,2)}%"
         session["best_stream"] = best_stream
         session["confidence_level"] = confidence_level
         session["scores"] = scores

      print(f"Ability Vector :- {ability_student} \nRIASSEC Vector :- {riasec_student} \nIntrest Vector :- {intrest_student}\n Score : - {scores}")
      return render_template("generate_career_profile.html",best_stream=best_stream,scores=scores,confidence_level=confidence_level)
      # return f"Ability Vector :- {ability_student} \nRIASSEC Vector :- {riasec_student} \nIntrest Vector :- {intrest_student} \n Score : - {score}"
      # return render_template("generate_career_profile.html")


def inference(prompt):
    print("Thinking ......")
    r = requests.post("http://localhost:11434/api/generate",json={
            "model":"llama3.2",
            "prompt":prompt,
            "stream":False

        })
    response = r.json()
    return response

@app.route("/career_roadmap")
def career_roadmap():

   prompt = f'''You are an AI Career Guidance Expert.\nYou do not change the predicted stream.\nYou do not override the scoring engine.\nYou only explain and expand on the recommendation.\nYou provide structured, practical, realistic guidance.\nYou never force the student to choose a stream.\nYou suggest, justify, and provide roadmap steps \n Student Profile Data:

   Best Recommended Stream: { session.get("best_stream") }
   Confidence Level: { session.get("confidence_level") }

   All Stream Scores:
   Science: { session.get("scores")["Science"] }
   Commerce: { session.get("scores")["Commerce"] }
   Arts: { session.get("scores")["Arts"] }

   Academic Strength Vector (0-1 scale):
   Math: { session.get("student_vector")["Math"] }
   Science: { session.get("student_vector")["Science"] }
   Social Science: { session.get("student_vector")["Social"] }
   Language: {session.get("student_vector")["Language"] }

   RIASEC Personality Scores (0-1 scale):
   Realistic: { session.get("riasec_vector")["R"] }
   Investigative: { session.get("riasec_vector")["I"] }
   Artistic: { session.get("riasec_vector")["A"] }
   Social: { session.get("riasec_vector")["S"] }
   Enterprising: { session.get("riasec_vector")["E"] }
   Conventional: { session.get("riasec_vector")["C"] }

   Interest Scores (0-1 scale):
   Mathematics: { session.get("intrest_vector")["Math"] }
   Science: { session.get("intrest_vector")["Science"] }
   Business: { session.get("intrest_vector")["Business"] }
   Creative: { session.get("intrest_vector")["Creativity"] }
   Social: { session.get("intrest_vector")["Social"] }


   Instructions:

   1. Explain why the recommended stream is suitable based on academic strengths, personality, and interests.
   2. Mention the second-best stream and explain briefly why it is also a possible option.
   3. Provide a 3-year roadmap (11th, 12th, Entrance Exams preparation).
   4. Suggest 5 career options after graduation.
   5. Suggest skill improvement areas based on weaker dimensions.
   6. Keep tone encouraging and practical.
   7. Do not contradict the predicted stream.
   8. Format response in clear sections with headings. 
   so that i can show in the web page in a structured format. every point should be in different section with heading.'''
   
   with open("career_roadmap_prompt.md","w") as f:
      f.write(prompt)

   response = inference(prompt)["response"]

   
   with open("response.txt","w") as f:
      f.write(response)
   return render_template("career_roadmap.html",response=response)




@app.route("/Idont_agree")
def retake_assessment():
   
    return redirect(url_for("assessment"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/register")

app.run()
