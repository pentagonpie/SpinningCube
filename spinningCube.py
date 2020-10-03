import pygame
import math
import sys
import numpy as np

class point:

    def __init__(self,x,y,z):
        if math.fabs(x)<1e-12:
            self.x = 0
        else:
            self.x = x

        if math.fabs(y)<1e-12:
            self.y = 0
        else:
            self.y = y

        if math.fabs(z)<1e-12:
            self.z = 0
        else:
            self.z = z
        
    def distance(self,pointB):
        deltaX = pointB.x-self.x
        deltaY = pointB.y-self.y
        deltaZ = pointB.z-self.z
        return math.sqrt(deltaX**2+deltaY**2+deltaZ**2)


    def getCenterPoint(self,pointB):
        newX = (self.x + pointB.x )/2
        newY = (self.y + pointB.y )/2
        newZ = (self.z + pointB.z )/2
        return point(newX,newY,newZ)

    def __str__(self):
        x = '%.2f' % self.x
        y = '%.2f' % self.y
        z = '%.2f' % self.z
        return "({},{},{})".format(x,y,z)


    def dotProduct(self,aPoint):
        return self.x*aPoint[0]+self.y*aPoint[1]+self.z+aPoint[2]

class cube:

    points = []
    lines = []

    def __init__(self, a,b,c,d,e,f,g,h):
        self.points.append(a)
        self.points.append(b)
        self.points.append(c)
        self.points.append(d)
        self.points.append(e)
        self.points.append(f)
        self.points.append(g)
        self.points.append(h)

    def createLines(self):
        self.lines.clear()
        self.lines.append(line(self.points[0],self.points[1]))
        self.lines.append(line(self.points[1],self.points[2]))
        self.lines.append(line(self.points[2],self.points[3]))
        self.lines.append(line(self.points[3],self.points[0]))

        self.lines.append(line(self.points[4],self.points[5]))
        self.lines.append(line(self.points[5],self.points[6]))
        self.lines.append(line(self.points[6],self.points[7]))
        self.lines.append(line(self.points[7],self.points[4]))

        self.lines.append(line(self.points[0],self.points[4]))
        self.lines.append(line(self.points[1],self.points[5]))
        self.lines.append(line(self.points[2],self.points[6]))
        self.lines.append(line(self.points[3],self.points[7]))
    

    def getLines(self):
        return self.lines

    def update(self):

        radius = 0.7071
        center1 = point(0,0,self.points[0].z)
        center2 = point(0,0,self.points[4].z)
        movement = 3
        for x in range(4):
            self.points[x] = sphere.movePointArc(radius,self.points[x], movement,center1)

        for x in range(4,8):
            self.points[x] = sphere.movePointArc(radius,self.points[x], movement,center2)

        self.createLines()

    def __str__(self):
        string = "Lines:\n"
        for aLine in self.lines:
            toAdd = '{}'.format(aLine)
            string += toAdd
            string += '\n'

        string+="\n\nPoints:\n"
        for aPoint in self.points:
            toAdd = '{}'.format(aPoint)
            string += toAdd
            string += '\n'

        return string

class line:
    def __init__(self, a,b):
        self.start = point(a.x,a.y,a.z)
        self.end = point(b.x,b.y,b.z)
    
    def __str__(self):
        return "({}) -> ({})".format(self.start,self.end)

    #gets normal from vector ab, from a to b
    def getNormal(self):
        values = [self.b.x-self.a.x,self.b.y-self.a.y,self.b.z-self.a.z]
        return np.array(values)

    

class sphere:

    #steps is what angle to move the point
    @staticmethod
    def movePointArc(radius, aPoint,steps,center):

        oldAngle = sphere.getAngleFromPoint(radius,aPoint,center)
        angle = math.pi/40*steps+oldAngle
        newX = center.x + math.cos(angle)*radius
        newY = center.y + math.sin(angle)*radius
        return point(newX,newY,aPoint.z)

    @staticmethod
    def getRadiusFromHeight(radius, h):
        return math.sqrt((radius**2)-(h*h))

    @staticmethod
    def getFirstPoint(radius,center):
        return point(center.x-radius,center.y,center.z)

    @staticmethod
    def getAngleFromPoint(radius,aPoint,center):
        translateX = aPoint.x-center.x
        translateY = aPoint.y-center.y
        angle = 0
        
        if math.fabs(aPoint.x)<1e-12:

            if aPoint.y > 0:
                return math.pi/2
            else:
                return math.pi*1.5
        if math.fabs(aPoint.y)<1e-12:

            if aPoint.x > 0:
                return math.pi*2
            else:
                return math.pi

        try:
            angle = math.asin(translateY/radius)
        except:
            print("Exception at getAngleFromPoint function\nin asin function we try {},{}".format(translateY,radius))
            sys.exit(1)
        yangle = math.fabs(angle)

        if aPoint.x<0 and aPoint.y < 0:
            return math.pi+yangle
        elif aPoint.x<0 and aPoint.y > 0:
            return math.pi/4+angle
        elif aPoint.x>0 and aPoint.y < 0:
            return math.pi*1.5+angle
        else:
            return angle


    def getViewingAngle(self,steps):
        return steps*math.pi/60

    def getPointViewer(self,angle,radius):
        x = 0
        y = math.cos(angle)/radius
        y *= -1
        z = math.sin(angle)/radius
        return point(x,y,z)

