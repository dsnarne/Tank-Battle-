from cmu_graphics import *

def onAppStart(app):
    app.url = 'https://t4.ftcdn.net/jpg/02/82/18/79/360_F_282187946_WwV8GHXwGB9x5j6OqEoMG6emNIMUBDxY.jpg'

def redrawAll(app):
    imageWidth, imageHeight = app.width, app.height

    drawLabel(f'Original ({imageWidth}x{imageHeight})', 125, 75, size=16)
    drawImage(app.url, 125, 200, align='center')


def main():
  runApp()
main()