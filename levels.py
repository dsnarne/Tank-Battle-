import math
import time 
from cmu_graphics import *
from PIL import Image
import numpy as np

def onAppStart(app):
  app.width = 750
  app.height = 500
  app.backgroundImagePath = Image.open("Images/background.jpeg")
  app.backgroundImagePath = CMUImage(app.backgroundImagePath)
  
  app.gameOver = False
  app.gameWon = False
  app.startTime = time.time()
  app.fastestTimeLevel1 = None
  app.fastestTimeLevel2 = None
  app.levelSelect = True
  
  restartApp(app)
  
def restartApp(app):
  app.gameOver = False
  app.gameWon = False
  app.startTime = time.time()
  #tank properties
  app.tankX = app.width / 4
  app.tankY = app.height / 2
  app.tankWidth = 50
  app.tankHeight = 40
  app.tankColor = 'green'
  app.turretColor = 'lightgreen'
  app.turretRadius = 15
  app.tankSpeed = 5
  app.tankAngle = 0  #angle in radians for tank rotation
  
  app.level = 1
  
  #enemy tank properties
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
  app.enemyLives = 3
  
  app.cannonWidth = 30
  app.cannonHeight = 10
  app.cannonAngle = 0 
  
  app.enemyTank2X = app.width * 3 / 4
  app.enemyTank2Y = app.height / 4 
  app.enemyTank2Width = 50
  app.enemyTank2Height = 40
  app.enemyTank2Color = 'blue' 
  app.enemyTank2Speed = 1  
  app.enemyTank2Angle = 0
  app.enemyTank2Lives = 3  
  

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
  
  
  app.enemyHitTime = None
  app.enemyHitDuration = 0.5
  app.enemyHealthFlashColor = 'red'
  app.levelSelect = True
  
  app.speedBoosts = []
  for i in range(5):  #create 5 random yellow circles "powerups"
      x = np.random.randint(50, 750)
      y = np.random.randint(50, 350)
      radius = 15
      app.speedBoosts.append([x, y, radius])
  app.showSpeedMessage = False
  app.speedMessageTime = 0
  
  
def drawGame(app):
  drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height)
  if app.levelSelect:
    drawLevelSelectScreen(app)
    
    if app.fastestTimeLevel1 is not None:
        fastestTimeLevel1Text = f'Fastest Time (Level 1): {rounded(app.fastestTimeLevel1)} seconds'
    else:
        fastestTimeLevel1Text = 'Fastest Time (Level 1): No recorded time yet.'
    
    if app.fastestTimeLevel2 is not None:
        fastestTimeLevel2Text = f'Fastest Time (Level 2): {rounded(app.fastestTimeLevel2)} seconds'
    else:
        fastestTimeLevel2Text = 'Fastest Time (Level 2): No recorded time yet.'
    drawLabel(fastestTimeLevel1Text, app.width / 2, app.height / 2 - 90, size=20, fill='red')
    drawLabel(fastestTimeLevel2Text, app.width / 2, app.height / 2 - 60, size=20, fill='red')
    return
  
  else:  
    if app.gameOver:
      if app.gameWon:
        if app.level == 2:
          drawLabel('YOU WIN THE GAME!', app.width / 2, app.height / 2 - 40, size=40, bold=True, fill='green')
          drawLabel('Now Go For the Fastest Time!!!', app.width / 2, app.height / 2 + 100, size=20, fill='blue')
        else:  
          drawLabel('YOU WIN!', app.width / 2, app.height / 2 - 40, size=40, bold=True, fill='green')
          drawLabel('Press C to Continue to Next Level', app.width / 2, app.height / 2 + 100, size=20, fill='blue')
      else:
        drawLabel('GAME OVER', app.width / 2, app.height / 2 - 40, size=40, bold=True, fill='red')
      
      if app.level == 1:
        fastest_time_text = (
            f'Fastest Time (Level 1): {rounded(app.fastestTimeLevel1)} seconds'
            if app.fastestTimeLevel1 is not None
            else 'Fastest Time (Level 1): No recorded time yet.')
        drawLabel(fastest_time_text, app.width / 2, app.height / 2 + 40, size=20, fill='black')
      elif app.level == 2:
        fastest_time_text = (
            f'Fastest Time (Level 2): {rounded(app.fastestTimeLevel2)} seconds' 
            if app.fastestTimeLevel2 is not None else 'Fastest Time (Level 2): No recorded time yet.')
        drawLabel(fastest_time_text, app.width / 2, app.height / 2 + 40, size=20, fill='black')
        
      drawLabel(f'Press R to Restart', app.width / 2, app.height / 2, size=20, fill='red')
      return

    if app.level == 2:
      drawEnemyTank2(app)
      
    drawTank(app)
    
    drawEnemyTank(app)


    
    for boost in app.speedBoosts:
      drawCircle(boost[0], boost[1], boost[2], fill='yellow',border='black')
    
    for projectile in app.projectiles:
        drawCircle(projectile['x'], projectile['y'], projectile['radius'], fill='black')

    for wall in app.walls:
        drawRect(wall[0], wall[1], wall[2], wall[3], fill='bisque', border='burlyWood', borderWidth=3)
    
    if app.showSpeedMessage:
      drawLabel('+speed', app.tankX, app.tankY -20, size = 20, fill ='black')
      
    
    drawCircle(app.mouseX, app.mouseY, app.recticleRadius, fill='red')
    
    drawLabel(f'Red Tank Health: {app.enemyLives}', 625, 20, size =20, fill=app.enemyHealthFlashColor, bold = True)


