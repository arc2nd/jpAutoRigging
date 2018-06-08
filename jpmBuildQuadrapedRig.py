##James Parks
##Maya auto rigging functions.

import maya.cmds as cmds
import maya.mel as mm
import math
import os
import sys

import jpmArms as arms
import jpmCreateControls as ctrls
import jpmAutoClusterCurve as clsCrvs
import jpmCreateLimb as limbs
import helperFunctions as helper


def jpmBuildQuadrapedRig( armsFKIK, armsStretchy, armsSingle, armsRadius, arms4Joint, armsChicken, armsFingers, legsFKIK, legsStretchy, legsSingle ):
	##################
	##sorting
	##################
	grps = []
	geos = []
	crvs = []
	left = []
	right = []
	leftThumb = []
	leftIndex = []
	leftMiddle = []
	leftRing = []
	leftPinky = []
	leftUlna = []
	leftRadius = []
	leftChickenArms = []
	rightThumb = []
	rightIndex = []
	rightMiddle = []
	rightRing = []
	rightPinky = []
	rightUlna = []
	rightRadius = []
	rightChickenArms = []
	stabilize = []

	places = cmds.ls( "*_PLACE_*", tr=True, fl=True )
	for thisPlace in places:
		isFound = thisPlace.find("GRP")
		if str(isFound) != "-1":
			grps.append( thisPlace )
		isFound = thisPlace.find("GEO")
		if str(isFound) != "-1":
			geos.append( thisPlace )
		isFound = thisPlace.find("CRV")
		if str(isFound) != "-1":
			crvs.append( thisPlace )
		isFound = thisPlace.find("left")
		if str(isFound) != "-1":
			left.append( thisPlace )
		isFound = thisPlace.find("right")
		if str(isFound) != "-1":
			right.append( thisPlace )
		isFound = thisPlace.find("stabilize")
		if str(isFound) != "-1":
			stabilize.append( thisPlace )

	##Left Hand
	for thisPlace in left:
		isFound = thisPlace.find("thumb")
		if str(isFound) != "-1":
			leftThumb.append( thisPlace )
		isFound = thisPlace.find("index")
		if str(isFound) != "-1":
			leftIndex.append( thisPlace )
		isFound = thisPlace.find("middle")
		if str(isFound) != "-1":
			leftMiddle.append( thisPlace )
		isFound = thisPlace.find("ring")
		if str(isFound) != "-1":
			leftRing.append( thisPlace )
		isFound = thisPlace.find("pinky")
		if str(isFound) != "-1":
			leftPinky.append( thisPlace )
		isFound = thisPlace.find("ulna")
		if str(isFound) != "-1":
			leftUlna.append( thisPlace )
		isFound = thisPlace.find("radius")
		if str(isFound) != "-1":
			leftRadius.append( thisPlace )
		isFound = thisPlace.find("chickenArm")
		if str(isFound) != "-1":
			leftChickenArms.append( thisPlace )

	##Right Hand
	for thisPlace in right:
		isFound = thisPlace.find("thumb")
		if str(isFound) != "-1":
			rightThumb.append( thisPlace )
		isFound = thisPlace.find("index")
		if str(isFound) != "-1":
			rightIndex.append( thisPlace )
		isFound = thisPlace.find("middle")
		if str(isFound) != "-1":
			rightMiddle.append( thisPlace )
		isFound = thisPlace.find("ring")
		if str(isFound) != "-1":
			rightRing.append( thisPlace )
		isFound = thisPlace.find("pinky")
		if str(isFound) != "-1":
			rightPinky.append( thisPlace )
		isFound = thisPlace.find("ulna")
		if str(isFound) != "-1":
			rightUlna.append( thisPlace )
		isFound = thisPlace.find("radius")
		if str(isFound) != "-1":
			rightRadius.append( thisPlace )
		isFound = thisPlace.find("chickenArm")
		if str(isFound) != "-1":
			rightChickenArms.append( thisPlace )


	##################
	##Make Limb Skeletons
	##################

	##Define Anchor/Place points
	##leg anchors[] ==  hip-place, knee-place, ankle-place, ball-place, toe-place, heel-place 
	leftLegAnchors = [ "left_hip_PLACE_GEO", "left_knee_PLACE_GEO", "left_ankle_PLACE_GEO", "left_ball_PLACE_GEO", "left_toe_PLACE_GEO", "left_heel_PLACE_GEO" ]
	rightLegAnchors = [ "right_hip_PLACE_GEO", "right_knee_PLACE_GEO", "right_ankle_PLACE_GEO", "right_ball_PLACE_GEO", "right_toe_PLACE_GEO", "right_heel_PLACE_GEO" ]
	##arm anchors[] == clavicle-place, shoulder-place, elbow-place, wrist-place, hands[finger][joint]
	leftHand = [ leftThumb, leftIndex, leftMiddle, leftRing, leftPinky ]
	leftArmAnchors = [ "left_clavicle_PLACE_GEO", "left_shoulder_PLACE_GEO", "left_elbow_PLACE_GEO", "left_wrist_PLACE_GEO", leftHand, leftUlna, leftRadius ]
	rightHand = [ rightThumb, rightIndex, rightMiddle, rightRing, rightPinky ]
	rightArmAnchors = [ "right_clavicle_PLACE_GEO", "right_shoulder_PLACE_GEO", "right_elbow_PLACE_GEO", "right_wrist_PLACE_GEO", rightHand, rightUlna, rightRadius ]
	##spine anchors[] == waist-place, upperBody-place
	spineAnchors = [ "waist_PLACE_GEO", "upperBody_PLACE_GEO" ]
	
	
	leftLegJoints = limbs.createLimbJoints( "left", "leg", leftLegAnchors )
	rightLegJoints = limbs.createLimbJoints( "right", "leg", rightLegAnchors )

	leftArmJoints = limbs.createLimbJoints( "left", "arm", leftArmAnchors )
	rightArmJoints = limbs.createLimbJoints( "right", "arm", rightArmAnchors )

	shoulderGirdle = helper.makeObj( "SHOULDER_GIRDLE_GRP", "transform", "upperBody_PLACE_GEO", 0,0,0 )

	spineJoints = limbs.createLimbJoints( "", "spine", spineAnchors )

	cmds.parent( leftLegJoints[0], spineJoints[0] )
	cmds.parent( rightLegJoints[0], spineJoints[0] )
	cmds.parent( leftArmJoints[0], spineJoints[-1][-1] )
	cmds.parent( rightArmJoints[0], spineJoints[-1][-1] )



	##################
	##Joint Cleanup
	##################
	cmds.select( "*_JNT" )
	mm.eval( "jsOrientJoint 1" )
	#cmds.joint( e=True, oj="yxz", sao="xdown", zso=True )

	##################
	##Default Rig
	##################
	transCtrl, pivotCtrl = ctrls.jpmCreateDefaultRig()

	
	##################
	##Make Limb Controls
	##################
	leftLegControls = limbs.createLimbControls( "left", "leg", leftLegAnchors, leftLegJoints )
	rightLegControls = limbs.createLimbControls( "right", "leg", rightLegAnchors, rightLegJoints )

	leftArmControls = limbs.createLimbControls( "left", "arm", leftArmAnchors, leftArmJoints )
	rightArmControls = limbs.createLimbControls( "right", "arm", rightArmAnchors, rightArmJoints )

	shoulderGirdle = helper.makeObj( "SHOULDER_GIRDLE_GRP", "transform", "upperBody_PLACE_GEO", 0,0,0 )
	cmds.parent( leftArmControls, shoulderGirdle )
	cmds.parent( rightArmControls, shoulderGirdle )
	cmds.parent( shoulderGirdle, pivotCtrl )

	
	##Hands Parent Stuff
	leftWristCon = cmds.parentConstraint( leftArmControls[0], leftArmControls[1], mo=True )
	cmds.parentConstraint( pivotCtrl, leftArmControls[1], mo=True )
	rightWristCon = cmds.parentConstraint( rightArmControls[0], rightArmControls[1], mo=True )
	cmds.parentConstraint( pivotCtrl, rightArmControls[1], mo=True ) 

	cmds.addAttr( transCtrl, ln="handsParent", at="float",  min=0, max=1, dv=1 )
	cmds.setAttr( (transCtrl + ".handsParent"), e=True, keyable=True ) 

	cmds.connectAttr( (transCtrl + ".handsParent"), (leftWristCon[0] + ".w0") )
	cmds.connectAttr( (transCtrl + ".handsParent"), (rightWristCon[0] + ".w0") )
	revNode = cmds.shadingNode( "reverse", asUtility=True, n="hands_REV" )
	cmds.connectAttr( (transCtrl + ".handsParent"), (revNode + ".inputX") )
	cmds.connectAttr( (revNode + ".outputX"), (leftWristCon[0] + ".w1") )
	cmds.connectAttr( (revNode + ".outputX"), (rightWristCon[0] + ".w1") )

	spineControls = limbs.createLimbControls( "", "spine", spineAnchors, spineJoints )


	##################
	##Pole Vectors
	##################

	##################
	##Head CTRLs
	##################
	headGrp = helper.makeObj( "neck_GRP", "transform", "neck_PLACE_GEO", 0,0,0 )
	neckCtrl = helper.makeObj( "neck", "straightCompass", "neck_PLACE_GEO", 0,0,0 )
	headCtrl = helper.makeObj( "head", "cubeTwo", "head_PLACE_GEO", 0,0,0 )

	cmds.parent( headCtrl, neckCtrl )
	cmds.parent( neckCtrl, headGrp )

	##################
	##Do Mouth
	##################
	cmds.select( cl=True )
	cmds.select(crvs)
	clsCrvs.jpmACCurve(2, 2, 1)

	##################
	#Cleanup
	##################
	skelGrp = helper.makeObj( "SKELETON", "transform", "origin", 0,0,0 )
	defGrp = helper.makeObj( "DEFORMERS", "transform", "origin", 0,0,0 )

	cmds.parent( skelGrp, "WORLD" )
	cmds.parent( defGrp, "WORLD" )

	cmds.select( "*_PLACE_GEO" )
	cmds.delete()