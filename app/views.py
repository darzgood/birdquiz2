#!venv/Scripts/python

from app import app, db, models, basedir
from app import DataHandler as DH
from flask import session, render_template, flash, redirect, url_for, request
from .forms import GuessForm, HomePageForm, BlankForm
import os, random, datetime


alphacodes = DH.buildRequiredAlphaCodeDicts(basedir+"/static/masterData2.txt")

import sys, traceback
import logging
logging.basicConfig(filename='birdquiz.log',level=logging.DEBUG)

@app.route('/')
def root():
    return redirect(url_for('setup'))

@app.route('/test2', methods=["GET", "POST"])
def test2():
    setupForm = HomePageForm()
    if setupForm.validate_on_submit():
        return redirect(url_for('test3'))
    flash("Test2")
    return render_template('setup.html', title = "Bird Quiz", form = setupForm)

@app.route('/test3', methods=["GET", "POST"])
def test3():
    setupForm = HomePageForm()
    if setupForm.validate_on_submit():
        return redirect(url_for('test2'))
    flash("Test3")
    return render_template('setup.html', title = "Bird Quiz", form = setupForm)


@app.route('/home', methods=['GET', 'POST'])
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    '''
    Build the setup page and commits most of the quiz variables to the
    data-base.
    '''
    if "quizID" in request.args: # if redirected a previous quiz, populates form with previous quiz's data
        quizID = request.args["quizID"]
        prevquiz = models.Quiz.query.get(quizID)
        setupForm = HomePageForm(username = prevquiz.username, numberOfQuestions = prevquiz.questionTotal, maxQuestions = 20)
    else:
        setupForm = HomePageForm()

    if setupForm.validate_on_submit():

        try:
            photoDir = basedir+"/static/photos/"
            #logging.info("testing photosDict")
            photosDict = DH.birdPhotosDict(photoDir, alphacodes["codes2PlainNames"], alphacodes["names2Codes"])
            #logging.info(photosDict)
        except:
            logging.info("Photos Failure")
            logging.error(traceback.format_exc())
            traceback.print_exc(file=open("birdquiz.log","a"))
            sys.exit()

        '''photoDir = basedir+"/static/photos/"
        photos = DH.birdPhotos(DH.allImages(photoDir), alphacodes["codes2PlainNames"])
        photosDict = DH.birdPhotos2(DH.allImages(photoDir), alphacodes["codes2PlainNames"])
        logging.debug("Old photosDict: ")
        logging.debug(photosDict)'''





        # currentImage = DH.getRandomImage(photosDict)
        # print(currentImage)
        #availablePhotosDict = DH. #Dictionary to hold photos of birds that have not been used yet.

        try:

            thisquiz = models.Quiz(
                username = setupForm.username.data,
                timestamp = datetime.datetime.utcnow(),
                questionTotal = setupForm.numberOfQuestions.data,
                questionComplete = 0,
                questionCorrect = 0,
                setupComplete = 1,
                allPhotosDict = photosDict, #Master dictionary to hold all photo data
                availablePhotosDict = photosDict, #Dictionary to hold photos of birds that have not been used yet.
                currentImage = None,
                photographer = None,
                retry = False,
                messages = ["Message Error: Please contact me if you see this message"])

            db.session.add(thisquiz)
            DH.setRandomImage(thisquiz, photographers = {"dg": "Darrell Good", "tg":"Tom Grey"})
            db.session.commit()



        except:
            logging.info("DB Failure")
            logging.error(traceback.format_exc())
            traceback.print_exc(file=open("birdquiz.log","a"))
            sys.exit()


        # session['basedir'] = os.path.abspath(os.path.dirname(__file__))
        # session['setup'] = True
        # session['username'] = setupForm.username.data
        # session['numberOfQuestions'] = setupForm.numberOfQuestions.data
        # ACD2 = buildAlphaCodeDict(session['basedir'] +
        # "/static/masterData2.txt", lowercase = False)
        # session['alphacodes'] = ACD
        # session['images'] = allImages(session['basedir']+"/static/photos/")
        return redirect(url_for('question', quizID = thisquiz.id))
    return render_template('setup.html', title = "Bird Quiz", form = setupForm)

