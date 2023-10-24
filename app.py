
from flask import Flask, request, render_template, redirect,flash, session ,json,jsonify
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config['SECRET_KEY'] ="oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
from boggle import Boggle

boggle_game = Boggle()

@app.route("/")
def home_page():
 board = boggle_game.make_board()
 session["board"]=board
 print (board)
 return render_template("homepage.html",board =board)

@app.route("/validateWord",methods=["POST"])
def validate_word():
  board = session["board"]
  inputWord =json.loads(request.data)["word"]
  boggle_check =boggle_game.check_valid_word(board,inputWord)
  response = {"result":boggle_check}
  return jsonify(response)


@app.route("/statistics",methods=["POST"])
def statistics():
  print ("I am in stadisctics")
 
  if 'maxScore' in  session:
    seccionMaxScore = int(session["maxScore"])
    currentScore =int(json.loads(request.data)["currentScore"])
    print(f'currentScore {currentScore}')
    if currentScore>seccionMaxScore:
      session["maxScore"] =currentScore
  else:
    session["maxScore"] = 0

  if 'timesPlayed' in session:
    timesPlayed = int(session["timesPlayed"])
    timesPlayed += 1;
    session["timesPlayed"] = timesPlayed
  else:
    session["timesPlayed"] = 0

  maxScoreOutPut = session["maxScore"];
  timesPlayedOutPut = session["timesPlayed"];
  response ={"maxScore":maxScoreOutPut,"timesPlayed":timesPlayedOutPut }
  print (response)
  return jsonify(response)