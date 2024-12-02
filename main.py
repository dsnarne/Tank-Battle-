from cmu_graphics import *
import levels as lv
from PIL import Image

def onAppStart(app):
    print('hi')
    app.width = 750
    app.height = 500
    
    #start box
    app.boxWidth = 200
    app.boxHeight = 100
    app.startBoxX = (app.width - app.boxWidth) / 2  
    app.startBoxY = (app.height - app.boxHeight) / 2
    app.startBoxColor = 'blue'
    app.startTextColor = 'white'
    app.isStartHovering = False
    
    #controls box
    app.controlsBoxX = app.startBoxX
    app.controlsBoxY = app.startBoxY + app.boxHeight + 20
    app.controlsBoxColor = 'green'
    app.controlsTextColor = 'white'
    app.isControlsHovering = False
    
    app.isControlsPage = False
    
    app.backgroundImagePath = Image.open("Images/background.jpeg")
    app.backgroundImagePath = CMUImage(app.backgroundImagePath)

    app.isFlickerVisible = True  
    app.flickerTimer = 0
    
    app.screen = 'ui'  
    app.isGameStarted = False
    lv.onAppStart(app)

def redrawAll(app):
    if app.isGameStarted:
        lv.drawGame(app)
        return 
    
    drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height)
    
    if app.isControlsPage:
        #Draw the Controls page
        drawRect(0, 0, app.width, app.height, fill='white')  # Blank background
        drawLabel('CONTROLS', app.width / 2, 50, size=45, bold=True, fill='black')
        drawLabel('1. Use WASD to move.', app.width / 2, 150, size=30, fill='black')
        drawLabel('2. Aim your mouse and press space to shoot.', app.width / 2, 200, size=30, fill='black')
        drawLabel('3. Avoid enemy tanks and destroy the red tank!', app.width / 2, 250, size=30, fill='black')
        drawLabel('Press ESC to return to the main menu.', app.width / 2, 350, size=20, fill='red')
    else:
        drawLabel('Tank Battle!!!', app.width / 2, 100, size=100, bold=True, fill='black')
        
        if app.isFlickerVisible:
            drawLabel('PRESS START AND THE CHALLENGE BEGINS', 
                    app.width / 2, 175, size=30, fill='white', bold=True, border= 'black', borderWidth = 1)
        
        #start button
        drawRect(app.startBoxX, app.startBoxY, app.boxWidth, app.boxHeight, 
                fill=app.startBoxColor, border='black')
        drawLabel('START', app.startBoxX + app.boxWidth / 2, app.startBoxY + app.boxHeight / 2,
                size=50, bold=True, fill=app.startTextColor)
        
        #controls button
        drawRect(app.controlsBoxX, app.controlsBoxY, app.boxWidth, app.boxHeight, 
                fill=app.controlsBoxColor, border='black')
        drawLabel('CONTROLS', app.controlsBoxX + app.boxWidth / 2, 
                app.controlsBoxY + app.boxHeight / 2, size=35, bold=True, fill=app.controlsTextColor)

def onStep(app):
    app.flickerTimer += 1

    #every 33 steps change visibility
    if app.flickerTimer % 33 == 0:
        app.isFlickerVisible = not app.isFlickerVisible

def onMouseMove(app, mouseX, mouseY):
    #hover over start button
    if (app.startBoxX <= mouseX <= app.startBoxX + app.boxWidth and
        app.startBoxY <= mouseY <= app.startBoxY + app.boxHeight):
        app.isStartHovering = True
        app.startBoxColor = 'orange'
        app.startTextColor = 'black'
    else:
        app.isStartHovering = False
        app.startBoxColor = 'blue'
        app.startTextColor = 'white'

    #hover over controls button
    if (app.controlsBoxX <= mouseX <= app.controlsBoxX + app.boxWidth and
        app.controlsBoxY <= mouseY <= app.controlsBoxY + app.boxHeight):
        app.isControlsHovering = True
        app.controlsBoxColor = 'yellow'
        app.controlsTextColor = 'black'
    else:
        app.isControlsHovering = False
        app.controlsBoxColor = 'green'
        app.controlsTextColor = 'white'

def onMousePress(app, mouseX, mouseY):
    if not app.isControlsPage:
        if (app.controlsBoxX <= mouseX <= app.controlsBoxX + app.boxWidth and
            app.controlsBoxY <= mouseY <= app.controlsBoxY + app.boxHeight):
            app.isControlsPage = True
        elif (app.startBoxX <= mouseX <= app.startBoxX + app.boxWidth and
              app.startBoxY <= mouseY <= app.startBoxY + app.boxHeight):
            app.isGameStarted = True
            
            
    
            

def onKeyPress(app, key):
    if app.isGameStarted:
        lv.onKeyPress(app,key)
        return
    if app.isControlsPage and key == 'escape':
        app.isControlsPage = False

def onKeyHold(app, keys):
    if app.isGameStarted:
        lv.onKeyHold(app,keys)
        return
def onMouseMove(app, mouseX, mouseY):
    if app.isGameStarted:
        lv.onMouseMove(app, mouseX, mouseY)
        return
def onStep(app):
    if app.isGameStarted:
        lv.onStep(app)
        return

def main():
    runApp(width=750, height=500)

main()
