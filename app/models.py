#!venv/Scripts/python

from app import db
from flask_sqlalchemy import orm
# class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), index=True, unique=True)
    # quizzes = db.relationship("QuizVars", backref = "user", lazy = "dynamic")
    # #scores = db.relationship("Score", backref = "user", lazy = "dynamic")
    
    # def __repr__(self):
        # return '<User {}>'.format(self.username)
        
# class QuizVars(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    # questionTotal = db.Column(db.Integer)
    # questionComplete = db.Column(db.Integer)
    # questionCorrect = db.Column(db.Integer)
    # images = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # #score = db.relationship("Score", backref = "user", lazy = "dynamic")
    
    # def __repr__(self):
        # return '<QuizVars {}>'.format(self.images)
        
# class Score(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    # timestamp = db.Column(db.DateTime)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # quiz_id = db.Column(db.Integer, db.ForeignKey('quizvars.id'))
    # score = db.Column(db.Float)
    
    # def __repr__(self):
        # return '<Score {}>'.format(self.score)
        
class Quiz(db.Model):
    '''
    Database model for storing quiz variables
    username: name of the person taking the quiz
    timestamp: date taken
    
    questionTotal: total number of questions in the quiz
    questionComplete: questions the user has completed
    questionCorrect: questions the user has gotten right
    score: synonym for questionCorrect
    setupComplete: variable for assuring that the user completes the setup page before continuing the quiz.
    allPhotosDict: Dict mapping from alphacode to list of images
    availablePhotosDict: Dict of unused images, mapping from from alphacode to list of images
    currentImage: the str of the current quiz image, excluding path 
    retry: variable for checking if the user has tried the question twice
    messages: pickled list for holding feedback messages
    
    deprecated:
    images: deprecated; string listing all available images: replaced with photos
    photos: pickletype list for all images available to quiz, replaced by allPhotosDict and availablePhotosDict
    currentBird: the name of the bird being displayed, replaced by currentImage
    
    '''
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime)
    #images = db.Column(db.Text)
    questionTotal = db.Column(db.Integer)
    questionComplete = db.Column(db.Integer)
    questionCorrect = db.Column(db.Float)
    score = orm.synonym("questionCorrect")
    setupComplete = db.Column(db.Integer)
    #photos = db.Column(db.PickleType) # List of photos: replaced by allPhotosDict and availablePhotosDict
    allPhotosDict = db.Column(db.PickleType)
    availablePhotosDict = db.Column(db.PickleType)
    #currentBird = db.Column(db.String(60)) # String of image name: replaced by currentImage
    currentImage = db.Column(db.String(60))
    photographer = db.Column(db.Text)
    retry = db.Column(db.Integer)
    messages = db.Column(db.PickleType)
    regions = db.Column(db.PickleType) # regions of the country to pull birds from
    habitats = db.Column(db.PickleType) # habitats to pull birds from
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User {}>'.format(self.username)    
