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
  messageText = "n = " + str(degree) + ", " + "s = " + str(segment) + ", " + "L = " + str(point) + ", " + "K = " + str(knot)
  message = Text(Point(windowWidth / 6, windowLength / 10), messageText)
  message.setTextColor(color_rgb(0, 0, 0))
  message.draw(window)

# de Boor function
def deBoor(p1, p2, leftEnd, rightEnd, u):
  x = p1.x + (p2.x - p1.x) * (float(u) - float(leftEnd)) / ((float(rightEnd)) - float(leftEnd))
  y = p1.y + (p2.y - p1.y) * (float(u) - float(leftEnd)) / ((float(rightEnd)) - float(leftEnd))
  return Point(x, y)


# Main Function: Calculate and draw the result
def main():
  # Initialize window
  win = GraphWin("B-Spline (de Boor)", windowWidth, windowLength)
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

      BSplinePtList = []

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
      # Draw points on the curve (sampleCount amount)
      for samp in range(sampleCount + 1):
        
        u = n + samp * float(s) / float(sampleCount)
        
        d = controlPtList

        # Calculate every result till n degree
        for r in range(1, n + 1):
          tempPt = []
          
          length = n - r + 1
          
          if u == (n + s):
            interval_start = int(u) - 1 - length + 1
            interval_end = int(u) - 1 + length
          else:
            interval_start = int(u) - length + 1
            interval_end = int(u) + length

          print("u" + str(samp) + " = " + str(u) + ", r = " + str(r) + ", len = " + str(length) + ", [" + str(interval_start) + ", " + str(interval_end) + "]")

          i = 0

          for t in range(interval_start, interval_end - length + 1):
            start = t
            end = t + length

            # function to find the right points
            if r == 1:
              startIndex = start - 1
              endIndex = end - n
            else:
              startIndex = i
              endIndex = i + 1
            
            startPt = d[startIndex]
            endPt = d[endIndex]

            print("  [" + str(start) + ", " + str(end) + "], " + "d_" + str(startIndex) + ", d_" + str(endIndex) + " -> (" + str(startPt.getX()) + ", " + str(startPt.getY()) + "), (" + str(endPt.getX()) + ", " + str(endPt.getY()) + ")")

            # function to calculate point here
            tempPt.append(deBoor(startPt, endPt, start, end, u))
          
            i += 1
          
          d = tempPt
        
        result = d[0]
        result.setOutline(color_rgb(255, 0, 0))
        result.draw(win)
        BSplinePtList.append(result)
    
      drawLines(BSplinePtList, color_rgb(0, 0, 0), win, 1)


main()
