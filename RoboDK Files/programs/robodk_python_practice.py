# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Or visit: http://www.robodk.com/doc/PythonAPI/
# Note: you do not need to keep a copy of this file, your python script is saved with the station
from robolink import *    # API to communicate with RoboDK
from robodk import *      # basic matrix operations
import time
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
        randNumX = random.uniform(-1,1)
        randNumY = random.uniform(-1,1)
        randNumZ = random.uniform(-1,1)
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
mypose = RDK.Item('mypose')
rearpose = RDK.Item('rearpose')
x_pos_pose = RDK.Item('x_pos_pose')
x_neg_pose = RDK.Item('x_neg_pose')
y_pos_pose = RDK.Item('y_pos_pose')
y_neg_pose = RDK.Item('y_neg_pose')
robot = RDK.Item('UR5', ITEM_TYPE_ROBOT)
test_points = RDK.Item('3d_pts_SW_output_mm')

# Display points from import
print('test_points = ' + str(test_points))
test_point_list = test_points.GetPoints(FEATURE_POINT)
test_point_array = test_point_list[0]
print('test_points = ' + str(test_point_list[0]))
pose_import = robot.Pose()
print('robot start pose = ' + str(pose_import))
pose_import.setPos(test_point_array[0])
print('robot imported pose = ' + str(pose_import))
xyz_list = []
for i in range(len(test_point_array)):
    print('test point %s = ' % i + str(test_point_array[i]))
    point = test_point_array[i]
    for j in range(len(point)):
        x = point[0]
        y = point[1]
        z = point[2]
        xyz = [x,y,z]
    xyz_list.append(xyz)
print('xyz_list = ' + str(xyz_list))


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
radius = 200 # specify a bounding radius
rand_points = MakeRandomPoints(target,N,radius)
#P_Rand = [1,1,1]
#P_Rand = [randint(-1,1)*x for x in P_Rand] # this is how to multiply a list by a scalar in python
#print('P_Rand = ' + str(P_Rand))
print('rand_points = ' + str(rand_points))

# move robot between points
while True:
    # move robot with targets created with robodk gui
    robot.MoveJ(start)
    robot.MoveJ(appr)
    robot.MoveJ(entry)
    robot.MoveJ(appr)
    robot.MoveJ(start)
    time.sleep(1)

    # move robot with points generated programmatically in python
    pose_ref = robot.Pose() # get the robot's current pose
    for i in range(NUM_POINTS):
        pose_i = pose_ref
        pose_i.setPos(points[i])
        robot.MoveJ(pose_i)
    for i in range(NUM_POINTS):
        pose_i = pose_ref
        pose_i.setPos(points[NUM_POINTS-i-1])
        robot.MoveJ(pose_i) 
    time.sleep(1)

    # move robot with points randomly generated in python
    rand_points = MakeRandomPoints(target,N,radius)
    for i in range(N):
        pose_i = pose_ref
        pose_i.setPos(rand_points[i])
        robot.MoveJ(pose_i)

    # move robot through points with solidworks points
    for i in range(len(test_point_array)):
        chkpt = test_point_array[i]
        print('chkpt %s / %s = ' % (i + 1, len(test_point_array)) + str(chkpt))
        if chkpt[0] > 0:
            # point exists in +x
            robot.MoveJ(x_pos_pose)
            pose_ref = robot.Pose()
        if chkpt[0] < 0:
            # point exists in -x
            robot.MoveJ(rearpose)
            pose_ref = robot.Pose()
            
        if chkpt[0] >0 and chkpt[1] > 0:
            # point exists in +y
            robot.MoveJ(mypose)
            pose_ref = robot.Pose()
            
            '''
        if chkpt[1] < 0:
            # point exists in -y
            robot.MoveJ(start)
            pose_ref = robot.Pose()
            '''
        pose_i = pose_ref
        pose_i.setPos(chkpt)
        robot.MoveJ(pose_i)
        '''
        pose_i = pose_ref
        pose_i.setPos(test_point_array[4])
        robot.MoveJ(pose_i)
        pose_i.setPos(test_point_array[5])
        robot.MoveJ(pose_i)

        
        print('target_position (4x4) = ' + str(pose_i))
        print('target_position (XYZRPW) = ' + str(pose_2_xyzrpw(pose_i)))
        print('target_position (angles) = ' + str(pose_angle(pose_i)))
        print('target_position (quaternion) = ' + str(pose_2_quaternion(pose_i)))
        #print('target_position (UR Target) = ' + str(pose_2_UR(pose_i)))
        '''

        