def drawEnemyTank2(app):
  centerX = app.enemyTank2X + app.enemyTank2Width / 2
  centerY = app.enemyTank2Y + app.enemyTank2Height / 2

  halfWidth = app.enemyTank2Width / 2
  halfHeight = app.enemyTank2Height / 2
  angle = app.enemyTank2Angle

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

  # Draw the enemy tank body as a rotated rect
  drawPolygon(corners[0][0], corners[0][1],
          corners[1][0], corners[1][1],
          corners[2][0], corners[2][1],
          corners[3][0], corners[3][1],
          fill=app.enemyTank2Color, border='black')

  # Draw turret
  drawCircle(centerX, centerY, app.enemyTurretRadius, fill=app.enemyTurretColor, border='black')

  # Draw enemy cannon
  drawCannon(app, centerX, centerY, 'darkblue', False)

def checkSpeedBoostCollision(app):
  tankCenterX = app.tankX + app.tankWidth / 2
  tankCenterY = app.tankY + app.tankHeight /2 
  tankRadius = app.tankWidth / 2
  
  for boost in app.speedBoosts:
    boostX, boostY, boostRadius = boost
    distance = math.sqrt((tankCenterX - boostX) ** 2 + (tankCenterY - boostY) ** 2)
    if distance < (tankRadius + boostRadius):
      app.speedBoosts.remove(boost)
      app.tankSpeed += 1
      app.showSpeedMessage = True
      app.speedMessageTime = time.time()

def drawTank(app):
  centerX = app.tankX + app.tankWidth / 2
  centerY = app.tankY + app.tankHeight / 2

  #calc tank corners based on rotation
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

  #draw tank body as a rotated rectangle
  drawPolygon(corners[0][0], corners[0][1],
              corners[1][0], corners[1][1],
              corners[2][0], corners[2][1],
              corners[3][0], corners[3][1],
              fill=app.tankColor, border='black')

  #draw the turret
  drawCircle(centerX, centerY, app.turretRadius, fill=app.turretColor, border='black')

  #draw the cannon
  drawCannon(app, centerX, centerY, 'lightgreen', True)

def drawCannon(app, centerX, centerY, color, isPlayer):
  
  if isPlayer:
    angle = app.cannonAngle  #cannon's angle towards the mouse
    halfHeight = app.cannonHeight / 2
  else:
      dx = app.tankX - app.enemyTankX
      dy = app.tankY - app.enemyTankY
      angle = math.atan2(dy, dx)  #calc angle to the player tank
      halfHeight = app.cannonHeight / 2

  startX = centerX + math.cos(angle) * app.turretRadius   #cannon connected to the circle's edge (turret center circle thing)
  startY = centerY + math.sin(angle) * app.turretRadius

  corners = [
      (startX + math.cos(angle) * app.cannonWidth - math.sin(angle) * halfHeight,   #cannon's four corners relative to rotation
        startY + math.sin(angle) * app.cannonWidth + math.cos(angle) * halfHeight),
      (startX + math.cos(angle) * app.cannonWidth + math.sin(angle) * halfHeight,
        startY + math.sin(angle) * app.cannonWidth - math.cos(angle) * halfHeight),
      (startX - math.sin(angle) * halfHeight, startY + math.cos(angle) * halfHeight),
      (startX + math.sin(angle) * halfHeight, startY - math.cos(angle) * halfHeight)
  ]
  
  #draw cannon as rectangle rotated in toward cannon angle
  drawPolygon(corners[0][0], corners[0][1],
              corners[1][0], corners[1][1],
              corners[3][0], corners[3][1],
              corners[2][0], corners[2][1],
              fill=color, border='black')

