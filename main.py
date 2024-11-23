from cmu_graphics import *

def onAppStart(app):
    app.width = 750
    app.height = 500
    
    #Starting screen
    app.boxWidth = 200
    app.boxHeight = 100
    app.boxX = (app.width - app.boxWidth) / 2  # Center horizontally
    app.boxY = (app.height - app.boxHeight) / 2  # Center vertically
    app.boxColor = 'blue'
    app.textColor = 'white'
    app.isHovering = False

def redrawAll(app):
    drawLabel('Tank Battle!!!', app.width / 2, 100, size=100, bold=True, fill='black')
    drawLabel('PRESS START', 
              app.width / 2, 175, size=20, fill='gray')
    drawRect(app.boxX, app.boxY, app.boxWidth, app.boxHeight, fill=app.boxColor, border='black')
    drawLabel('START', app.boxX + app.boxWidth / 2, app.boxY + app.boxHeight / 2,
              size=50, bold=True, fill=app.textColor)

def onMouseMove(app, mouseX, mouseY):
    # Check if mouse is inside the box
    if (app.boxX <= mouseX <= app.boxX + app.boxWidth and
        app.boxY <= mouseY <= app.boxY + app.boxHeight):
        app.isHovering = True
        app.boxColor = 'orange'
        app.textColor = 'black'
    else:
        app.isHovering = False
        app.boxColor = 'blue'
        app.textColor = 'white'

def main():
    runApp(width=750, height=500)

main()
