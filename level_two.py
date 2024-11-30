import math
import time
from cmu_graphics import *
from level_one import *  

def onAppStart(app):
    app.backgroundImagePath = '/Users/dhirennarne/Desktop/Src/Images/level_two_background.jpeg'  # New background for level two
    # Modify any level-specific settings if needed

def redrawAll(app):
    drawImage(app.backgroundImagePath, 0, 0, width=app.width, height=app.height)  # Use new level's background
    drawTank(app)  # Reuse the tank drawing functions from level_one
    drawEnemyTank(app)
    
    for projectile in app.projectiles:
        drawCircle(projectile['x'], projectile['y'], projectile['radius'], fill='black')

    for wall in app.walls:
        drawRect(wall[0], wall[1], wall[2], wall[3], fill='bisque', border='burlyWood', borderWidth=3)

    drawCircle(app.mouseX, app.mouseY, app.recticleRadius, fill='red')
    drawLabel(f'Enemy Health: {app.enemyLives}', 625, 20, size=20, fill=app.enemyHealthFlashColor, bold=True)

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

    if dx != 0 or dy != 0:
        app.tankAngle = math.atan2(dy, dx)

    newX = app.tankX + dx
    newY = app.tankY + dy

    if not checkCollision(app, newX, newY):
        app.tankX, app.tankY = newX, newY

    # Keep the tank within screen bounds
    app.tankX = max(0, min(app.width - app.tankWidth, app.tankX))
    app.tankY = max(0, min(app.height - app.tankHeight, app.tankY))

    if 'space' in keys:
        spawnProjectile(app)

def spawnProjectile(app):
    currentTime = time.time()
    if currentTime - app.lastShotTime < 0.25:
        return  

    app.lastShotTime = currentTime
    playerProjectiles = [p for p in app.projectiles if p['source'] == 'player']

    if len(playerProjectiles) >= 5:
        return  # Don't spawn more than 5 projectiles

    turretCenterX = app.tankX + app.tankWidth / 2
    turretCenterY = app.tankY + app.tankHeight / 2
    startX = turretCenterX + math.cos(app.cannonAngle) * (app.turretRadius + 25)
    startY = turretCenterY + math.sin(app.cannonAngle) * (app.turretRadius + 25)

    angle = app.cannonAngle  # Cannon angle as direction

    app.projectiles.append({
        'x': startX,
        'y': startY,
        'radius': 5,
        'angle': angle,
        'dx': math.cos(angle) * 10,  
        'dy': math.sin(angle) * 10,
        'bounces': 0,
        'source': 'player'  # Mark as player's projectile
    })

def onStep(app):
    if app.gameOver:
        return
    
    moveEnemyTank(app)
    enemyShoot(app)

    if checkTankCollisionWithPlayer(app):
        app.gameOver = True
        app.gameWon = False 
        updateFastestTime(app)
        return  

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

    # Handle projectile movement and wall collisions
    for projectile in list(app.projectiles):
        new_x = projectile['x'] + projectile['dx']
        new_y = projectile['y'] + projectile['dy']

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

        projectile['x'] = new_x
        projectile['y'] = new_y
        
        if projectile['bounces'] >= 2 or not (0 <= new_x <= app.width and 0 <= new_y <= app.height):
            app.projectiles.remove(projectile)

def main():
    runApp(width=750, height=500)

main()
