#!venv/Scripts/python

import os, random
from string import capwords

import sys, traceback
import logging
logging.basicConfig(filename='birdquiz.log',level=logging.DEBUG)

def allImages(picDir, acceptedExtensions = [".ppm", ".jpg", ".jpeg", ".png"]):
    '''
    Returns a list of all images in picDir with acceptedExtensions.
    picDir: directory of images
    acceptedExtensions: list of file extensions accepted:
        defaulted to [".ppm", ".jpg", ".jpeg", ".png"]
    '''
    infiles = [f for f in os.listdir(picDir) if os.path.isfile(picDir+f)]
    outfiles = []
    for file in infiles:
        filename, file_extension = os.path.splitext(file)
        if file_extension.lower() in acceptedExtensions:
            outfiles.append(file)
    return outfiles

def birdPhotos(imagelist, alphacodes2NamesDict):
    '''
    Returns a list of the images in imagelist that have a bird alphacode as 
    the four first letters: eg. "NOCA1.jpg"(Northern Cardinal) 
    imagelist: list of photos; preferably from allImages().
    alphacodes2NamesDict: dictionary mapping from bird alphacodes to bird names
    '''
    return [image for image in imagelist if image[0:4] in alphacodes2NamesDict]
    
def birdPhotos2(imagelist, alphacodes2NamesDict):
    '''
    Returns a dictionary mapping from alphacodes to a list of photos with that alphacode.
    '''
    photosDict = {}
    for image in imagelist:
        code = image[0:4]
        if code in alphacodes2NamesDict:
            if code in photosDict:
                photosDict[code].append(image)
            else:
                photosDict[code] = [image]
    return photosDict
    
def birdPhotosDict(picDir, codes2PlainNames, names2Codes):
    acceptedExtensions = [".ppm", ".jpg", ".jpeg", ".png"]
    photosDict = dict()
    for subdir, dirs, files in os.walk(picDir):
        
        
        for file in files:
            filename, file_extension = os.path.splitext(file)
            
            if file_extension.lower() not in acceptedExtensions:
                logging.info("The file {} does not have the right file extension. Accepted extensions are: {}.".format(file, acceptedExtensions))
                continue #Skips files that are not in the acceptedExtensions list
                
            simpleDir = subdir[subdir.find("photos/")+7:]#.strip("/home2/crgood/birdquiz.craigood.com/cgi-bin/app/static/")
            #logging.info(simpleDir)
            filePath = "{}/{}".format(simpleDir, file)
            
            code = getCodefromImageName(filename, codes2PlainNames, names2Codes)
            if code: #The image name must contain bird ID
                #logging.debug(filePath)
                if code in photosDict:
                    photosDict[code].append(filePath)
                else:
                    photosDict[code] = [filePath]
            else:
                logging.error('The file "{}" does not contain a bird name or alphacode, or it is not recognized.'.format(filePath))
    return photosDict
    
def getCodefromImageName(filename, codes2PlainNames, names2Codes):
    '''Returns the alphacode of the bird described in the image name:
    False if no name or wrong name exists'''
    #Grabs bird codes/names from images
    alphacodeName = [names2Codes[name] for name in names2Codes if (name.replace("'","").replace(" ","") in filename.lower() and name != "ou")] #Alphacode if filename includes the full bird name
    alphacode = [code for code in codes2PlainNames if (code.lower() in filename.lower() and code != "ou")] #Alphacode if filename only include the alphacode

    if alphacodeName or alphacode: #Makes sure the filename did include a bird name or code
        #logging.info(alphacodeName+["   "]+alphacode)
        code = (alphacodeName+alphacode)[0] #Grabs either the code derived from the name or the actual alphacode with preference for the code derived from a name. This is to prevent oddities like "Snowy Plover" and "Snowy Owl" both returning "SNOW"(Snowy Owl)
        return code
    else:
        return False

    
def getRandomImage(photoDict):
    '''
    Returns a random image to use in the quiz from photoDict.
    photoDict: dictionary mapping from alphacodes to a list of photos with that alphacode.
    '''
    code = random.choice(list(photoDict.keys()))
    photos = random.choice(photoDict[code])
    print(photos)
    return random.choice(photos) 
    
def removeCodeImage(image, photoDict):
    """
    Deletes the list of images from photoDict with the alphacode as image
    """
    #logging.debug("TEst 1")
    alphacode = image[0:4]
    #logging.debug("TEst 2")
    photoDict.pop(alphacode, None)
    return photoDict    
    