def drawEnemyTank(app):
  centerX = app.enemyTankX + app.enemyTankWidth / 2
  centerY = app.enemyTankY + app.enemyTankHeight / 2
  
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

  #draw enemy tank body as a rotated rect
  drawPolygon(corners[0][0], corners[0][1],
              corners[1][0], corners[1][1],
              corners[2][0], corners[2][1],
              corners[3][0], corners[3][1],
              fill=app.enemyHealthFlashColor, border='black')

  #draw turret
  drawCircle(centerX, centerY, app.enemyTurretRadius, fill=app.enemyTurretColor, border='black')

  #draw enemy cannon
  drawCannon(app, centerX, centerY, 'darkred', False)

def moveEnemyTank(app):
  #calc the angle between the enemy tank and the player tank
  dx = app.tankX - app.enemyTankX
  dy = app.tankY - app.enemyTankY
  app.enemyTankAngle = math.atan2(dy, dx)  #angle to the player

  moveSpeed = app.enemyTankSpeed
  newX = app.enemyTankX + math.cos(app.enemyTankAngle) * moveSpeed
  newY = app.enemyTankY + math.sin(app.enemyTankAngle) * moveSpeed

  #check if the enemy tank will collide with any wall at the new position
  if not checkTankCollision(app, newX, newY, app.enemyTankWidth, app.enemyTankHeight):
      app.enemyTankX = newX
      app.enemyTankY = newY
  #second tank movement
  dx2 = app.tankX - app.enemyTank2X
  dy2 = app.tankY - app.enemyTank2Y
  app.enemyTank2Angle = math.atan2(dy2, dx2)
  newX2 = app.enemyTank2X + math.cos(app.enemyTank2Angle) * moveSpeed
  newY2 = app.enemyTank2Y + math.sin(app.enemyTank2Angle) * moveSpeed

  if not checkTankCollision(app, newX2, newY2, app.enemyTank2Width, app.enemyTank2Height):
      app.enemyTank2X = newX2
      app.enemyTank2Y = newY2

  #keep the enemy tank inside the screen
  app.enemyTankX = max(0, min(app.width - app.enemyTankWidth, app.enemyTankX))
  app.enemyTankY = max(0, min(app.height - app.enemyTankHeight, app.enemyTankY))

def checkTankCollision(app, newX, newY, tankWidth, tankHeight):
  for wall in app.walls:
      wallX, wallY, wallW, wallH = wall

      #check if the tank's new position will cause it to collide with a wall
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
        app.enemyLives -= 1
        app.projectiles.remove(projectile)
        if app.enemyLives <= 0:
            app.gameOver = True
            app.gameWon = False
        return True
  return False


def isPlayerVisible(app):
  enemyX = app.enemyTankX + app.enemyTankWidth / 2
  enemyY = app.enemyTankY + app.enemyTankHeight / 2
  playerX = app.tankX + app.tankWidth / 2
  playerY = app.tankY + app.tankHeight / 2

  for wall in app.walls:
      wallX, wallY, wallW, wallH = wall

      #check if the line between the enemy and player intersects with any wall
      if lineIntersectsRect(enemyX, enemyY, playerX, playerY, wallX, wallY, wallW, wallH):
          return False  #player is behind a wall

  return True  #player is visible

def lineIntersectsRect(x1, y1, x2, y2, rx, ry, rw, rh):
#work in progress used to make tank shoot only when player visible
  pass

