#!venv/Scripts/python

from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange, Length
from app import DataHandler as DH
#from config import alphacodes

# def validate_bird(quizobj):
    # def _bird(form, field):
        # print("hello")

        # if DH.checkAnswer(field.data, self.quiz, alphacodes["codes2PlainNames"], alphacodes["codes2FormalNames"], alphacodes["names2Codes"]) == False:
            # raise validators.ValidationError("Your guess {} isn't a valid \
# bird name or code.".format(field.data))
    # return _bird
class GuessForm(Form):
    '''
    Form for getting the user's guess at a bird's name.
    '''
    guess = StringField('Bird Name', validators=[DataRequired()])
    # def __init__(self, quizobj, *args, **kwargs):
        # Form.__init__(self, *args, **kwargs)
        # self.quiz = quizobj
    
    # def _validate(form, field):
        # rv = Form.validate(self)
        # if not rv:
            # return False
        # print("hello")

        # if DH.checkAnswer(self.field.data, quizobj, alphacodes["codes2PlainNames"], alphacodes["codes2FormalNames"], alphacodes["names2Codes"]) == False:
            # raise validators.ValidationError("Your guess {} isn't a valid \
# bird name or code.".format(self.field.data))
class HomePageForm(Form):
    '''
    Form for setup at the start of the quiz
    '''
    # def __init__(self, lastQuiz, *args, **kwargs):
        # super(HomePageForm, self).__init__(*args, **kwargs)
    # def __init__(self, defaultUsername = "", defaultQuestions = None, *args, **kwargs):
        # Form.__init__(self, *args, **kwargs)
        # self.defaultUsername = defaultUsername
        # self.defaultQuestions = defaultQuestions
    
    username = StringField("User", validators=[DataRequired(), Length(max = 25, message = 
    "Nickname must be less than %(max)d characters")])
    
    numberOfQuestions = IntegerField("Number of Questions",
    validators= [NumberRange(min =1, max = 25)])
    
    #regions = MultiCheckboxField('Label', choices=[(1,"Northwest"), (2,"Northeast")])
    region1 = BooleanField('I accept the TOS', [validators.Required()], default = "checked")
    
class BlankForm(Form):
    ''' Form with no entries '''
    pass