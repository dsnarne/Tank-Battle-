from cmu_graphics import *
import math

def onAppStart(app):
    app.width = 750
    app.height = 500
    app.backgroundImagePath = '/Users/dhirennarne/Desktop/Src/Images/background.jpeg'
    
    # Tank properties
    app.tankX = app.width / 4
    app.tankY = app.height / 2
    app.tankWidth = 50
    app.tankHeight = 40
    app.tankColor = 'green'
    app.turretColor = 'lightgreen'
    app.turretRadius = 15
    app.tankSpeed = 5
    app.tankAngle = 0  # Angle in radians for tank rotation

    # Cannon properties
    app.cannonWidth = 30
    app.cannonHeight = 10
    app.cannonAngle = 0 
    
    # Wall properties
    app.walls = [
      [100, 100, 200, 20],  # Wall 1
      [400, 200, 20, 150],  # Wall 2
      [600, 300, 100, 20],  # Wall 3
      [250, 400, 300, 20],  # Wall 4
    ]

def redrawAll(app):
    drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height)
    
    # Draw the tank with rotation
    drawTank(app)

    # Draw walls
    for wall in app.walls:
        drawRect(wall[0], wall[1], wall[2], wall[3], fill='bisque', border='burlyWood', borderWidth=3)

def drawTank(app):
    centerX = app.tankX + app.tankWidth / 2
    centerY = app.tankY + app.tankHeight / 2

    # Calculate tank corners based on rotation
    halfWidth = app.tankWidth / 2
    halfHeight = app.tankHeight / 2
    angle = app.tankAngle

    corners = [
        (centerX + math.cos(angle) * halfWidth - math.sin(angle) * halfHeight,
         centerY + math.sin(angle) * halfWidth + math.cos(angle) * halfHeight),
        (centerX + math.cos(angle) * halfWidth + math.sin(angle) * halfHeight,
         centerY + math.sin(angle) * halfWidth - math.cos(angle) * halfHeight),
        (centerX - math.cos(angle) * halfWidth + math.sin(angle) * halfHeight,
         centerY - math.sin(angle) * halfWidth - math.cos(angle) * halfHeight),
        (centerX - math.cos(angle) * halfWidth - math.sin(angle) * halfHeight,
         centerY - math.sin(angle) * halfWidth + math.cos(angle) * halfHeight),
    ]

    # Draw tank body as a rotated rectangle
    drawPolygon(corners[0][0], corners[0][1],
                corners[1][0], corners[1][1],
                corners[2][0], corners[2][1],
                corners[3][0], corners[3][1],
                fill=app.tankColor, border='black')

    # Draw the turret
    drawCircle(centerX, centerY, app.turretRadius, fill=app.turretColor, border='black')

    # Draw the cannon
    drawCannon(app, centerX, centerY)

def drawCannon(app, centerX, centerY):
    angle = app.cannonAngle
    halfHeight = app.cannonHeight / 2

    # Start of cannon connected to the circle's edge
    startX = centerX + math.cos(angle) * app.turretRadius
    startY = centerY + math.sin(angle) * app.turretRadius

    # Corners relative to the cannon's rotation
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
    dx, dy = 0, 0  # Movement vector

    if 'w' in keys: 
        dy -= app.tankSpeed
    if 's' in keys: 
        dy += app.tankSpeed
    if 'a' in keys: 
        dx -= app.tankSpeed
    if 'd' in keys: 
        dx += app.tankSpeed

    if dx != 0 or dy != 0:  # Only update angle if there is movement
        app.tankAngle = math.atan2(dy, dx)

    # New position after movement
    newX = app.tankX + dx
    newY = app.tankY + dy

    # Check collision
    if not checkCollision(app, newX, newY):
        app.tankX, app.tankY = newX, newY

    # Keep the tank within the boundaries of the screen
    app.tankX = max(0, min(app.width - app.tankWidth, app.tankX))
    app.tankY = max(0, min(app.height - app.tankHeight, app.tankY))

def checkCollision(app, newX, newY):
    for wall in app.walls:
        wallX, wallY, wallW, wallH = wall
        if (newX < wallX + wallW and newX + app.tankWidth > wallX and
            newY < wallY + wallH and newY + app.tankHeight > wallY):
            return True
    return False

def onMouseMove(app, mouseX, mouseY):
    # Calculate angle between turret center and mouse
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    dx = mouseX - turretCenterX
    dy = mouseY - turretCenterY
    app.cannonAngle = math.atan2(dy, dx)  # Finds angle using arctan

def main():
    runApp(width=750, height=500)

main()