def enemyShoot(app):
  currentTime = time.time()

  #check if 0.3 second has passed since the last shot for the red tank
  if currentTime - app.enemyLastShotTime < 0.3:
      return

  if app.level == 2:
    app.enemyLastShotTime = currentTime
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
        'source': 'enemy',  #indicate an enemy projectile
        'bounces': 0})
    
    #blue tank shooting
    startX2 = app.enemyTank2X + app.enemyTank2Width / 2
    startY2 = app.enemyTank2Y + app.enemyTank2Height / 2
    angle2 = app.enemyTank2Angle
    app.projectiles.append({
        'x': startX2,
        'y': startY2,
        'radius': 15,  #larger bullet for the blue tank
        'angle': angle2,
        'dx': 0,
        'dy': 0,
        'isTracking': True,  #tracking behavior for the blue tank
        'source': 'enemy',
        'bounces': 0,
        'speed': 0.1
    })
  else:
      if isPlayerVisible(app):  #shoot if the player is visible
        app.enemyLastShotTime = currentTime
        startX = app.enemyTankX + app.enemyTankWidth / 2
        startY = app.enemyTankY + app.enemyTankHeight / 2
        angle = app.enemyTankAngle

        app.projectiles.append({
            'x': startX,
            'y': startY,
            'radius': 5,  #small bullet for the red tank
            'angle': angle,
            'dx': math.cos(angle) * 10,
            'dy': math.sin(angle) * 10,
            'source': 'enemy',
            'bounces': 0
          })

def onKeyPress(app, key):
    if key == 'r':
      if app.gameOver:
        elapsedTime = time.time() - app.startTime
        
        if app.level == 1:
          if app.fastestTimeLevel1 is None or elapsedTime < app.fastestTimeLevel1:
            app.fastestTimeLevel1 = elapsedTime
        elif app.level == 2:
          if app.fastestTimeLevel2 is None or elapsedTime < app.fastestTimeLevel2:
            app.fastestTimeLevel2 = elapsedTime
      
      restartApp(app)
      
    elif key == 'c':  
        app.gameOver = False
        app.enemyLives = 3
        app.level = 2
        app.projectiles = []
        app.startTime = time.time()  #reset the start time when continuing
        if app.level == 2:
            app.tankX = app.width / 4
            app.tankY = app.height / 2
            app.enemyTankX = app.width * 3 / 4
            app.enemyTankY = app.height / 2
            app.enemyTankSpeed += 0.5  #increase speed for the second level
            app.enemyTank2X = app.width * 3 / 4
            app.enemyTank2Y = app.height / 4 
            app.enemyTank2Width = 50
            app.enemyTank2Height = 40
            app.enemyTank2Color = 'blue' 
            app.enemyTank2Speed = 1  
            app.enemyTank2Angle = 0
            app.enemyTank2Lives = 3
                    
  

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

  if dx != 0 or dy != 0: #update angle if there is movement
      app.tankAngle = math.atan2(dy, dx)

  newX = app.tankX + dx
  newY = app.tankY + dy

  if not checkCollision(app, newX, newY):
      app.tankX, app.tankY = newX, newY

  #keep the tank in screen
  app.tankX = max(0, min(app.width - app.tankWidth, app.tankX))
  app.tankY = max(0, min(app.height - app.tankHeight, app.tankY))
  
  if 'space' in keys:
      spawnProjectile(app)

def spawnProjectile(app):
  currentTime = time.time()

  #check if 1/4 second passed since last shot
  if currentTime - app.lastShotTime < 0.25:
      return  

  app.lastShotTime = currentTime

  playerProjectiles = [p for p in app.projectiles if p['source'] == 'player']

  if len(playerProjectiles) >= 5:
      return  #don't spawn more than 5 projectiles

  #calculate starting position of projectile at the turret's edge
  turretCenterX = app.tankX + app.tankWidth / 2
  turretCenterY = app.tankY + app.tankHeight / 2
  startX = turretCenterX + math.cos(app.cannonAngle) * (app.turretRadius + 25)
  startY = turretCenterY + math.sin(app.cannonAngle) * (app.turretRadius + 25)

  angle = app.cannonAngle  #Cannon angle as the direction

  #add projectiles
  app.projectiles.append({
      'x': startX,
      'y': startY,
      'radius': 5,
      'angle': angle,
      'dx': math.cos(angle) * 10,  
      'dy': math.sin(angle) * 10,
      'bounces': 0,
      'source': 'player'  #player projectile
  })

