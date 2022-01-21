from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def survey_page():
    """Main Survey Page with Survey title and instructions"""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("survey_page.html", title=title, instructions=instructions)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the Survey of responses."""

    responses = []

    return redirect("/questions/0")


@app.route('/questions/<int:question_id>')
def show_question(question_id):
    """Show questions with given integer id. and the total of questions in the Survey"""

    question = satisfaction_survey.questions[question_id]
    questions = satisfaction_survey.questions
    question_total = len(questions)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")

    if (len(responses) != question_id):
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")

    return render_template("survey_questions.html", question=question, question_id=question_id, question_total=question_total)


@app.route('/answer', methods=["POST"])
def handle_answer():
    """Save answers and proceed with Survey"""

    choice = request.form['answer']
    responses.append(choice)

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def survey_completetion():
    """Show Thank You page when Survey is completed."""

    return render_template("survey_completed.html")
