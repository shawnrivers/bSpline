from graphics import *

# Draw lines from the points set
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

# Linear interpolation
def lagrangeInterpolation(p0, p1, t, i, r):
  x = p0.x * float(i + r - t) / float(r) + p1.x * float(t - i) / float(r)
  y = p0.y * float(i + r - t) / float(r) + p1.y * float(t - i) / float(r)
  return Point(x, y)


def main():
  # Initialize window
  win = GraphWin("Polynomial Curve (Aitken)", 512, 512)
  win.setBackground(color_rgb(255, 255, 255))

  ptList = []  # Create a list for control points
  sampleCount = 20  # Number of points on the curve
  
  while True:
    mouseCoord = win.getMouse()  # Get the coordinates when the mouse is clicked

    if mouseCoord:
      clearWindow(win)

      # Create a list for points on the curve
      bezierPtList = []

      # Draw a point based on the mouse's coordinates
      pt = Point(mouseCoord.x, mouseCoord.y)
      pt.setOutline(color_rgb(0, 0, 0))
      pt.draw(win)

      # Add the point to the control points list
      ptList.append(pt)
      print(ptList)
      L = len(ptList)
      n = L - 1

      if L > 1:
        # Draw periphery lines
        drawLines(ptList, color_rgb(200, 200, 200), win, 1)

        # Loop for every sample point
        for k in range(sampleCount + 1):
          t = float(k) * float(n) / float(sampleCount)
          p = ptList

          # Loop for every recursion level
          for r in range(1, n + 1):
            temp = []
            # Loop for every p_i^r
            for i in range(n + 1 - r):
              # Calculate points on the curve using Linear Interpolation
              temp.append(lagrangeInterpolation(p[i], p[i + 1], t, i, r))
            p = temp

          # Draw a point on the curve
          result = p[0]
          result.setOutline(color_rgb(255, 0, 0))
          result.draw(win)
          bezierPtList.append(result)

        # Draw Beizer curve
        drawLines(bezierPtList, color_rgb(0, 0, 0), win, 1)


# Run the program
main()
