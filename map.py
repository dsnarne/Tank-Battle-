import math
import random
import time 
from cmu_graphics import *

def onAppStart(app):
    app.width = 750
    app.height = 500
    app.backgroundImagePath = '/Users/dhirennarne/Desktop/Src/Images/background.jpeg' #if file path not working comment out line 44
    
    #Tank properties
    app.tankX = app.width / 4
    app.tankY = app.height / 2
    app.tankWidth = 50
    app.tankHeight = 40
    app.tankColor = 'green'
    app.turretColor = 'lightgreen'
    app.turretRadius = 15
    app.tankSpeed = 5
    app.tankAngle = 0  #Angle in radians for tank rotation
    
    #Enemy tank properties
    app.enemyTankX = app.width * 3 / 4
    app.enemyTankY = app.height / 2
    app.enemyTankWidth = 50
    app.enemyTankHeight = 40
    app.enemyTankColor = 'red'
    app.enemyTurretColor = 'darkred'
    app.enemyTurretRadius = 15
    app.enemyTankSpeed = 3
    app.enemyTankAngle = 0
    app.enemyLastShotTime = 0
    

    #Cannon properties
    app.cannonWidth = 30
    app.cannonHeight = 10
    app.cannonAngle = 0 

    #Wall properties
    app.walls = [
      [100, 100, 200, 20],  # Wall 1
      [400, 200, 20, 150],  # Wall 2
      [600, 300, 100, 20],  # Wall 3
      [250, 400, 300, 20],  # Wall 4
    ]

    #Projectiles
    app.projectiles = []
    app.lastShotTime = 0 
    
    app.recticleRadius = 10
    app.mouseX = 0
    app.mouseY = 0

def redrawAll(app):
    drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height) #if file path not working comment this out
    
    drawTank(app)
    
    drawEnemyTank(app)

    for projectile in app.projectiles:
        drawCircle(projectile['x'], projectile['y'], projectile['radius'], fill='black')

    for wall in app.walls:
        drawRect(wall[0], wall[1], wall[2], wall[3], fill='bisque', border='burlyWood', borderWidth=3)

    drawCircle(app.mouseX, app.mouseY, app.recticleRadius, fill='red')

def drawTank(app):
    centerX = app.tankX + app.tankWidth / 2
    centerY = app.tankY + app.tankHeight / 2

    #Calculate tank corners based on rotation
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

    #Draw tank body as a rotated rectangle
    drawPolygon(corners[0][0], corners[0][1],
                corners[1][0], corners[1][1],
                corners[2][0], corners[2][1],
                corners[3][0], corners[3][1],
                fill=app.tankColor, border='black')

    #Draw the turret
    drawCircle(centerX, centerY, app.turretRadius, fill=app.turretColor, border='black')

    #Draw the cannon
    drawCannon(app, centerX, centerY, 'lightgreen', True)

def drawCannon(app, centerX, centerY, color, isPlayer):
    
    if isPlayer:
      angle = app.cannonAngle  #Get the cannon's angle towards the mouse
      halfHeight = app.cannonHeight / 2
    else:
        dx = app.tankX - app.enemyTankX
        dy = app.tankY - app.enemyTankY
        angle = math.atan2(dy, dx)  # Calculate the angle to the player
        halfHeight = app.cannonHeight / 2

    #Start of cannon connected to the circle's edge (turret center)
    startX = centerX + math.cos(angle) * app.turretRadius
    startY = centerY + math.sin(angle) * app.turretRadius

    #Calculate the cannon's four corners relative to its rotation
    corners = [
        (startX + math.cos(angle) * app.cannonWidth - math.sin(angle) * halfHeight,
         startY + math.sin(angle) * app.cannonWidth + math.cos(angle) * halfHeight),
        (startX + math.cos(angle) * app.cannonWidth + math.sin(angle) * halfHeight,
         startY + math.sin(angle) * app.cannonWidth - math.cos(angle) * halfHeight),
        (startX - math.sin(angle) * halfHeight, startY + math.cos(angle) * halfHeight),
        (startX + math.sin(angle) * halfHeight, startY - math.cos(angle) * halfHeight)
    ]
    
    #Draw the cannon as rectangle rotated in the direction of the cannon angle
    drawPolygon(corners[0][0], corners[0][1],
                corners[1][0], corners[1][1],
                corners[3][0], corners[3][1],
                corners[2][0], corners[2][1],
                fill=color, border='black')

