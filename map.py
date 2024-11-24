from cmu_graphics import *

def onAppStart(app):
    app.width = 750
    app.height = 500
    
    # Path to the background image
    app.backgroundPath = '/Users/dhirennarne/Desktop/Src/Images/background.jpeg'

def redrawAll(app):
    # Draw the background image covering the entire canvas
    drawImage(app.backgroundPath, 0, 0, width=app.width, height=app.height)

def main():
    runApp(width=750, height=500)

main()
