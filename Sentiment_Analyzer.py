from textblob import TextBlob
import PySimpleGUI as sg
#import keyboard

title = "Sentiment Analyzr"

sg.theme("DarkTeal4")

layout = [[sg.Text("Paste your text directly into the box below or open a file from your computer:"),],
          [sg.Text("(Note that the checkbox must be selected inorder for the file to be analyzed.)")],
          [sg.InputText(key = "-TEXT-")],
          [sg.Input(), sg.FileBrowse(key = "-TEXTFILE-")],
          [sg.Checkbox("Add file from computer", default = False, key = "-CHECKBOX-")],
          [sg.Text("")],
          [sg.Button("Analyze")],
          [sg.Text("")],
          [sg.Text("This text is predominantly "), sg.Text(size = (15,1), key = "-SENTIMENT_TYPE-")],
          [sg.Text("The sentimentscore is "), sg.Text(size = (15,1), key = "-SENTIMENT_SCORE-")],
          [sg.Txt("(The value set of the sentiment score is given by [-1,1])")]]

margins = (100,100)

window = sg.Window(title = title, layout = layout, resizable = True, margins = margins)


while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED: # Close the window if the X is pressed
        break

    if event == "Analyze":      # If Analyze is pressed:
        if values["-CHECKBOX-"] == True: # If it was chosen to analyze a textfile
            with open(values["-TEXTFILE-"], "r") as f:
                text = f.read() # store the textfile in text
        else:
            text = values["-TEXT-"] # If the option to write ypur on text was cosen, store the inputed text in text

        blob = TextBlob(text)   # Make the textblod
        sentiment = blob.sentiment.polarity # Evaluate the sentiment score and save it in sentiment,
                                            # score between -1 to 1, where -1 is very negative and 1 is very positive
        window["-SENTIMENT_SCORE-"].update(sentiment) # Uppdate key -SENTIMENT_SCORE- with the value stored in sentiment

        if sentiment > 0:
            type = "positive"
        if sentiment == 0:
            type = "neutral"
        if sentiment < 0:
            type = "negative"

        window["-SENTIMENT_TYPE-"].update(type)