def drawEnemyTank(app):
    centerX = app.enemyTankX + app.enemyTankWidth / 2
    centerY = app.enemyTankY + app.enemyTankHeight / 2

    # Calculate tank corners based on rotation
    halfWidth = app.enemyTankWidth / 2
    halfHeight = app.enemyTankHeight / 2
    angle = app.enemyTankAngle

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

    # Draw enemy tank body as a rotated rectangle
    drawPolygon(corners[0][0], corners[0][1],
                corners[1][0], corners[1][1],
                corners[2][0], corners[2][1],
                corners[3][0], corners[3][1],
                fill=app.enemyTankColor, border='black')

    # Draw the turret
    drawCircle(centerX, centerY, app.enemyTurretRadius, fill=app.enemyTurretColor, border='black')

    # Draw the enemy cannon
    drawCannon(app, centerX, centerY, 'darkred', False)

def moveEnemyTank(app):
    # Calculate the angle between the enemy tank and the player tank
    dx = app.tankX - app.enemyTankX
    dy = app.tankY - app.enemyTankY
    app.enemyTankAngle = math.atan2(dy, dx)  #Angle to the player

    moveSpeed = app.enemyTankSpeed
    newX = app.enemyTankX + math.cos(app.enemyTankAngle) * moveSpeed
    newY = app.enemyTankY + math.sin(app.enemyTankAngle) * moveSpeed

    # Check if the enemy tank will collide with any wall at the new position
    if not checkTankCollision(app, newX, newY, app.enemyTankWidth, app.enemyTankHeight):
        app.enemyTankX = newX
        app.enemyTankY = newY

    #Keep the enemy tank inside the screen
    app.enemyTankX = max(0, min(app.width - app.enemyTankWidth, app.enemyTankX))
    app.enemyTankY = max(0, min(app.height - app.enemyTankHeight, app.enemyTankY))

def checkTankCollision(app, newX, newY, tankWidth, tankHeight):
    for wall in app.walls:
        wallX, wallY, wallW, wallH = wall

        #Check if the tank's new position will cause it to collide with a wall
        if (newX < wallX + wallW and newX + tankWidth > wallX and
            newY < wallY + wallH and newY + tankHeight > wallY):
            return True  

    return False 


def isPlayerVisible(app):
    enemyX = app.enemyTankX + app.enemyTankWidth / 2
    enemyY = app.enemyTankY + app.enemyTankHeight / 2
    playerX = app.tankX + app.tankWidth / 2
    playerY = app.tankY + app.tankHeight / 2

    for wall in app.walls:
        wallX, wallY, wallW, wallH = wall

        # Check if the line between the enemy and player intersects with any wall
        if lineIntersectsRect(enemyX, enemyY, playerX, playerY, wallX, wallY, wallW, wallH):
            return False  # Player is behind a wall

    return True  # Player is visible

def lineIntersectsRect(x1, y1, x2, y2, rx, ry, rw, rh):
    # Check for line intersection with a rectangle (basic algorithm)
    # This would require implementing line-rectangle intersection logic.
    # For simplicity, assume a basic check or library for geometric calculations is used here.
    pass

def enemyShoot(app):
    currentTime = time.time()

    # Check if 1/2 second has passed since last shot
    if currentTime - app.enemyLastShotTime < 0.5:
        return

    if isPlayerVisible(app):  # Only shoot if the player is visible
        app.enemyLastShotTime = currentTime

        # Spawn projectile toward the player
        startX = app.enemyTankX + app.enemyTankWidth / 2
        startY = app.enemyTankY + app.enemyTankHeight / 2
        angle = app.enemyTankAngle

        app.projectiles.append({
            'x': startX,
            'y': startY,
            'radius': 5,
            'angle': angle,
            'dx': math.cos(angle) * 10,
            'dy': math.sin(angle) * 10,
            'bounces': 0
        })


