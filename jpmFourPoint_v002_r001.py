##left_front = "L_Front_Wheel_PLACE"
##right_front = "R_Front_Wheel_PLACE"
##left_rear = "L_Back_Wheel_PLACE"
##right_rear = "R_Back_Wheel_PLACE"

##left_front_pos = getPositions(left_front)
##right_front_pos = getPositions(right_front)
##left_rear_pos = getPositions(left_rear)
##right_rear_pos = getPositions(right_rear)

##leftAnchors = ["L_Front_Wheel_PLACE", "L_Back_Wheel_PLACE"]
##rightAnchors = ["R_Front_Wheel_PLACE", "R_Back_Wheel_PLACE"]
##frontAnchors = ["L_Front_Wheel_PLACE", "R_Front_Wheel_PLACE"]
##rearAnchors = ["L_Back_Wheel_PLACE", "R_Back_Wheel_PLACE"]

##fourPointAnchors = ["left_front_PLACE", "right_front_PLACE", "left_rear_PLACE", "right_rear_PLACE"]

##make4point( "square", "suspension", fourPointAnchors )
##make4point( "cross", "wheels", fourPointAnchors )
##make4point( "x", "test", fourPointAnchors )
##make4point( "nurbs", "nurbs", fourPointAnchors )
#name = "test"

##fourPointAnchors = ["neck_A_top_ctl_loc", "neck_A_right_ctl_loc", "neck_A_left_ctl_loc", "neck_A_bot_ctl_loc"]
##fourPointAnchors = ["neck_B_top_ctl_loc", "neck_B_right_ctl_loc", "neck_B_left_ctl_loc", "neck_B_bot_ctl_loc"]

##make4point( "nurbs", "neck_A", fourPointAnchors )
##make4point( "nurbs", "neck_B", fourPointAnchors )

import maya.cmds as cmds
import maya.mel as mm
##import math
##import os
##import sys

import jpmCreateControls as ctrls
import helperFunctions as helpers
import jpmAutoCluster as autoCluster
import jpmMakeRivet as rivet


##