def setRandomImage(dbQuiz, photographers= {"dg": "Darrell Good", "tg":"Tom Grey"}):
    '''
    dbQuiz: database object Quiz for storing variables
    sets dbQuiz.currentImage to a random image, and removes all images of that
    bird from the available Photos Dictionary.
    '''
    
    code = random.choice(list(dbQuiz.availablePhotosDict.keys()))
    dbQuiz.currentImage = random.choice(dbQuiz.availablePhotosDict[code])
    # Makes a new dictionary without the list of images with the same alphacode
    dbQuiz.availablePhotosDict = {imageList: 
    dbQuiz.availablePhotosDict[imageList] for imageList in 
    dbQuiz.availablePhotosDict if imageList != code}
    
    dbQuiz.photographer = getPhotographer(dbQuiz.currentImage, choices = photographers) # Set photographer for this image, so that the copyright works
    #logging.info(dbQuiz.availablePhotosDict)

def getPhotographerOld(image, choices = {"dg": "Darrell Good"}):
    #logging.info(image)
    withoutNum = ''.join(l for l in image if not l.isdigit())
    #logging.info(withoutNum)
    initials = withoutNum.split(".")[0][4:] # Remove file extension from end and alphacode from beginning.
    #logging.info(initials)
    if initials in choices:
        return choices[initials]
    return "Undefined"

def getPhotographer(image, choices):
    #logging.info(image)
    return image.split("/")[0].replace("_", " ")
    
def buildAlphaCodeDict(file, reverse = False, noHyphens = False, lowercase = False):
    '''
    Builds dictionary from code to bird name.
    file: a .txt file containing bird names, alphacodes, and other info
        in that order and separated by double spaces.
    reverse: Flips dictionary so that it maps from name to code.
    noHyphens: Removes hyphens from name. Useful if you don't want the user to
        have to type them in.
    lowercase: Lowercases name.
    
    '''
    codes = dict()
    fin = open(file)
    for rawline in fin:
        line = rawline.strip()
        words = line.split('  ')
        if noHyphens == True:
            words[0]= words[0].replace('-',' ')
        if line.startswith('#') or line.startswith('+'):
            pass
        elif reverse == False:
            if lowercase == True: 
                codes[words[1]] = words[0].lower()
            else:
                codes[words[1]] = words[0]
        elif reverse == True:
            if lowercase == True: 
                codes[words[0].lower()] = words[1]
            else:
                codes[words[0]] = words[1]
            
    return codes
            
def buildRequiredAlphaCodeDicts(DataDir):
    '''
    Creates and returns a dictionary of the alphacode dictionaries necessary to run the quiz 
    DataDir: directory to a .txt file containing bird names, alphacodes, and other info
        in that order and separated by double spaces.
    
    returns: alphacodes: {"codes2FormalNames": codes2FormalNames, "codes2PlainNames": codes2PlainNames, "names2Codes":names2Codes}
    '''
    
    codes2FormalNames = buildAlphaCodeDict(DataDir) # Bird Alphacodes to name dictionary
    codes2PlainNames = buildAlphaCodeDict(DataDir,
        noHyphens = True, lowercase = True) # Bird Alphacodes to name dictionary lowercased and with hyphens removed
    names2Codes = buildAlphaCodeDict(DataDir,
        noHyphens = True, lowercase = True, reverse = True) # Bird name to alphacode dictionary lowercased and with hyphens removed
    alphacodes = {"codes2FormalNames": codes2FormalNames, "codes2PlainNames": codes2PlainNames,
        "names2Codes":names2Codes}  
    return alphacodes       
            
def Images2Str(path, imageList):
    ''' 
    Deprecated:
    Returns concatenated path+images into a string separated by semicolons
    in the format: "C\pics\image1.jpg;C\pics\image2.jpg;C\pics\image3.jpg"
    path: the path to the images
    imageList: List of image names as strings: 
    '''
    outStr = ""
    for image in imageList:
        if len(outStr) == 0:
            outStr = "{0}{1}".format(path, image)
        else:
            outStr = "{2};{0}{1}".format(path, image, outStr)
            
    return outStr

def Str2Images(imageStr):
    '''
    Deprecated:
    Splits imageStr into a list of images:
    imageStr: A string comprised of images separated by semicolons
        eg. "C\pics\image1.jpg;C\pics\image2.jpg;C\pics\image3.jpg"
    '''
    images = imageStr.split(";")
    return images
    
class analyzeEntry():
    pass

def arePartial(str1, str2):
    ls1 = str1.split(" ")
    ls2 = str2.split(" ")
    return areSimilar(ls1, ls2, 0)

def areSimilar(str1, str2, variance = 1):
    if abs(len(str1) - len(str2)) <= 1:
        if check(str1, str2, variance) or check(str2, str1, variance):
            return True
    else:
        return False
        
def check(str1, str2, variance = 1):
    x = 0
    for let in str1:
        if let not in str2:
            x += 1
    if x > variance:
        return False
    return True

def isBird(rstr, listOfBirds):
    for bird in listOfBirds:
        bird = bird.lower()
        if rstr == bird.split(" ")[-1] and len(rstr) >= 4 and rstr.lower() != "bird":
            return True
    return False

def isLastWord(string1, string2):
    if string1 == "":
        return False
    elif string1 == string2.split(" ")[-1]:
        return True
    return False

