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
    app.enemyTankSpeed = 1
    app.enemyTankAngle = 0
    app.enemyLastShotTime = 0
    
    app.cannonWidth = 30
    app.cannonHeight = 10
    app.cannonAngle = 0 

    app.walls = [
      [100, 100, 200, 20],  #Wall 1
      [400, 200, 20, 150],  #Wall 2
      [600, 300, 100, 20],  #Wall 3
      [250, 400, 300, 20],  #Wall 4
    ]

    app.projectiles = []
    app.lastShotTime = 0 
    app.recticleRadius = 10
    app.mouseX = 0
    app.mouseY = 0
    
    app.gameOver = False
    app.gameWon = False
    app.startTime = time.time()
    app.fastestTime = None

    
def redrawAll(app):
    drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height) #if file path not working comment this out
    
    
    if app.gameOver:
      if app.gameWon:
        drawLabel('YOU WIN!', app.width / 2, app.height / 2 - 40, size=40, bold=True, fill='green')
      else:
        drawLabel('GAME OVER', app.width / 2, app.height / 2 - 40, size=40, bold=True, fill='red')
        
      drawLabel(f'Press R to Restart', app.width / 2, app.height / 2, size=20, fill='white')
      if app.fastestTime:
          drawLabel(f'Fastest Time: {app.fastestTime:.2f} seconds', app.width / 2, app.height / 2 + 40, size=20, fill='yellow')
      return
      
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
        angle = math.atan2(dy, dx)  # Calculate the angle to the player tank
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

    #Calculate tank corners based on rotation
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

    #Draw enemy tank body as a rotated rectangle
    drawPolygon(corners[0][0], corners[0][1],
                corners[1][0], corners[1][1],
                corners[2][0], corners[2][1],
                corners[3][0], corners[3][1],
                fill=app.enemyTankColor, border='black')

    #Draw the turret
    drawCircle(centerX, centerY, app.enemyTurretRadius, fill=app.enemyTurretColor, border='black')

    #Draw the enemy cannon
    drawCannon(app, centerX, centerY, 'darkred', False)

def moveEnemyTank(app):
    #Calculate the angle between the enemy tank and the player tank
    dx = app.tankX - app.enemyTankX
    dy = app.tankY - app.enemyTankY
    app.enemyTankAngle = math.atan2(dy, dx)  #Angle to the player

    moveSpeed = app.enemyTankSpeed
    newX = app.enemyTankX + math.cos(app.enemyTankAngle) * moveSpeed
    newY = app.enemyTankY + math.sin(app.enemyTankAngle) * moveSpeed

    #Check if the enemy tank will collide with any wall at the new position
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

def checkProjectileCollisionWithPlayer(app):
    for projectile in app.projectiles:  
        if (
            app.tankX <= projectile['x'] <= app.tankX + app.tankWidth and
            app.tankY <= projectile['y'] <= app.tankY + app.tankHeight
        ):
            return True
    return False


def isPlayerVisible(app):
    enemyX = app.enemyTankX + app.enemyTankWidth / 2
    enemyY = app.enemyTankY + app.enemyTankHeight / 2
    playerX = app.tankX + app.tankWidth / 2
    playerY = app.tankY + app.tankHeight / 2

    for wall in app.walls:
        wallX, wallY, wallW, wallH = wall

        #Check if the line between the enemy and player intersects with any wall
        if lineIntersectsRect(enemyX, enemyY, playerX, playerY, wallX, wallY, wallW, wallH):
            return False  # Player is behind a wall

    return True  #Player is visible

def lineIntersectsRect(x1, y1, x2, y2, rx, ry, rw, rh):
  #work in progress used to make tank shoot only when player visible
    pass

def enemyShoot(app):
    currentTime = time.time()

    # Check if 1/2 second has passed since last shot
    if currentTime - app.enemyLastShotTime < 0.5:
        return

    if isPlayerVisible(app):  # Only shoot if the player is visible (WORK IN PROGRESS)
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
            'bounces': 0,
            'source': 'enemy'  # Indicate that this is an enemy projectile
        })


def onKeyPress(app, key):
  if app.gameOver and key == 'r':
    onAppStart(app)

def onKeyHold(app, keys):
    dx, dy = 0, 0

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

    # Check if 1/4 second passed since last shot
    if currentTime - app.lastShotTime < 0.25:
        return  

    app.lastShotTime = currentTime

    if len(app.projectiles) >= 5:
        return  # Don't spawn more than 5 projectiles

    # Calculate starting position of projectile at the turret's edge
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    startX = turretCenterX + math.cos(app.cannonAngle) * (app.turretRadius + 25)
    startY = turretCenterY + math.sin(app.cannonAngle) * (app.turretRadius + 25)

    angle = app.cannonAngle  # Cannon angle as the direction

    # Add projectiles to list
    app.projectiles.append({
        'x': startX,
        'y': startY,
        'radius': 5,
        'angle': angle,
        'dx': math.cos(angle) * 10,  # Set dx and dy based on angle
        'dy': math.sin(angle) * 10,
        'bounces': 0,  # Count bounces
        'source': 'player'  # Indicate that this is a player projectile
    })



