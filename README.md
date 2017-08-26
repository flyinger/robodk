robodk


Workflow

Solidworks

Create environment in Solidworks. Define points as a 3D sketch to export to text file using macro.
TIP: Design parts in Solidworks with points defined in the part. Then place parts in assembly to 
create a 3D sketch in assembly. You will need to drop points in the 3D sketch on the assembly level
and be sure to use the quick snap/points tool to speed up the process. Once you have the complete 
set of points defined in the assembly 3D sketch, copy and paste the sketch into a new part file.
Make sure the units are correct and Z-axis is pointing in the correct direction. Origin of assembly
file should be the same as the robot base. Click the 3D sketch in the part feature tree then run 
the create_data_table.swp macro to extract the points into excel. 


RoboDK

Create station and load robot, tool, and reference frame. Run the python test script file to see if 
the selected robot can reach all the points. (TODO)