def make4point( fourPointType, name, anchors=[]):
	allJnts = []
	allTopJnts = []
	allIK = []
	allCtrls = []
	allCentroids = []
	allExpr = []

	left_front = anchors[0]
	right_front = anchors[1]
	left_rear = anchors[2]
	right_rear = anchors[3]
	
	##Make Control structure
	left_front_ctrl = helpers.makeObj( ("left_front_" + name), "pivot", left_front, 180, 0, 0 )
	right_front_ctrl = helpers.makeObj( ("right_front_" + name), "pivot", right_front, 180, 0, 0 )
	left_rear_ctrl = helpers.makeObj( ("left_rear_" + name), "pivot", left_rear, 180, 0, 0 )
	right_rear_ctrl = helpers.makeObj( ("right_rear_" + name), "pivot", right_rear, 180, 0, 0 )
	
	allCtrls = [left_front_ctrl, right_front_ctrl, left_rear_ctrl, right_rear_ctrl]
	
	for ctrl in allCtrls:
		cmds.setAttr( (ctrl + ".scale"), 0.05, 0.05, 0.05 )
		cmds.makeIdentity( ctrl, apply=1 )
		
	
		##Make and place centroids	
	left_centroid = helpers.makeObj( ("left_" + name + "_loc"), "locator", left_front, 0, 0, 0)
	cmds.pointConstraint( left_front_ctrl, left_centroid, mo=0 )
	cmds.pointConstraint( left_rear_ctrl, left_centroid, mo=0 )
	cmds.aimConstraint( left_front_ctrl, left_centroid, mo=0 )
	
	right_centroid = helpers.makeObj( ("right_" + name + "_loc"), "locator", right_front, 0, 0, 0)
	cmds.pointConstraint( right_front_ctrl, right_centroid, mo=0 )
	cmds.pointConstraint( right_rear_ctrl, right_centroid, mo=0 )
	cmds.aimConstraint( right_front_ctrl, right_centroid, mo=0 )
	
	center_centroid = helpers.makeObj( ("center_" + name + "_loc"), "locator", left_front, 0, 0, 0)
	cmds.pointConstraint( left_front_ctrl, center_centroid, mo=0 )
	cmds.pointConstraint( right_front_ctrl, center_centroid, mo=0 )
	cmds.pointConstraint( left_rear_ctrl, center_centroid, mo=0 )
	cmds.pointConstraint( right_rear_ctrl, center_centroid, mo=0 )
	cmds.addAttr( ln="rearX", at="float", dv=0,  )
	cmds.addAttr( ln="frontX", at="float", dv=0,  )
	cmds.addAttr( ln="leftZ", at="float", dv=0,  )
	cmds.addAttr( ln="rightZ", at="float", dv=0,  )
	cmds.setAttr( ".rearX", k=1, cb=1 )
	cmds.setAttr( ".frontX", k=1, cb=1 )
	cmds.setAttr( ".leftZ", k=1, cb=1 )
	cmds.setAttr( ".rightZ", k=1, cb=1 )
	
	centroid_offset_2 = cmds.group(center_centroid, w=0, name=("center_" + name + "_offset_2"))
	centroid_offset_1 = cmds.group(centroid_offset_2, w=0, name=("center_" + name + "_offset_1"))
	
	allCentroids = [center_centroid, left_centroid, right_centroid]
	
	
	#######################################
	##Make the different types of fourPoint
	#######################################
	
	########
	##SQUARE
	########
	if fourPointType == "square":
			##Make Joint and IK structure
		left_front_jnt = helpers.makeJoint( "left_front", left_front, name )
		left_rear_jnt = helpers.makeJoint( "left_rear", left_rear, name )
		
		right_front_jnt = helpers.makeJoint( "right_front", right_front, name )
		right_rear_jnt = helpers.makeJoint( "right_rear", right_rear, name )
		
		front_left_jnt = helpers.makeJoint( "front_left", left_front, name )
		front_right_jnt = helpers.makeJoint( "front_right", right_front, name )
		
		rear_left_jnt = helpers.makeJoint( "rear_left", left_rear, name )
		rear_right_jnt = helpers.makeJoint( "rear_right", right_rear, name )
		
		cmds.parent( left_rear_jnt, left_front_jnt )
		cmds.parent( right_rear_jnt, right_front_jnt )
		cmds.parent( front_right_jnt, front_left_jnt )
		cmds.parent( rear_right_jnt, rear_left_jnt )
		
		allJnts = [left_front_jnt, left_rear_jnt, right_front_jnt, right_rear_jnt, front_left_jnt, front_right_jnt, rear_left_jnt, rear_right_jnt]
		allTopJnts = [left_front_jnt, right_front_jnt, front_left_jnt, rear_left_jnt]
    
		for thisJoint in allTopJnts:
			cmds.makeIdentity( thisJoint, apply=1 )
			cmds.joint( thisJoint, e=1, oj="yzx", sao="yup", zso=1 )
		
		left_IK = cmds.ikHandle( n=("left_" + name + "_IK"), sj=left_front_jnt, ee=left_rear_jnt )
		right_IK = cmds.ikHandle( n=("right_" + name + "_IK"), sj=right_front_jnt, ee=right_rear_jnt )
		front_IK = cmds.ikHandle( n=("front_" + name + "_IK"), sj=front_left_jnt, ee=front_right_jnt )
		rear_IK = cmds.ikHandle( n=("rear_" + name + "_IK"), sj=rear_left_jnt, ee=rear_right_jnt )
		
		allIK = [left_IK[0], right_IK[0], front_IK[0], rear_IK[0]]
    
		cmds.parentConstraint( left_front_ctrl, left_front_jnt, mo=1 )
		cmds.parentConstraint( left_front_ctrl, front_left_jnt, mo=1 )
		
		cmds.parentConstraint( right_front_ctrl, right_front_jnt, mo=1 )
		cmds.parentConstraint( right_front_ctrl, front_IK[0], mo=1 )
		
		cmds.parentConstraint( left_rear_ctrl, left_IK[0], mo=1 )
		cmds.parentConstraint( left_rear_ctrl, rear_left_jnt, mo=1 )
		
		cmds.parentConstraint( right_rear_ctrl, right_IK[0], mo=1 )
		cmds.parentConstraint( right_rear_ctrl, rear_IK[0], mo=1 )		
		
			#Make center centroid expression
		centroid_orient_EXPR = """
		//Find X Angles 
float $rearXangle = :::REAR_LEFT_JNT:::.rotateX;
float $frontXangle = :::FRONT_LEFT_JNT:::.rotateX;

//Find Z Angles
float $leftZangle = :::LEFT_FRONT_JNT:::.rotateX;
float $rightZangle = :::RIGHT_FRONT_JNT:::.rotateX;

//Assignations
:::CENTROID:::.rearX = $rearXangle;
:::CENTROID:::.frontX = $frontXangle;
:::CENTROID:::.leftZ = $leftZangle;
:::CENTROID:::.rightZ = $rightZangle;

:::CENTROID_OFFSET2:::.rotateZ = -(($rearXangle) + ($frontXangle))/2;
:::CENTROID_OFFSET1:::.rotateX = (($leftZangle) + ($rightZangle))/2;
		"""
			
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::REAR_LEFT_JNT:::", rear_left_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::FRONT_LEFT_JNT:::", front_left_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::LEFT_FRONT_JNT:::", left_front_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::RIGHT_FRONT_JNT:::", right_front_jnt )
			
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID:::", center_centroid[0] )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID_OFFSET2:::", centroid_offset_2 )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID_OFFSET1:::", centroid_offset_1 )

		##print centroid_orient_EXPR
		
		orient_expr = cmds.expression(n=(name + "_orient_EXPR"), s=centroid_orient_EXPR)
		allExpr = [orient_expr]

	#######
	##CROSS
	#######
	if fourPointType == "cross":
			##Find mid-point between controls
		z_axis_front = helpers.midPoint( left_front, right_front )
		z_axis_rear = helpers.midPoint( left_rear, right_rear )
		x_axis_left = helpers.midPoint( left_front, left_rear )
		x_axis_right = helpers.midPoint( right_front, right_rear )
	
			##Make Joint and IK structure
		z_front_jnt = helpers.makeJoint( "z_front", z_axis_front, name )
		z_rear_jnt = helpers.makeJoint( "z_rear", z_axis_rear, name )
		
		x_left_jnt = helpers.makeJoint( "x_left", x_axis_left, name )
		x_right_jnt = helpers.makeJoint( "x_right", x_axis_right, name )
		
		cmds.parent( z_rear_jnt, z_front_jnt )
		cmds.parent( x_right_jnt, x_left_jnt )
		
		allJnts = [z_front_jnt, z_rear_jnt, x_left_jnt, x_right_jnt]
		allTopJnts = [z_front_jnt, x_left_jnt]
		
		for thisJoint in allTopJnts:
			cmds.makeIdentity( thisJoint, apply=1 )
			cmds.joint( thisJoint, e=1, oj="yzx", sao="yup", zso=1 )
		
		z_IK = cmds.ikHandle( n=("z_" + name + "_IK"), sj=z_front_jnt, ee=z_rear_jnt )
		x_IK = cmds.ikHandle( n=("x_" + name + "_IK"), sj=x_left_jnt, ee=x_right_jnt )
		
		allIK = [z_IK[0], x_IK[0]]
		
		cmds.parentConstraint( left_front_ctrl, z_front_jnt, mo=1 )
		cmds.parentConstraint( right_front_ctrl, z_front_jnt, mo=1 )
		cmds.parentConstraint( left_front_ctrl, x_left_jnt, mo=1 )
		cmds.parentConstraint( left_rear_ctrl, x_left_jnt, mo=1 )
		
		cmds.parentConstraint( left_rear_ctrl, z_IK[0], mo=1 )
		cmds.parentConstraint( right_rear_ctrl, z_IK[0], mo=1 )
		cmds.parentConstraint( right_front_ctrl, x_IK[0], mo=1 )
		cmds.parentConstraint( right_rear_ctrl, x_IK[0], mo=1 )
		
			#Make center centroid expression
		centroid_orient_EXPR = """
		float $zAngle = :::Z_FRONT_JNT:::.rotateX;
float $xAngle = :::X_LEFT_JNT:::.rotateX;

:::CENTROID_OFFSET2:::.rotateZ = -($xAngle);
:::CENTROID_OFFSET1:::.rotateX = $zAngle;
		"""
		
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::Z_FRONT_JNT:::", z_front_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::X_LEFT_JNT:::", x_left_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID_OFFSET2:::", centroid_offset_2 )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID_OFFSET1:::", centroid_offset_1 )
		
		orient_expr = cmds.expression(n=(name + "_orient_EXPR"), s=centroid_orient_EXPR)
		allExpr = [orient_expr]
	
	###
	##X
	###
	if fourPointType == "x":
			##Make Joint and IK structure
		left_front_jnt = helpers.makeJoint( "left_front", left_front, name )
		right_rear_jnt = helpers.makeJoint( "right_rear", right_rear, name )
		
		right_front_jnt = helpers.makeJoint( "right_front", right_front, name )
		left_rear_jnt = helpers.makeJoint( "left_rear", left_rear, name )
		
		cmds.parent( right_rear_jnt, left_front_jnt )
		cmds.parent( left_rear_jnt, right_front_jnt )
		
		allJnts = [left_front, right_rear_jnt, right_front_jnt, left_rear_jnt]
		allTopJnts = [left_front_jnt, right_front_jnt]
		
		for thisJoint in allTopJnts:
			cmds.makeIdentity( thisJoint, apply=1 )
			cmds.joint( thisJoint, e=1, oj="yzx", sao="yup", zso=1 )
		
		right_rear_IK = cmds.ikHandle( n=("left_rear_" + name + "_IK"), sj=left_front_jnt, ee=right_rear_jnt )
		left_rear_IK = cmds.ikHandle( n=("right_rear_" + name + "_IK"), sj=right_front_jnt, ee=left_rear_jnt )
		
		allIK = [right_rear_IK[0], left_rear_IK[0]]
		
		cmds.parentConstraint( left_front_ctrl, left_front_jnt, mo=1 )
		cmds.parentConstraint( right_front_ctrl, right_front_jnt, mo=1 )
		
		cmds.parentConstraint( left_rear_ctrl, left_rear_IK[0], mo=1 )
		cmds.parentConstraint( right_rear_ctrl, right_rear_IK[0], mo=1 )
		
			#Make center centroid expression
		centroid_orient_EXPR = """
float $leftXAngle = :::LEFT_FRONT_JNT:::.rotateX;
float $rightXAngle = :::RIGHT_FRONT_JNT:::.rotateX;

:::CENTROID_OFFSET2:::.rotateZ = -($leftXAngle - $rightXAngle)/2;
:::CENTROID_OFFSET1:::.rotateX = ($leftXAngle + $rightXAngle)/2;
		"""
		
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::LEFT_FRONT_JNT:::", left_front_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::RIGHT_FRONT_JNT:::", right_front_jnt )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID_OFFSET2:::", centroid_offset_2 )
		centroid_orient_EXPR = centroid_orient_EXPR.replace( ":::CENTROID_OFFSET1:::", centroid_offset_1 )
		
		orient_expr = cmds.expression(n=(name + "_orient_EXPR"), s=centroid_orient_EXPR)
		allExpr = [orient_expr]	
		
	
	#############
	##NURBS Plane
	#############
	if fourPointType == "nurbs":
		#Make NURBS plane
		nurbs_plane = cmds.nurbsPlane( n=(name + "_plane"), p=(0,0,0), ax=(0,1,0), w=1, lr=1, d=1, u=1, v=1, ch=0 )[0]
		left_front_loc = autoCluster.jpmAutoCluster( (nurbs_plane + ".cv[1][1]"), ("left_front" + name) )[0]
		right_front_loc = autoCluster.jpmAutoCluster( (nurbs_plane + ".cv[1][0]"), ("right_front" + name) )[0]
		left_rear_loc = autoCluster.jpmAutoCluster( (nurbs_plane + ".cv[0][1]"), ("left_rear" + name) )[0]
		right_rear_loc = autoCluster.jpmAutoCluster( (nurbs_plane + ".cv[0][0]"), ("right_rear" + name) )[0]
		
		allJnts = [left_front_loc, right_front_loc, left_rear_loc, right_rear_loc]
		allTopJnts = [left_front_loc, right_front_loc, left_rear_loc, right_rear_loc]
		
		allIK = [nurbs_plane]
		
		##constrain cluster locators to the controls
		cmds.pointConstraint( left_front_ctrl, left_front_loc )
		cmds.pointConstraint( right_front_ctrl, right_front_loc )
		cmds.pointConstraint( left_rear_ctrl, left_rear_loc )
		cmds.pointConstraint( right_rear_ctrl, right_rear_loc )
		
		##rebuild the centroids
		cmds.delete( left_centroid )
		left_centroid = rivet.jpmMakeRivet( nurbs_plane, ("left_" + name ), 0.5,1 )[0]
		
		cmds.delete( right_centroid )
		right_centroid = rivet.jpmMakeRivet( nurbs_plane, ("right_" + name), 0.5,0 )[0]
		
		cmds.delete( center_centroid )
		center_centroid = rivet.jpmMakeRivet( nurbs_plane, ("center_" + name), 0.5,0.5 )[0]
		cmds.parent( center_centroid, centroid_offset_2 )
		
		allCentroids = [center_centroid, left_centroid, right_centroid]
	
	##Cleanup and group
	if not cmds.objExists("SKELETON"):
		skelGrp = cmds.group( name="SKELETON", empty=1 )
	else:
		skelGrp = "SKELETON"
		
	cmds.parent( centroid_offset_1, skelGrp )
	cmds.parent( left_centroid, skelGrp )
	cmds.parent( right_centroid, skelGrp )
	cmds.parent( allTopJnts, skelGrp )
	
	if not cmds.objExists("IK"):
	    ikGrp = cmds.group( name="IK", empty=1 )
	    cmds.parent( ikGrp, skelGrp )
	else:
		ikGrp = "IK"
	
	if len(allIK) > 0:
		cmds.parent( allIK, ikGrp )
	
	if not cmds.objExists("CONTROLS"):
		ctrlGrp = cmds.group( name="CONTROLS", empty=1 )
	else:
		ctrlGrp = "CONTROLS"
	
	if len(allCtrls) > 0:
		cmds.parent( allCtrls, ctrlGrp )
	
	return allJnts, allTopJnts,	allIK, allCtrls, allCentroids, allExpr