def checkCollision(app, newX, newY):
    for wall in app.walls:
        wallX, wallY, wallW, wallH = wall
        if (newX < wallX + wallW and newX + app.tankWidth > wallX and
            newY < wallY + wallH and newY + app.tankHeight > wallY):
            return True
    return False

def checkTankCollisionWithPlayer(app):
  enemyCenterX = app.enemyTankX + app.enemyTankWidth / 2
  enemyCenterY = app.enemyTankY + app.enemyTankHeight / 2
  playerCenterX = app.tankX + app.tankWidth / 2
  playerCenterY = app.tankY + app.tankHeight / 2
  
  distance = math.sqrt((enemyCenterX - playerCenterX) ** 2 + (enemyCenterY - playerCenterY) ** 2)
  return distance < (app.tankWidth + app.enemyTankWidth) / 2

def checkProjectileCollisionWithEnemy(app):
    for projectile in app.projectiles:  
        if projectile['source'] == 'player':  # Only check player's projectiles
            enemyCenterX = app.enemyTankX + app.enemyTankWidth / 2
            enemyCenterY = app.enemyTankY + app.enemyTankHeight / 2
            
            if (enemyCenterX - app.enemyTankWidth / 2 <= projectile['x'] <= enemyCenterX + app.enemyTankWidth / 2 and
                enemyCenterY - app.enemyTankHeight / 2 <= projectile['y'] <= enemyCenterY + app.enemyTankHeight / 2):
                return True
    return False





def onMouseMove(app, mouseX, mouseY):
    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    dx = mouseX - turretCenterX  #Difference between mouse and turret center X
    dy = mouseY - turretCenterY  #Difference between mouse and turret center Y
    app.cannonAngle = math.atan2(dy, dx)  #Get the angle using arctan2 function
    app.mouseX = mouseX  
    app.mouseY = mouseY  


def onStep(app):
    # Exit early if the game is over
    if app.gameOver:
        return
    
    # Game logic runs only if the game is not over or won
    moveEnemyTank(app)
    enemyShoot(app)

    # Check if the enemy tank collides with the player tank
    if checkTankCollisionWithPlayer(app):
        app.gameOver = True
        app.gameWon = False  # Player loses if enemy tank collides
        updateFastestTime(app)
        return  # No need to process further if the game is over

    # Check if the player's projectile hits the enemy tank
    if checkProjectileCollisionWithEnemy(app):
        app.gameOver = True
        app.gameWon = True  # Player wins if projectile hits the enemy
        updateFastestTime(app)
        return  # No need to process further if the game is over

    # Check if the player is hit by a projectile
    if checkProjectileCollisionWithPlayer(app):
        app.gameOver = True
        app.gameWon = False  # Player loses if hit by projectile
        updateFastestTime(app)
        return  # No need to process further if the game is over

    # Handle projectile movement and wall collisions
    for projectile in list(app.projectiles):
        new_x = projectile['x'] + projectile['dx']
        new_y = projectile['y'] + projectile['dy']

        # Handle wall collisions
        for wall in app.walls:
            wallX, wallY, wallW, wallH = wall
            
            # Vertical wall hit
            if (wallX <= new_x <= wallX + wallW and
                wallY - projectile['radius'] <= new_y <= wallY + wallH + projectile['radius']):
                projectile['dy'] = -projectile['dy']  # Reverse direction on vertical wall hit
                projectile['bounces'] += 1
                new_y = projectile['y'] + projectile['dy']
                break

            # Horizontal wall hit
            if (wallY <= new_y <= wallY + wallH and
                wallX - projectile['radius'] <= new_x <= wallX + wallW + projectile['radius']):
                projectile['dx'] = -projectile['dx']  # Reverse direction on horizontal wall hit
                projectile['bounces'] += 1
                new_x = projectile['x'] + projectile['dx']
                break

        # Update projectile position after potential collision adjustments
        projectile['x'] = new_x
        projectile['y'] = new_y

        # Remove projectile if it bounces twice or goes off-screen
        if projectile['bounces'] >= 2 or not (0 <= new_x <= app.width and 0 <= new_y <= app.height):
            app.projectiles.remove(projectile)

def updateFastestTime(app):
    elapsedTime = time.time() - app.startTime
    if app.fastestTime is None or elapsedTime < app.fastestTime:
        app.fastestTime = elapsedTime

def main():
  runApp(width=750, height=500)

main()