def onKeyHold(app, keys):
    dx, dy = 0, 0 #Movement vector

    if 'w' in keys: 
        dy -= app.tankSpeed
    if 's' in keys: 
        dy += app.tankSpeed
    if 'a' in keys: 
        dx -= app.tankSpeed
    if 'd' in keys: 
        dx += app.tankSpeed

    if dx != 0 or dy != 0: #Update angle if there is movement
        app.tankAngle = math.atan2(dy, dx)

    newX = app.tankX + dx
    newY = app.tankY + dy

    if not checkCollision(app, newX, newY):
        app.tankX, app.tankY = newX, newY

    #Keep the tank in screen
    app.tankX = max(0, min(app.width - app.tankWidth, app.tankX))
    app.tankY = max(0, min(app.height - app.tankHeight, app.tankY))
    
    if 'space' in keys:
        spawnProjectile(app)

def spawnProjectile(app):
    currentTime = time.time()

    #Check if 1/4 second passed since last shot
    if currentTime - app.lastShotTime < 0.25:
        return  

    app.lastShotTime = currentTime

    if len(app.projectiles) >= 5:
        return  #Don't spawn more than 5 projectiles

    #Calculate starting position of projectile at the turret's edge
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    startX = turretCenterX + math.cos(app.cannonAngle) * (app.turretRadius + 5)
    startY = turretCenterY + math.sin(app.cannonAngle) * (app.turretRadius + 5)

 
    angle = app.cannonAngle    #Cannon angle as the direction

    #Add projectiles to list
    app.projectiles.append({
        'x': startX,
        'y': startY,
        'radius': 5,
        'angle': angle,
        'dx': math.cos(angle) * 10, #Set dx and dy based on angle
        'dy': math.sin(angle) * 10,
        'bounces': 0  #Count bounces
    })


def checkCollision(app, newX, newY):
    for wall in app.walls:
        wallX, wallY, wallW, wallH = wall
        if (newX < wallX + wallW and newX + app.tankWidth > wallX and
            newY < wallY + wallH and newY + app.tankHeight > wallY):
            return True
    return False

def onMouseMove(app, mouseX, mouseY):
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    dx = mouseX - turretCenterX  # Difference between mouse and turret center X
    dy = mouseY - turretCenterY  # Difference between mouse and turret center Y
    app.cannonAngle = math.atan2(dy, dx)  # Get the angle using arctan2 function
    app.mouseX = mouseX  # Store the mouse position
    app.mouseY = mouseY  # Store the mouse position


def onStep(app):
    moveEnemyTank(app)
    enemyShoot(app)
    
    for projectile in list(app.projectiles):
        new_x = projectile['x'] + projectile['dx']
        new_y = projectile['y'] + projectile['dy']
        
        for wall in app.walls:
            wallX, wallY, wallW, wallH = wall

            #Check if projectile is colliding with a wall horizontally 
            if (wallX <= new_x <= wallX + wallW and
                wallY - projectile['radius'] <= new_y <= wallY + wallH + projectile['radius']):
                #Adjust the direction of the projectile after hitting the wall
                projectile['dy'] = -projectile['dy']
                projectile['bounces'] += 1
                new_y = projectile['y'] + projectile['dy']  # Correct the new position after bounce
                break 

            #Check if projectile is colliding with a wall vertically
            if (wallY <= new_y <= wallY + wallH and
                wallX - projectile['radius'] <= new_x <= wallX + wallW + projectile['radius']):
                #Adjust direction of the projectile after hitting the wall
                projectile['dx'] = -projectile['dx']
                projectile['bounces'] += 1
                new_x = projectile['x'] + projectile['dx']
                break 
              
        projectile['x'] = new_x
        projectile['y'] = new_y

        #Remove projectile if it bounces twice or off-screen
        if projectile['bounces'] >= 2:
            app.projectiles.remove(projectile)
            continue

        if (projectile['x'] < 0 or projectile['x'] > app.width or
            projectile['y'] < 0 or projectile['y'] > app.height):
          app.projectiles.remove(projectile)
 
def main():
    runApp(width=750, height=500)

main()