def moveTrackingProjectile(app, projectile):
   if projectile['isTracking']: 
    playerX = app.tankX + app.tankWidth / 2 #projectile's direction to always move towards the player's tank
    playerY = app.tankY + app.tankHeight / 2
    
    dx = playerX - projectile['x'] #angle toward player
    dy = playerY - projectile['y']
    angleToPlayer = math.atan2(dy, dx)
    
    speed = 0.1  #update the dx, dy to move towards the player
    projectile['dx'] += math.cos(angleToPlayer) * speed
    projectile['dy'] += math.sin(angleToPlayer) * speed
    projectile['x'] += projectile['dx']
    projectile['y'] += projectile['dy']


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
    if projectile['source'] == 'player':  # check player's projectiles
      enemyCenterX = app.enemyTankX + app.enemyTankWidth / 2
      enemyCenterY = app.enemyTankY + app.enemyTankHeight / 2

      if (enemyCenterX - app.enemyTankWidth / 2 <= projectile['x'] <= enemyCenterX + app.enemyTankWidth / 2 and
        enemyCenterY - app.enemyTankHeight / 2 <= projectile['y'] <= enemyCenterY + app.enemyTankHeight / 2):

        app.enemyLives -= 1
        app.projectiles.remove(projectile)

        app.enemyHitTime = time.time()  # record the time of the hit
        app.enemyHealthFlashColor = 'yellow'  # change the color to red for the flash effect

        if app.enemyLives <= 0:
            app.gameOver = True
            app.gameWon = True  
        return True
      enemy2CenterX = app.enemyTank2X + app.enemyTank2Width / 2
      enemy2CenterY = app.enemyTank2Y + app.enemyTank2Height / 2
      if (enemy2CenterX - app.enemyTank2Width / 2 <= projectile['x'] <= enemy2CenterX + app.enemyTank2Width / 2 and
          enemy2CenterY - app.enemyTank2Height / 2 <= projectile['y'] <= enemy2CenterY + app.enemyTank2Height / 2):

          app.enemyTank2Lives -= 1
          app.projectiles.remove(projectile)

          app.enemyTank2HitTime = time.time()  # Record the time of the hit
          app.enemyTank2HealthFlashColor = 'yellow'  # Flash color effect

          if app.enemyTank2Lives <= 2:
            app.enemyTank2X = -100  # Move it off-screen (or flag it for removal)
            app.enemyTank2Y = -100
          return True
  return False

def onMouseMove(app, mouseX, mouseY):
  turretCenterX = app.tankX + app.tankWidth / 2
  turretCenterY = app.tankY + app.tankHeight / 2
  dx = mouseX - turretCenterX  #difference between mouse and turret center X
  dy = mouseY - turretCenterY  #difference between mouse and turret center Y
  app.cannonAngle = math.atan2(dy, dx)  #get the angle using arctan2 function
  app.mouseX = mouseX  
  app.mouseY = mouseY

def onMousePress(app, mouseX, mouseY):
    if app.levelSelect:
        level1_button_x = app.width / 4 - 100
        level1_button_y = app.height / 2
        level1_button_width = 200
        level1_button_height = 50
        # Check if mouse is within the bounds of Level 1 button
        if (level1_button_x <= mouseX <= level1_button_x + level1_button_width and
            level1_button_y <= mouseY <= level1_button_y + level1_button_height):
            app.levelSelect = False  # Hide the level select screen
            app.level = 1  # Set the level to 1

        level2_button_x = app.width * 3 / 4 - 100
        level2_button_y = app.height / 2
        # Check if mouse is within the bounds of Level 2 button
        if (level2_button_x <= mouseX <= level2_button_x + level1_button_width and
            level2_button_y <= mouseY <= level2_button_y + level1_button_height):
            app.levelSelect = False  # Hide the level select screen
            app.level = 2  # Set the level to 2

  


