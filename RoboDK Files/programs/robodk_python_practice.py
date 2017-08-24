# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Or visit: http://www.robodk.com/doc/PythonAPI/
# Note: you do not need to keep a copy of this file, your python script is saved with the station
from robolink import *    # API to communicate with RoboDK
from robodk import *      # basic matrix operations
import time
#from random import randint
import random
RDK = Robolink()

# Notify user:
print('To edit this program:\nright click on the Python program, then, select "Edit Python script"')

# Program example:
item = RDK.Item('base')
if item.Valid():
    print('Item selected: ' + item.Name())
    print('Item position: ' + repr(item.Pose()))

print('Items in the station:')
itemlist = RDK.ItemList()
print(itemlist)
print('\n')


def MakePoints(xStart, xEnd, numPoints):
    """Generates a list of points"""
    if len(xStart) != 3 or len(xEnd) != 3:
        raise Exception("Start and end point must be 3-dimensional vectors")
    if numPoints < 2:
        raise Exception("At least two points are required")
    
    # Starting Points
    pt_list = []
    x = xStart[0]
    y = xStart[1]
    z = xStart[2]

    # How much we add/subtract between each interpolated point
    x_steps = (xEnd[0] - xStart[0])/(numPoints-1)
    y_steps = (xEnd[1] - xStart[1])/(numPoints-1)
    z_steps = (xEnd[2] - xStart[2])/(numPoints-1)

    # Incrementally add to each point until the end point is reached
    for i in range(numPoints):
        point_i = [x,y,z] # create a point
        #append the point to the list
        pt_list.append(point_i)
        x = x + x_steps
        y = y + y_steps
        z = z + z_steps
    return pt_list

def MakeRandomPoints(origin, numPoints, radius):
    """Generates a list of random XYZ points about the origin"""
    pt_list = []
    x0 = origin[0]
    y0 = origin[1]
    z0 = origin[2]

    for i in range(numPoints):
        scalar = random.randint(-radius,radius)
        randNumX = random.random()
        randNumY = random.random()
        randNumZ = random.random()
        x = x0 + scalar * randNumX
        y = y0 + scalar * randNumY
        z = z0 + scalar * randNumZ
        point_i = [x,y,z]
        pt_list.append(point_i)
    return pt_list

##PETERS CODE

# Define program input parameters
P_Start = [500,200,200]
P_End = [700,200,200]
NUM_POINTS = 10

# Get the RDK items and assign to variables
start = RDK.Item('Start')
appr = RDK.Item('Approach')
entry = RDK.Item('Entry')
robot = RDK.Item('UR5', ITEM_TYPE_ROBOT)

# create list of interpolated points
points = MakePoints(P_Start,P_End,NUM_POINTS)
print('value of points = ' + str(points))

# programmatically create a new point
pose_ref = robot.Pose() # get the robot's current pose
pose_i = pose_ref
pose_i.setPos(points[0])
print('pose_ref = ' + str(pose_ref))
print('points[0] = ' + str(points[0]))
print('pose_i = ' + str(pose_i))

# create a random list of points
#target = P_Start # specify the point about which random points are to be generated
target = points[NUM_POINTS-1] # specify the point about which random points are to be generated
N = 10 # specify the number of random points to generate
rand_points = MakeRandomPoints(target,N,300)
#P_Rand = [1,1,1]
#P_Rand = [randint(-1,1)*x for x in P_Rand] # this is how to multiply a list by a scalar in python
#print('P_Rand = ' + str(P_Rand))
print('rand_points = ' + str(rand_points))

# move robot between points
while True:
    robot.MoveJ(start)
    robot.MoveJ(appr)
    robot.MoveJ(entry)
    robot.MoveJ(appr)
    robot.MoveJ(start)
    time.sleep(1)
    for i in range(NUM_POINTS):
        pose_i = pose_ref
        pose_i.setPos(points[i])
        robot.MoveJ(pose_i)
    for i in range(NUM_POINTS):
        pose_i = pose_ref
        pose_i.setPos(points[NUM_POINTS-i-1])
        robot.MoveJ(pose_i) 
    #robot.MoveJ(pose_i)
    time.sleep(1)
    for i in range(N):
        pose_i = pose_ref
        pose_i.setPos(rand_points[i])
        robot.MoveJ(pose_i)
