#James Parks
#01-11-02
#ConstraintSnap

#select source of tranforms and then target

#
#Constraint Snap procedure
#
import maya.cmds as cmds

def jpmConstraintSnap(master, slave):
	cmds.select( cl=1 )
	cmds.select( master )
	cmds.select( slave, add=True )
	
	#CreateConstraints
	try:
		thisPoint = cmds.pointConstraint( n="tempPoint", w=1 )
		thisOrient = cmds.orientConstraint( n="tempOrient", w=1 )
		thisScale = cmds.scaleConstraint( n="tempScale", w=1 )
	except:
		print "Constraint Problems"
		
	#Delete Constraints
	cmds.select( thisPoint )
	cmds.select( thisOrient, add=1 )
	cmds.select( thisScale, add=1 )
	cmds.delete()
	
	cmds.select( slave )