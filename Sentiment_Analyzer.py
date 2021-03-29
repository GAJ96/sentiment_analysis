from textblob import TextBlob
from newspaper import Article
from nltk import punkt
import PySimpleGUI as sg
#import keyboard

### The user interface:
title = "Sentiment Analyzr"

layout = [[sg.Text("Write your text directly into the box below, paste an url to an article on the internet, or open a file from your computer:"),],
          [sg.Text("(Note that the proper checkbox must be selected inorder for the program to work.)")],
          [sg.InputText(key = "-TEXT-")],
          [sg.Input(), sg.FileBrowse(key = "-TEXTFILE-")],
          [sg.Checkbox("Read text from file on computer", default = False, key = "-CHECKBOX_FILE-")],
          [sg.Checkbox("Read text from an URL", default = False, key = "-CHECKBOX_URL-")],
          [sg.Text("")],
          [sg.Button("Analyze")],
          [sg.Text("")],
          [sg.Text("This text is predominantly "), sg.Text(size = (15,1), key = "-SENTIMENT_TYPE-")],
          [sg.Text("The sentimentscore is "), sg.Text(size = (15,1), key = "-SENTIMENT_SCORE-")],
          [sg.Txt("(The value set of the sentiment score is given by [-1,1])")]]

margins = (100,100)

window = sg.Window(title = title, layout = layout, resizable = True, margins = margins)

### The program
while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED:      # Close the window if the X is pressed
        break

    if event == "Analyze":          # If Analyze is pressed:
        if values["-CHECKBOX_FILE-"] == True and values["-TEXTFILE-"] != "": # If it was chosen to analyze a textfile
            with open(values["-TEXTFILE-"], "r") as f:
                text = f.read()     # Store the textfile in text
        elif values["-CHECKBOX_URL-"] == True:          # If it was chosen to analyze an article on an url
            article = Article(values["-TEXT-"]) # Save the URL in article
            article.download()                          # Download the content of article...
            article.parse()                             # ...parse it...
            article.nlp()                               # ...and perform natural language processing.
            text = article.text
        else:
            text = values["-TEXT-"] # If the option to write ypur on text was cosen, store the inputed text in text

        blob = TextBlob(text)       # Make the textblod
        sentiment = blob.sentiment.polarity # Evaluate the sentiment score and save it in sentiment,
                                            # score between -1 to 1, where -1 is very negative and 1 is very positive
        window["-SENTIMENT_SCORE-"].update(sentiment) # Uppdate key -SENTIMENT_SCORE- with the value stored in sentiment

        # Define if the setiemnt is of type (very) positive, (very) negative or neutral.
        if sentiment > 0:
            if sentiment > 0.7:
                type = "very positive"
                #sg.theme("LightBlue")
            else:
                type = "positive"
        if sentiment == 0:
            type = "neutral"
        if sentiment < 0:
            if sentiment < -0.7:
                type = "very negative"
                #sg.theme("HotDogStand")
            else:
                type = "negative"

        window["-SENTIMENT_TYPE-"].update(type) # Snet the dentiment type to the user interface