@app.route('/question', methods=['GET', 'POST'])
def question():
    quizID = request.args["quizID"]
    quiz = models.Quiz.query.get(quizID)

    user = {'nickname': quiz.username}

    if quiz.questionComplete == quiz.questionTotal:
        userFile = open("users.log", "a")
        userFile.write("{0}  ID {4}({1}/{2} @{3})\n".format(quiz.username,
        quiz.questionCorrect, quiz.questionTotal, quiz.timestamp, quizID))
        userFile.close()

        finalMessage = DH.generateFinalMessage(quiz.score, quiz.questionTotal)
        #flash(finalMessage)
        quiz.messages = quiz.messages + [finalMessage]
        db.session.commit()
        #logging.info("Message: ")
        #logging.info(quiz.messages[-1:])
        return redirect(url_for('finish', quizID = quizID))


    guessForm = GuessForm()
    if guessForm.validate_on_submit():

        try:

            answerMessage = DH.checkAnswer(guessForm.guess.data, quiz,
            alphacodes["codes2PlainNames"], alphacodes["codes2FormalNames"],
            alphacodes["names2Codes"])

        except:
            logging.info("Quiz Failure")
            logging.error(traceback.format_exc())
            traceback.print_exc(file=open("birdquiz.log","a"))
            sys.exit()

        if answerMessage == False and quiz.retry == False:
            redoMessage = '''Sorry. I can't recognize the name "{}". Please try again.
            '''.format(guessForm.guess.data)
            #flash(redoMessage)
            quiz.messages = quiz.messages + [redoMessage]
            quiz.retry = True
            db.session.commit()
            return redirect(url_for('question', quizID = quizID))
        else:
            #logging.info(quiz.messages)
            quiz.messages = quiz.messages + [answerMessage]
            db.session.commit()
            #logging.info(quiz.messages)
            #flash(answerMessage)
            quiz.questionComplete += 1
            db.session.commit()
            return redirect(url_for('answer', quizID = quizID))
    db.session.commit()
    return render_template('question.html', title='Bird Quiz', user=user,
        photo="/static/photos/"+quiz.currentImage,
        form = guessForm, photographer = quiz.photographer,
        retry = quiz.retry, message = quiz.messages[-1])

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    quizID = request.args["quizID"]
    quiz = models.Quiz.query.get(quizID)

    user = {'nickname': quiz.username}

    answerForm = BlankForm()
    if answerForm.validate_on_submit():
        #logging.info(quiz.availablePhotosDict)


        quiz.retry = False
        #logging.info("Answer view test")
        DH.setRandomImage(quiz, photographers = {"dg": "Darrell Good", "tg":"Tom Grey"}) # Setting variables for next question
        db.session.commit()
        #logging.info(quiz.availablePhotosDict)
        return redirect(url_for('question', quizID = quizID))
    db.session.commit()

    try:
        return render_template('answer.html', title='Bird Quiz', user=user,
            photo="/static/photos/"+quiz.currentImage, form = answerForm,
            photographer = quiz.photographer, message = quiz.messages[-1],
            birdname = alphacodes["codes2FormalNames"][DH.getCodefromImageName(quiz.currentImage, alphacodes["codes2PlainNames"], alphacodes["names2Codes"])]) #TODO: Simplify this last statement by adding a "currentBirdCode" element to the database
    except:
        logging.info("Answer view Failure")
        logging.error(traceback.format_exc())
        traceback.print_exc(file=open("birdquiz.log","a"))
        sys.exit()

@app.route('/finsh', methods = ["GET", "POST"])
def finish():
    quizID = request.args["quizID"]
    quiz = models.Quiz.query.get(quizID)
    user = {'nickname': quiz.username}
    againForm = BlankForm()

    if againForm.validate_on_submit():
        return redirect(url_for('setup', quizID = quizID))
    return render_template("finish.html", title='Bird Quiz', user=user,
        photo="/static/photos/"+quiz.currentImage, form = againForm,
        finalbird = alphacodes["codes2FormalNames"][DH.getCodefromImageName(quiz.currentImage, alphacodes["codes2PlainNames"], alphacodes["names2Codes"])],
        photographer = quiz.photographer, message = quiz.messages[-1])

@app.route('/about', methods = ["GET", "POST"])
def about():
    try:
    	logging.info("testing")
    	with open('/static/about.txt', 'r') as aboutFile:
    		about=aboutFile.read()
    	return render_template("about.html", aboutText = about )

    except:
            logging.info("About Page Failure")
            logging.error(traceback.format_exc())
            traceback.print_exc(file=open("birdquiz.log","a"))
            sys.exit()


@app.route('/contact', methods = ["GET", "POST"])
def contact():
    try:
    	logging.info("testing")
    	return render_template("contact.html")

    except:
            logging.info("Contact Page Failure")
            logging.error(traceback.format_exc())
            traceback.print_exc(file=open("birdquiz.log","a"))
            sys.exit()


@app.route('/resources', methods = ["GET", "POST"])
def resources():
    try:
    	logging.info("testing")
    	return render_template("resources.html")

    except:
            logging.info("Resources Page Failure")
            logging.error(traceback.format_exc())
            traceback.print_exc(file=open("birdquiz.log","a"))
            sys.exit()