def onStep(app):
  if app.gameOver:
    if app.gameWon:
      elapsedTime = time.time() - app.startTime
      if app.level == 1:
        if app.fastestTimeLevel1 is None or elapsedTime < app.fastestTimeLevel1:
          app.fastestTimeLevel1 = elapsedTime
      elif app.level == 2:
        if app.fastestTimeLevel2 is None or elapsedTime < app.fastestTimeLevel2:
            app.fastestTimeLevel2 = elapsedTime
    if app.gameOver:
        return
      
  moveEnemyTank(app)
  enemyShoot(app)
  checkSpeedBoostCollision(app)
  if checkTankCollisionWithPlayer(app):
      app.gameOver = True
      app.gameWon = False 
      updateFastestTime(app)
      return  
  if time.time() - app.speedMessageTime > 1:
    app.showSpeedMessage = False
  #check if the player's projectile hits the enemy tank
  if checkProjectileCollisionWithEnemy(app):
      if app.enemyLives <= 0:
        app.gameOver = True
        app.gameWon = True  
        updateFastestTime(app)
      return 

  if checkProjectileCollisionWithPlayer(app):
      app.gameOver = True
      app.gameWon = False  
      updateFastestTime(app)
      return 

  #handle projectile movement and wall collisions
  for projectile in list(app.projectiles):
      if projectile.get('isTracking', False):  #move tracking projectiles
            moveTrackingProjectile(app, projectile)
      
      new_x = projectile['x'] + projectile['dx']
      new_y = projectile['y'] + projectile['dy']

      for wall in app.walls:
          wallX, wallY, wallW, wallH = wall
          
          #vertical wall hit
          if (wallX <= new_x <= wallX + wallW and
              wallY - projectile['radius'] <= new_y <= wallY + wallH + projectile['radius']):
              projectile['dy'] = -projectile['dy']  #reverse direction on vertical wall hit
              projectile['bounces'] += 1
              new_y = projectile['y'] + projectile['dy']
              break

          #horizontal wall hit
          if (wallY <= new_y <= wallY + wallH and
              wallX - projectile['radius'] <= new_x <= wallX + wallW + projectile['radius']):
              projectile['dx'] = -projectile['dx']  #reverse direction on horizontal wall hit
              projectile['bounces'] += 1
              new_x = projectile['x'] + projectile['dx']
              break

      projectile['x'] = new_x
      projectile['y'] = new_y
      
      if projectile['bounces'] >= 2 or not (0 <= new_x <= app.width and 0 <= new_y <= app.height):
          app.projectiles.remove(projectile)

  if app.enemyHitTime and time.time() - app.enemyHitTime < 0.20:
      if int(time.time() * 10) % 0.1 == 0:  
          app.enemyHealthFlashColor = 'yellow'
      else:
          app.enemyHealthFlashColor = 'red'

  elif app.enemyHitTime and time.time() - app.enemyHitTime > 0.20:

      app.enemyHealthFlashColor = 'red'
      app.enemyHitTime = None
  
  for boost in app.speedBoosts:
    x, y, radius = boost
    if (app.tankX + app.tankWidth / 2 - x) ** 2 + (app.tankY + app.tankHeight / 2 - y) ** 2 < (radius + app.tankWidth / 2) ** 2:
      app.tankSpeed += 2  #increase speed
      newX = np.random.randint(50, 750)
      newY = np.random.randint(50, 350)
      boost[0] = newX
      boost[1] = newY

def updateFastestTime(app):
  elapsedTime = time.time() - app.startTime
  if app.level == 1:
    if app.fastestTimeLevel1 is None or elapsedTime < app.fastestTimeLevel1:
        app.fastestTimeLevel1 = elapsedTime
  elif app.level == 2:
    if app.fastestTimeLevel2 is None or elapsedTime < app.fastestTimeLevel2:
        app.fastestTimeLevel2 = elapsedTime

def drawLevelSelectScreen(app):
  drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height)
  
  drawLabel('Select Level', app.width / 2, 100, size=40, bold=True, fill='Black')

  level1_button_x = app.width / 4 - 100
  level1_button_y = app.height / 2
  level1_button_width = 200
  level1_button_height = 50
  drawRect(level1_button_x, level1_button_y, level1_button_width, level1_button_height, fill='lightblue', border='black')
  drawLabel('Level 1', level1_button_x + level1_button_width / 2, level1_button_y + level1_button_height / 2, size=20, bold=True)

  level2_button_x = app.width * 3 / 4 - 100
  level2_button_y = app.height / 2
  drawRect(level2_button_x, level2_button_y, level1_button_width, level1_button_height, fill='lightgreen', border='black')
  drawLabel('Level 2', level2_button_x + level1_button_width / 2, level2_button_y + level1_button_height / 2, size=20, bold=True)
  
  drawLabel('Click on a level to start', app.width / 2, app.height / 2 + 100, size=20, fill='Black')

