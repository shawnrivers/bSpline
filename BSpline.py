from graphics import *

windowWidth = 512
windowLength = 512

## Draw lines from the points set
def drawLines(ptSet, color, window, width):
  for i in range(len(ptSet)):
    if i < len(ptSet) - 1:
      pt1 = ptSet[i]
      pt2 = ptSet[i + 1]
      ln = Line(pt1, pt2)
      ln.setOutline(color)
      ln.setWidth(width)
      ln.draw(window)

# Draw a white rectangle to clear the previous result
def clearWindow(window):
  windowClearer = Rectangle(Point(0, 0), Point(512, 512))
  windowClearer.setOutline(color_rgb(255, 255, 255))
  windowClearer.setFill(color_rgb(255, 255, 255))
  windowClearer.draw(window)

# Draw a message text to show the current number of knots
def displayNum(degree, segment, point, knot, window):
  messageText = "n = " + str(degree) + ", " + "s = " + str(segment) + \
      ", " + "L = " + str(point) + ", " + "K = " + str(knot)
  message = Text(Point(windowWidth / 6, windowLength / 10), messageText)
  message.setTextColor(color_rgb(0, 0, 0))
  message.draw(window)

# de Boor function
def deBoor(p1, p2, leftEnd, rightEnd, u):
  x = p1.x + (p2.x - p1.x) * (float(u) - float(leftEnd)) / \
      ((float(rightEnd)) - float(leftEnd))
  y = p1.y + (p2.y - p1.y) * (float(u) - float(leftEnd)) / \
      ((float(rightEnd)) - float(leftEnd))
  return Point(x, y)

# B-Spline function
def BSpline(r, i, u, knots):
  if r == 0:
    if u >= knots[i] and u < knots[i + 1]:
      return 1
    else:
      return 0
  else:
    if i + r + 1 > len(knots) - 1:
      return 0
    else:
      if (knots[i + r] == knots[i]) and (knots[i + r + 1] == knots[i + 1]):
        return 0
      elif knots[i + r] == knots[i]:
        return ((knots[i + r + 1] - u) / (knots[i + r + 1] - knots[i + 1])) * BSpline(r - 1, i + 1, u, knots)
      elif knots[i + r + 1] == knots[i + 1]:
        return ((u - knots[i]) / (knots[i + r] - knots[i])) * BSpline(r - 1, i, u, knots)
      else:
        return ((u - knots[i]) / (knots[i + r] - knots[i])) * BSpline(r - 1, i, u, knots) + ((knots[i + r + 1] - u) / (knots[i + r + 1] - knots[i + 1])) * BSpline(r - 1, i + 1, u, knots)

# Main Function: Calculate and draw the result
def main():
  # Initialize window
  win = GraphWin("B-Spline", windowWidth, windowLength)
  win.setBackground(color_rgb(255, 255, 255))

  # Initialize degree, segment, point and knot number
  n = 0
  s = 0
  L = 0
  K = 7

  # Create a list for control points
  controlPtList = []

  # Number of points on the curve
  sampleCount = 20

  # Input box to change n
  inputBox = Entry(Point(windowWidth / 2, windowLength / 10), 10)
  inputBox.setText(7)
  inputBox.setTextColor(color_rgb(0, 0, 0))
  inputBox.setFace("courier")
  inputBox.draw(win)

  # Message text to display the current n
  displayNum(n, s, L, K, win)

  while True:
    # When ENTER is pressed, redraw graph with the new n
    entryText = int(inputBox.getText())
    if (K != entryText):
      K = entryText
      # clearWindow(win)
      displayNum(n, s, L, K, win)

    # Get the coordinates when the mouse is clicked
    mouseCoord = win.getMouse()

    # When mouse is clicked, draw a new control point there
    if mouseCoord:
      clearWindow(win)


      # Draw a point based on the mouse's coordinates
      controlPt = Point(mouseCoord.x, mouseCoord.y)
      controlPt.setOutline(color_rgb(0, 0, 0))
      controlPt.draw(win)

      # Add the point to the control points list
      controlPtList.append(controlPt)

      # Update L, s, n
      L += 1
      s = 2 * L - K - 1
      n = K - L + 1
      displayNum(n, s, L, K, win)

    # Draw periphery lines if
    # there are more than 1 control points
    if L > 1:
      drawLines(controlPtList, color_rgb(200, 200, 200), win, 1)

    # Draw the curve when there are segments existing
    if s > 0:
      
      knots = [float(u) for u in range(0, K + n)]
      print(knots)
      dList = []
      
      # Calculate the points on the curve using B-Spline function
      for p in range(sampleCount + 1):
        # Reset d
        dX = 0
        dY = 0

        u = knots[n] + (knots[n + s] - knots[n]) * (float(p) / float(sampleCount))

        for i in range(L):
          dX += controlPtList[i].x * BSpline(n, i, u, knots)
          dY += controlPtList[i].y * BSpline(n, i, u, knots)
          print(" P_" + str(i) + "(" + str(knots[i]) + ", " + str(knots[i+1]) + "): " + str(BSpline(n, i, float(u), knots)))

        d = Point(dX, dY)
        print(str(u) + " -> " + str(d))
        d.setOutline(color_rgb(255, 0, 0))
        d.draw(win)
        dList.append(d)

      drawLines(dList, color_rgb(0, 0, 0), win, 1)


main()
