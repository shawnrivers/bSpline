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

# Draw coordinate axis
def drawAxisBox(leftUpPt, leftDownPt, rightDownPt, window, markCount):
  leftLine = Line(leftUpPt, leftDownPt)
  downLine = Line(leftDownPt, rightDownPt)

  lineColor = color_rgb(200, 200, 200)
  lineWidth = 1

  leftLine.setOutline(lineColor)
  downLine.setOutline(lineColor)

  leftLine.setWidth(lineWidth)
  downLine.setWidth(lineWidth)

  leftLine.draw(window)
  downLine.draw(window)

  # Marks on X-axis
  for m in range(markCount):
    markX = leftDownPt.getX() + (rightDownPt.getX() - leftDownPt.getX()) * (float(m) / float(markCount - 1))
    markLineStartPt = Point(markX, leftDownPt.getY())
    markLineEndPt = Point(markX, leftDownPt.getY() - 4)
    markLine = Line(markLineStartPt, markLineEndPt)
    markLine.setWidth(1)
    markLine.setOutline(color_rgb(0, 0, 0))
    markLine.draw(window)

    markNum = Text(Point(markX, leftDownPt.getY() + 20), str(m))
    markNum.setSize(16)
    markNum.draw(window)

  # Marks on Y-axis
  for m in range(markCount):
    markY = leftDownPt.getY() + (leftUpPt.getY() - leftDownPt.getY()) * (float(m) / float(markCount - 1))
    markLineStartPt = Point(leftDownPt.getX(), markY)
    markLineEndPt = Point(leftDownPt.getX() + 4, markY)
    markLine = Line(markLineStartPt, markLineEndPt)
    markLine.setWidth(1)
    markLine.setOutline(color_rgb(0, 0, 0))
    markLine.draw(window)

    markNum = Text(Point(leftDownPt.getX() - 20, markY), str(m))
    markNum.setSize(16)
    markNum.draw(window)

# Convert point in the axis box
def coordShiftPoint(point, origin, scale, K):
  shiftedX = (point.x * scale) / (K - 1) + origin.x
  shiftedY = -(point.y * scale / (K - 1) - origin.y)
  return Point(shiftedX, shiftedY)

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

# Draw the graph of B-spline function
def drawBSpline(n, sampleCount, knots, leftDownPt, axisBoxSize, window):
  K = len(knots)
  
  # Loop for every N_i
  for i in range(0, K - 1):

    # Loop for every interval in N_i
    for t in range(0, K - 1):
      knotCurrent = knots[t]
      knotNext = knots[t + 1]
      drawnPtList = []
      
      # Loop for every sample point in the interval
      for p in range(sampleCount + 1):
        u = knotCurrent + (knotNext - knotCurrent) * (float(p) / float(sampleCount))
        
        # Multiple knots
        if knotCurrent == knotNext:
          y = 0
        else:
          y = BSpline(n, i, float(u), knots)
        
        pt = Point(u, y)
        drawnPt = coordShiftPoint(pt, leftDownPt, axisBoxSize, K)
        print("(" + str(u) + ", " + str(y) + ") -> (" + str(drawnPt.getX()) + ", " + str(drawnPt.getY()) + ")")
        drawnPtList.append(drawnPt)

      drawLines(drawnPtList, color_rgb(0, 0, 0), window, 1)


# Main Function: Calculate and draw the result
def main():
  # Initialize window
  windowWidth = 512
  windowLength = 512
  win = GraphWin("Bernstein Polynomial", windowWidth, windowLength)
  win.setBackground(color_rgb(255, 255, 255))

  # Setting for Coordinates grid to draw the graph
  axisBoxSize = 400

  # Four vertices of the axis box drawn
  leftUpPt = Point((windowWidth - axisBoxSize) / 2, (windowLength - axisBoxSize) / 2)
  leftDownPt = Point((windowWidth - axisBoxSize) / 2, (windowLength + axisBoxSize) / 2)
  rightDownPt = Point((windowWidth + axisBoxSize) / 2, (windowLength + axisBoxSize) / 2)

  sampleCount = 10

  knots = [0.0, 1.0, 1.0, 2.0, 3.0, 4.0]

  # Draw coordinate axis
  drawAxisBox(leftUpPt, leftDownPt, rightDownPt, win, len(knots))

  # Draw B-spline functions
  drawBSpline(1, sampleCount, knots, leftDownPt, axisBoxSize, win)


  win.getKey()

main()