def getPlane(aPoint,normal):
    plane = [aPoint.x,aPoint.y,aPoint.z]
    d = 0
    for i,j in zip(aPoint,normal):
        d += i*j
    d *= -1
    plane += d
    return plane



#not in use,delete
def projectionScreen(aPoint):
    newY = aPoint.y+((8+4*aPoint.y)/4)
    return point(aPoint.x,newY,aPoint.z)

def getProjected(aPoint, viewerPoint):
 
   # if aPoint.y > 0:
      #  newX = aPoint.x+aPoint.y*paralax
      #  newY = aPoint.z+aPoint.y*paralax
   # else:
      #  newX = aPoint.x-aPoint.y*paralax
       # newY = aPoint.z-aPoint.y*paralax

    normal = line(viewerPoint,aPoint).getNormal()
    plane = getPlane(viewerPoint,normal)
    distance = aPoint.dotProduct(normal) + plane[3]
    
    projectedX = aPoint.x+distance*normal[0]
    projectedY = aPoint.y+distance*normal[1]
    projectedZ = aPoint.z+distance*normal[2]
    
    
    newPoint = point(projectedX,projectedZ,projectedZ )
    print("projecting point {} to point {}".format(aPoint,newPoint))
    return newPoint

def setParalax(aPoint):
    paralax = 0.9

    newX = aPoint.x*(math.e**(paralax*aPoint.y))   
    newY = aPoint.z*(math.e**(paralax*aPoint.y))  
    newPoint = point(newX,newY, aPoint.z)
    print("projecting point {} to point {}".format(aPoint,newPoint))
    return newPoint

def getProjectedLines(aCube):
    global sizeX
    global sizeY
    multiplier = 120
    points = []
    lines = aCube.getLines()
    projectedLines = []

    for aline in lines:
        startCorner = getProjected(aline.start)
        startCenter = point((startCorner.x)*multiplier+sizeX/2, (startCorner.y)*multiplier+sizeY/2,startCorner.z)

        endCorner = getProjected(aline.end)
        endCenter = point((endCorner.x)*multiplier+sizeX/2, (endCorner.y)*multiplier+sizeY/2,endCorner.z)
        newLine = line(startCenter,endCenter)
        projectedLines.append(newLine)
    
    return projectedLines


def getCubeInSphere():
    height = math.sqrt(2)/2
    aRadius = sphere.getRadiusFromHeight(1,-height)

    center = point(0,0,-height)
    step = 20
    a = sphere.getFirstPoint(aRadius,point(0,0,-height))

    b = sphere.movePointArc(aRadius,a,step,center)
    c = sphere.movePointArc(aRadius,b,step,center)
    d = sphere.movePointArc(aRadius,c,step,center)

    center2 = point(0,0,height)

    aRadius2 = sphere.getRadiusFromHeight(1,height)

    e = sphere.getFirstPoint(aRadius2,point(0,0,height))

    f = sphere.movePointArc(aRadius2,e,step,center2)
    g = sphere.movePointArc(aRadius2,f,step,center2)
    h = sphere.movePointArc(aRadius2,g,step,center2)

    aCube = cube(a,b,c,d,e,f,g,h)
    return aCube


pygame.init()

sizeX = 600
sizeY = 600

screen = pygame.display.set_mode((sizeX,sizeY))

done = False
color = (0, 128, 255)
x = 30
y = 30

aCube = getCubeInSphere()

i = 0
for aLine in aCube.getLines():
    i+=1
    print("{}Oprinting line real:{} ".format(i,aLine))
    

for aLine in getProjectedLines(aCube):
    i+=1
    print("{}Oprinting line projected: {}".format(i,aLine))
    

clock = pygame.time.Clock()


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue
        
        count = 0
        aCube.update()

        screen.fill((22, 0, 45))
        for aLine in getProjectedLines(aCube):
            #print("{}Iprinting line projected: {}".format(i,aLine))
            count+=1
            pygame.draw.line(screen,color,(int(aLine.start.x),int(aLine.start.y)),(int(aLine.end.x),int(aLine.end.y)),2)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(6)


