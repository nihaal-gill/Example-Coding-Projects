from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT, BOTTOM, TOP, RIGHT, SUNKEN
import random

class MathGame():
    def __init__(self):
        self.questionType = random.choice(['addition', 'subtraction', 'multiplication', 'division'])
        self.ans = 0
        self.numOfProblems = 0

    def getQuestion(self):
        currentQuestion = self.question()
        return currentQuestion

    def question(self):
        self.questionType = random.choice(['addition', 'subtraction', 'multiplication', 'division'])
        if (self.questionType == 'addition'):
            self.num1 = random.randint(0, 999)
            self.num2 = random.randint(0, 999)
            self.ans = self.num1 + self.num2
            self.numOfProblems += 1
            return '{} + {} ='.format(self.num1, self.num2)

        if (self.questionType == 'subtraction'):
            self.num1 = random.randint(0, 999)
            self.num2 = random.randint(0, 999)
            if (self.num2 > self.num1):
                self.num2, self.num1 = self.num1, self.num2
            self.ans = self.num1 - self.num2
            self.numOfProblems += 1
            return '{} - {} ='.format(self.num1, self.num2)

        if (self.questionType == 'multiplication'):
            self.num1 = random.randint(0, 99)
            self.num2 = random.randint(0, 99)
            self.ans = self.num1 * self.num2
            self.numOfProblems += 1
            return '{} * {} ='.format(self.num1, self.num2)
        if (self.questionType == 'division'):
            factorialList = []
            self.num1 = random.randint(0, 999)
            i = 1
            while i != self.num1:
                if (self.num1 % i) == 0:
                    factorialList.append(i)
                i += 1
            factorialList.append(self.num1)
            self.num2 = random.choice(factorialList)
            self.ans = self.num1 / self.num2
            self.numOfProblems += 1
            return '{} / {} ='.format(self.num1, self.num2)

    def getAns(self):
        self.ans = int(self.ans)
        return self.ans

    def getNumOfProblems(self):
        return self.numOfProblems

    def __str__(self):
        if (self.questionType == 'addition'):
            return '{} + {} ='.format(self.num1, self.num2)
        if (self.questionType == 'subtraction'):
            return '{} - {} ='.format(self.num1, self.num2)
        if (self.questionType == 'multiplication'):
            return '{} * {} ='.format(self.num1, self.num2)
        if (self.questionType == 'division'):
            return '{} / {} ='.format(self.num1, self.num2)

prevQuestion = None
def checkAns():
    global numOfCorrectAns, numOfIncorrectAns, numOfAttempts, incorrectAnsLabel, rootWindow, submitButton, q, prevQuestion

    if(q != prevQuestion):
        numOfAttempts += 1
        prevQuestion = q
    if(ansEntry.get() == None or ansEntry.get() == ''):
        feedBackLabel.configure(text='You have entered not entered a number.')
        userAns = None
    else:
        userAns = int(ansEntry.get())

    if (userAns == a):
        feedBackLabel.configure(text='Correct!')
        #increment number of correct answers by 1
        numOfCorrectAns += 1
        ansEntry.configure(state='disabled')
        submitButton.configure(state='disabled')
    else:
        feedBackLabel.configure(text='Incorrect, Try Again!')
        #increment number of incorrect answers by 1
        numOfIncorrectAns += 1
        ansEntry.delete(0, 'end')

    incorrectAnsLabel.configure(text='Number of Incorrect Answers: {}'.format(numOfIncorrectAns))
    ansEntry.delete(0,'end')

def newQuestion():
    global q,a, questionList, game, questionLabel,submitButton

    submitButton.configure(state='normal')
    ansEntry.configure(state='normal')
    ansEntry.delete(0, 'end')

    q = game.getQuestion()
    while (q in questionList):
        q = game.getQuestion()
    questionLabel.configure(text='Solve the Problem: \n {}'.format(q))
    questionList.append(q)
    a = game.getAns()
    #if you would like to see the answer for all the questions uncomment 'print(a)'
    #print(a)

def quit():
    global game, numOfAttempts
    rootWindow.destroy()
    #print number of problems (total)
    print("Number of problems attempted:", numOfAttempts)
    print("Number of problems solved:", numOfCorrectAns)
    print("Average number of incorrect answer attempts per problem: {0:.2f}".format(numOfIncorrectAns/numOfAttempts))

def createGui():
    global questionLabel, ansEntry, feedBackLabel, numOfIncorrectLabel, rootWindow, numOfProblems, numOfCorrectAns
    global numOfIncorrectAns, numOfAttempts, avgIncorrectAns, q, a, incorrectAnsLabel, questionList, game, entered_once
    global submitButton

    numOfAttempts = 0
    numOfCorrectAns = 0
    numOfIncorrectAns = 0
    questionList = []

    #create the rootWindow
    rootWindow = Tk()
    rootWindow.title("Play Math Game")

    #outputs the question onto the window
    game = MathGame()
    q = game.question()
    questionList.append(q)
    a = game.getAns()
    #print(a)
    questionFrame = Frame(rootWindow)
    questionFrame.pack()
    questionLabel = Label(questionFrame, text='Solve the Problem: \n {}'.format(q))
    questionLabel.pack()

    #text box for the answer input
    ansInputFrame = Frame(rootWindow)
    ansBox = Label(ansInputFrame, text='Answer:')
    ansEntry = Entry(ansInputFrame)
    ansInputFrame.pack(side=LEFT)
    ansBox.pack(side=LEFT)
    ansEntry.pack(side=LEFT)

    #submit button
    submitButton = Button(ansInputFrame, text='Submit', command=checkAns)
    submitButton.pack()

    #feedback Label
    feedBackFrame = Frame(rootWindow)
    feedBackLabel = Label(feedBackFrame)
    feedBackFrame.pack()
    feedBackLabel.pack(side=BOTTOM)

    #outputs the number of incorrect answers
    incorrectAnsFrame = Frame(rootWindow)
    incorrectAnsLabel = Label(incorrectAnsFrame)
    incorrectAnsFrame.pack()
    incorrectAnsLabel.pack()

    #new problem button
    newProblemButton = Button(rootWindow,text='New Problem',command=newQuestion)
    newProblemButton.pack(side=LEFT)
    newProblemButton.pack(side=BOTTOM)

    #quit button
    quitButton = Button(rootWindow,text='Quit',command=quit)
    quitButton.pack(side=BOTTOM)

def runGame():
    createGui()
    rootWindow.mainloop()


runGame()
