from cmu_graphics import *
import math

def onAppStart(app):
    app.width = 750
    app.height = 500
    app.backgroundImagePath = '/Users/dhirennarne/Desktop/Src/Images/background.jpeg'
    
    #Tank properties
    app.tankX = app.width / 2
    app.tankY = app.height / 2
    app.tankWidth = 50
    app.tankHeight = 30
    app.tankColor = 'green'
    app.turretColor = 'lightgreen'
    app.turretRadius = 15
    app.tankSpeed = 5  # Movement speed

    #Cannon properties
    app.cannonWidth = 40
    app.cannonHeight = 10
    app.cannonAngle = 0 

def redrawAll(app):
    drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height)
    
    drawRect(app.tankX, app.tankY, app.tankWidth, app.tankHeight, fill=app.tankColor, border='black')
    
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    drawCircle(turretCenterX, turretCenterY, app.turretRadius, fill=app.turretColor, border='black')
    
    drawCannon(app, turretCenterX, turretCenterY)

def drawCannon(app, centerX, centerY):
    angle = app.cannonAngle
    halfHeight = app.cannonHeight / 2
    
    #Start of cannon connected to the circle's edge)
    startX = centerX + math.cos(angle) * app.turretRadius
    startY = centerY + math.sin(angle) * app.turretRadius

    #Corners relative to the cannon's rotation
    corners = [
        (startX + math.cos(angle) * app.cannonWidth - math.sin(angle) * halfHeight,
         startY + math.sin(angle) * app.cannonWidth + math.cos(angle) * halfHeight),
        (startX + math.cos(angle) * app.cannonWidth + math.sin(angle) * halfHeight,
         startY + math.sin(angle) * app.cannonWidth - math.cos(angle) * halfHeight),
        (startX - math.sin(angle) * halfHeight, startY + math.cos(angle) * halfHeight),
        (startX + math.sin(angle) * halfHeight, startY - math.cos(angle) * halfHeight)
    ]
    
    # Draw cannon as a polygon
    drawPolygon(corners[0][0], corners[0][1],
                corners[1][0], corners[1][1],
                corners[3][0], corners[3][1],
                corners[2][0], corners[2][1],
                fill=app.turretColor, border='black')

def onKeyHold(app, keys):
    if 'w' in keys: 
        app.tankY -= app.tankSpeed
    if 's' in keys: 
        app.tankY += app.tankSpeed
    if 'a' in keys: 
        app.tankX -= app.tankSpeed
    if 'd' in keys: 
        app.tankX += app.tankSpeed
    
    #Keep tank within bounds
    app.tankX = max(0, min(app.width - app.tankWidth, app.tankX))
    app.tankY = max(0, min(app.height - app.tankHeight, app.tankY))

def onMouseMove(app, mouseX, mouseY):
    # Calculate angle between turret center and mouse
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    dx = mouseX - turretCenterX
    dy = mouseY - turretCenterY
    app.cannonAngle = math.atan2(dy, dx)

def main():
    runApp(width=750, height=500)

main()
