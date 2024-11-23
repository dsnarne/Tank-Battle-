from cmu_graphics import *

def onAppStart(app):
    app.width = 750
    app.height = 500
    
    #Starting screen box properties
    app.boxWidth = 200
    app.boxHeight = 100
    app.startBoxX = (app.width - app.boxWidth) / 2  
    app.startBoxY = (app.height - app.boxHeight) / 2
    app.startBoxColor = 'blue'
    app.startTextColor = 'white'
    app.isStartHovering = False
    
    app.controlsBoxX = app.startBoxX
    app.controlsBoxY = app.startBoxY + app.boxHeight + 20
    app.controlsBoxColor = 'green'
    app.controlsTextColor = 'white'
    app.isControlsHovering = False
    
    app.isControlsPage = False

def redrawAll(app):

    drawLabel('Tank Battle!!!', app.width / 2, 100, size=100, bold=True, fill='black')
    drawLabel('PRESS START AND THE CHALLENGE BEGINS', 
              app.width / 2, 175, size=20, fill='gray')
    
    #Start button
    drawRect(app.startBoxX, app.startBoxY, app.boxWidth, app.boxHeight, 
             fill=app.startBoxColor, border='black')
    drawLabel('START', app.startBoxX + app.boxWidth / 2, app.startBoxY + app.boxHeight / 2,
              size=50, bold=True, fill=app.startTextColor)
    
    #Controls button
    drawRect(app.controlsBoxX, app.controlsBoxY, app.boxWidth, app.boxHeight, 
             fill=app.controlsBoxColor, border='black')
    drawLabel('CONTROLS', app.controlsBoxX + app.boxWidth / 2, 
              app.controlsBoxY + app.boxHeight / 2, size=35, bold=True, fill=app.controlsTextColor)

def onMouseMove(app, mouseX, mouseY):
    #Start button
    if (app.startBoxX <= mouseX <= app.startBoxX + app.boxWidth and
        app.startBoxY <= mouseY <= app.startBoxY + app.boxHeight):
        app.isStartHovering = True
        app.startBoxColor = 'orange'
        app.startTextColor = 'black'
    else:
        app.isStartHovering = False
        app.startBoxColor = 'blue'
        app.startTextColor = 'white'

    #Controls button
    if (app.controlsBoxX <= mouseX <= app.controlsBoxX + app.boxWidth and
        app.controlsBoxY <= mouseY <= app.controlsBoxY + app.boxHeight):
        app.isControlsHovering = True
        app.controlsBoxColor = 'yellow'
        app.controlsTextColor = 'black'
    else:
        app.isControlsHovering = False
        app.controlsBoxColor = 'green'
        app.controlsTextColor = 'white'

def main():
    runApp(width=750, height=500)

main()