def isFirstWord(string1, string2):
    if string1 == "":
        return False
    elif string1 == string2.split(" ")[0]:
        return True
    return False
        
def modifyStr(rawstr):
    rawstr = rawstr.lower()
    rawstr = rawstr.replace("-", " ")
    return rawstr


        
def checkAnswer(guess, dbQuiz, codes2PlainNames, codes2FormalNames, names2Codes):
    """
    Checks the given guess to see if it is correct, adds the appropriate
    points to dbQuiz.score and returns text feedback.
    
    guess: the users gues at the current birds name or code.
    dbQuiz: database object Quiz for storing variables
    codes2PlainNames: dictionary mapping from bird alphacodes to simplified
        names. eg. "blue winged warbler" instead of "Blue-winged Warbler"
    codes2FormalNames: dictionary mapping from bird alphacodes to complete names
    """
    
    correctCode = getCodefromImageName(dbQuiz.currentImage, codes2PlainNames, names2Codes)#[0:4]
    #logging.info(correctCode)
    correctAnswer = codes2PlainNames[correctCode].lower()
    formalCorrect = codes2FormalNames[correctCode]
    mGuess = modifyStr(guess)
    youreRight = "You're right! {0} ({1}) is the correct answer." \
                 .format(formalCorrect, correctCode)
    
    youreCloseHalf = """You're almost right! The correct answer was {0} ({1}),\
 but your answer of "{2}" was close enough to get half credit.""" \
.format(formalCorrect, correctCode, guess)
    
    youreCloseFull = """You're really close! The correct answer was {0} ({1}),\
 but your answer of "{2}" was close enough to get full credit."""\
.format(formalCorrect, correctCode, guess)
    
    if mGuess == correctAnswer: 
        dbQuiz.score += 1
        return youreRight
    elif mGuess == correctCode.lower():
        dbQuiz.score += 1
        return youreRight
        
    elif mGuess == "bird":  #Some people....
        return "It is a bird. More precisely, it is a {0} ({1}). Please try to be more specific next time.".format(formalCorrect, correctCode)
        
    elif isLastWord(mGuess, correctAnswer):
        dbQuiz.score += 0.5
        return """Yes, the bird was a {}, \
a {}. You get half credit.""".format(mGuess.capitalize(), formalCorrect)
    elif isFirstWord(mGuess, correctAnswer):
        dbQuiz.score += 1
        return youreCloseFull
    elif mGuess in names2Codes:
        dbQuiz.score += 0
        return "".join(["No. ", capwords(mGuess), " (",
                                   names2Codes[mGuess],
                                   ") is not right. The correct answer was ",
                                   formalCorrect, " (", correctCode, ")"])
    elif areSimilar(mGuess, correctAnswer):
        dbQuiz.score += 1
        return youreCloseFull
    elif arePartial(mGuess, correctAnswer):
        dbQuiz.score += 0.5
        return youreCloseHalf
    elif mGuess in correctAnswer and len(mGuess) > 3:
        dbQuiz.score += 0.5
        return youreCloseHalf
    elif isBird(mGuess, names2Codes):
        dbQuiz.score += 0
        return "".join(["No. The bird was not a ",capwords(mGuess),
                                   ". It was a ", formalCorrect,
                                   " (", correctCode, ")"])
    elif mGuess.upper() in codes2PlainNames:
        code = mGuess.upper()
        dbQuiz.score += 0
        return "".join(["No. ", codes2FormalNames[code],
                                   " (", code,
                                   ") is not right. The correct answer was ",
                                   formalCorrect, " (", correctCode, ")"])
    
    elif dbQuiz.retry == True:    # If the user has already tried at this bird then
                                # it goes to the next question.
        return '''Sorry. The name "{0}" is not valid. The correct answer was 
        {1} ({2}).'''.format(guess, formalCorrect, correctCode)

    elif dbQuiz.retry == False:
        return False
    
    else: 
        return "Error: Entry not recognized, but exception not caught."
        
def generateFinalMessage(correctQuestions, totalQuestions):
    '''
    Generates a message based on the score
    totalQuestions: The total number of questions in the quiz
    correctQuestions: The number of questions answered correctly
    '''
    pCorrect = round((correctQuestions/totalQuestions) * 100, 1)
    #root.txtBox.write(text = "Congratulations!")
    if pCorrect == 100:
        return "Amazing! You got {2} out of {1} ({0}%) right!".format(pCorrect,
        totalQuestions, correctQuestions)
    elif pCorrect >= 75:
        return "Nice job! You got {2} out of {1} ({0}%) right!".format(
        pCorrect, totalQuestions, correctQuestions)
    elif pCorrect >= 50:
        return "You got {2} out of {1} ({0}%) right. That's a pretty good \
score!".format(pCorrect, totalQuestions, correctQuestions)
    elif pCorrect < 50:
        return "You got {2} out of {1} ({0}%). \
Please play again!".format(pCorrect,
 totalQuestions, correctQuestions)