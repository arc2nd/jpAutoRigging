import maya.cmds as cmds
import maya.mel as mm
import math
import os
import sys

#myPath = "//nitro.canary.media/tech/Python/jpmAutoRigging"
#os.chdir( myPath )
#myPath = os.getcwd()
#print myPath
#sys.path.append( myPath )

import jpmArms as arms
import jpmCreateControls as ctrls
#import jpmAutoClusterCurve as clsCrvs
import helperFunctions as helper


def createLimbJoints( side, limbType, anchors=[] ):
	if limbType == "leg":
		HipPlace = anchors[0]
		KneePlace = anchors[1]
		AnklePlace = anchors[2]
		BallPlace = anchors[3]
		ToePlace = anchors[4]
		HeelPlace = anchors[5]

		##anchors[] ==  hip-place, knee-place, ankle-place, ball-place, toe-place, heel-place 
		##################
		##Leg JNTs
		##################
		##
		HipJnt = helper.makeJoint( (side + "_hip"), HipPlace, "BIND" )
		KneeJnt = helper.makeJoint( (side + "_knee"), KneePlace, "BIND" )
		AnkleJnt = helper.makeJoint( (side + "_ankle"), AnklePlace, "BIND" )
		BallJnt = helper.makeJoint( (side + "_ball"), BallPlace, "BIND" )
		ToeJnt = helper.makeJoint( (side + "_toe"), ToePlace, "BIND" )
		helper.multiParent( (HipJnt, KneeJnt, AnkleJnt, BallJnt, ToeJnt) )

		joints = [ HipJnt, KneeJnt, AnkleJnt, BallJnt, ToeJnt ]
		return joints

	if limbType == "arm": 
		ClaviclePlace = anchors[0]
		ShoulderPlace = anchors[1]
		ElbowPlace = anchors[2]
		WristPlace = anchors[3]
		hands = anchors[4]
		UlnaOnePlace = anchors[5][0]
		UlnaTwoPlace = anchors[5][1]
		RadiusOnePlace = anchors[6][0]
		RadiusTwoPlace = anchors[6][1]

		##anchors[] == clavicle-place, shoulder-place, elbow-place, wrist-place, hands[finger][joint]
		##################
		##Arm JNTs
		##################
		##
		ClavicleJnt = helper.makeJoint( (side + "_clavicle"), ClaviclePlace, "BIND" )
		ShoulderJnt = helper.makeJoint( (side + "_shoulder"), ShoulderPlace, "BIND" ) 
		ElbowJnt = helper.makeJoint( (side + "_elbow"), ElbowPlace, "BIND" ) 
		ArmWristJnt = helper.makeJoint( (side + "_armWrist"), WristPlace, "BIND" ) 
		HandWristJnt = helper.makeJoint( (side + "_handWrist"), WristPlace, "BIND" ) 
		helper.multiParent( [ClavicleJnt, ShoulderJnt, ElbowJnt, ArmWristJnt, HandWristJnt] )

		UlnaJnt = helper.makeJoint( (side + "_ulna"), UlnaOnePlace, "BIND" )
		UlnaTipJnt = helper.makeJoint( (side + "_ulnaTip"), UlnaTwoPlace, "BIND" )
		cmds.parent( UlnaTipJnt, UlnaJnt )

		RadiusJnt = helper.makeJoint( (side + "_radius"), RadiusOnePlace, "BIND" )
		RadiusTipJnt = helper.makeJoint( (side + "_radiusTip"), RadiusTwoPlace, "BIND" )
		cmds.parent( RadiusTipJnt, RadiusJnt )

		cmds.parent( UlnaJnt, HandWristJnt )
		cmds.parent( RadiusJnt, HandWristJnt )

		##################
		##Hand JNTs
		##################
		newJoints = []
		#hands = [Thumb, Index, Middle, Ring, Pinky]
		for finger in hands:
			newJoints = []
			for joint in finger:
				thisJoint = helper.makeJoint( helper.parseNames(joint), joint, "BIND" )
				newJoints.append( thisJoint )
			helper.multiParent( newJoints )
			cmds.parent( newJoints[0], HandWristJnt )

		joints = [ ClavicleJnt, ShoulderJnt, ElbowJnt, ArmWristJnt, HandWristJnt, newJoints, [UlnaJnt, UlnaTipJnt], [RadiusJnt, RadiusTipJnt] ]
		return joints


	if limbType == "spine":
		WaistPlace = anchors[0]
		UpperBodyPlace = anchors[1]

		rootJnt = helper.makeJoint( "root", WaistPlace, "BIND" )
		hipRootJnt = helper.makeJoint( "hipRoot", WaistPlace, "BIND" )
		spineRootJnt = helper.makeJoint( "spineRoot", WaistPlace, "BIND" )
		cmds.parent( hipRootJnt, rootJnt)
		cmds.parent( spineRootJnt, rootJnt)

		##anchors[] == waist-place, upperBody-place
		##################
		##Spine JNTs
		##################
		spineDist = helper.getDistance( anchors[0], anchors[1] )
		startPos = helper.getPositions( anchors[0] )
		numOfJoints = 3
		thisOffset = [spineDist[1]/numOfJoints, spineDist[2]/numOfJoints, spineDist[3]/numOfJoints]
		spineJoints = []
		for i in range(1,numOfJoints+1):
			thisName = ("spine" + str(i))
			thisPos = helper.addDistance(startPos, (thisOffset * 1))
			spineJoints.append( helper.makeJoint( thisName, thisPos, "BIND" ) )
			#spineJoints.append( helper.makeJoint( ("spine" + str(i)), helper.addDistance(startPos, (thisOffset * i), "BIND" ) )
			startPos = helper.addDistance(startPos, thisOffset)
		helper.multiParent( spineJoints )
		cmds.parent( spineJoints[0], spineRootJnt )

		joints = [ rootJnt, hipRootJnt, spineRootJnt, spineJoints ]
		return joints




def createLimbControls(side=None, limbType=None, anchors=None, joints=None, FKIK=False, stretchy=False ):
	if limbType == "leg":	
		HipPlace = anchors[0]
		KneePlace = anchors[1]
		AnklePlace = anchors[2]
		BallPlace = anchors[3]
		ToePlace = anchors[4]
		HeelPlace = anchors[5]

		HipJnt = joints[0]
		KneeJnt = joints[1]
		AnkleJnt = joints[2]
		BallJnt = joints[3]
		ToeJnt = joints[4] 

		##anchors[] ==  hip-place, knee-place, ankle-place, ball-place, toe-place, heel-place 
		##################
		##Leg CTRLs
		##################
		FootGrp = helper.makeObj( (side + "_foot_GRP"), "transform", HipJnt, 0,0,0 )
		BallPiv = helper.makeObj( (side + "_ballPivot_GRP"), "transform", BallJnt, 0,0,0 )
		BallLift = helper.makeObj( (side + "_ballLift_GRP"), "transform", BallJnt, 0,0,0 )
		ToePiv = helper.makeObj( (side + "_toePivot_GRP"), "transform", BallJnt, 0,0,0 )
		
		AnkleCtrl = helper.makeObj( (side + "_Ankle"), "cubeTwo", AnkleJnt, 0,0,'180deg' )
		HeelCtrl = helper.makeObj( (side + "_Heel"), "cubeTwo", HeelPlace, 0,0,0 )
		ToeCtrl = helper.makeObj( (side + "_Toe"), "cubeTwo", ToeJnt, 0,0,0 )

		cmds.parent( FootGrp, "pivot_CTRL" )
		cmds.parent( AnkleCtrl, FootGrp )
		cmds.parent( HeelCtrl, AnkleCtrl )
		cmds.parent( ToeCtrl, HeelCtrl )
		cmds.parent( BallPiv, ToeCtrl )
		cmds.parent( ToePiv, BallPiv )
		cmds.parent( BallLift, BallPiv )

		##Channels
		channels = [ "ballLift", "ballPivot", "toeTap", "kneeTwist" ]
		helper.addChannels( AnkleCtrl, -90, 90, 0, channels )

		##IK
		ToeIK = cmds.ikHandle( n=(side + "Toe_IK"), sj=BallJnt, ee=ToeJnt )
		FootIK = cmds.ikHandle( n=(side + "Foot_IK"), sj=AnkleJnt, ee=BallJnt )
		LegIK = cmds.ikHandle( n=(side + "Leg_IK"), sj=HipJnt, ee=AnkleJnt )

		##IK Parenting
		cmds.parent( ToeIK[0], ToePiv )
		cmds.parent( FootIK[0], BallLift )
		cmds.parent( LegIK[0], BallLift )

		##Connections
		cmds.connectAttr( (AnkleCtrl + ".ballLift"), (BallLift + ".rotateX") ) 
		cmds.connectAttr( (AnkleCtrl + ".toeTap"), (ToePiv + ".rotateX") )
		cmds.connectAttr( (AnkleCtrl + ".ballPivot"), (BallPiv + ".rotateY") )

		if stretchy:
			arms.jpmTwoBoneStretch( "trans_CTRL", AnkleCtrl, HipJnt, KneeJnt, AnkleJnt, 5, 0, 1, 0 )

		return FootGrp

	#Arm Controls
	if limbType == "arm":
		ClaviclePlace = anchors[0]
		ShoulderPlace = anchors[1]
		ElbowPlace = anchors[2]
		WristPlace = anchors[3]
		hands = anchors[4]

		Thumb = anchors[4][0]
		Index = anchors[4][1]
		Middle = anchors[4][2]
		Ring = anchors[4][3]
		Pinky = anchors[4][4]

		ClavicleJnt = joints[0]
		ShoulderJnt = joints[1]
		ElbowJnt = joints[2]
		ArmWristJnt = joints[3]
		HandWristJnt = joints[4]
		handJoints = joints[5]
		UlnaJnt = joints[6]
		RadiusJnt = joints[7]

		##anchors[] == clavicle-place, shoulder-place, elbow-place, wrist-place, hands[finger][joint], Ulna, Radius
		##################
		##Arm CTRLs
		##################
		ShoulderCtrl = helper.makeObj( (side + "_shoulder"), "straightCompass", ShoulderJnt, 0,0,'90deg' )
		
		WristGrp = helper.makeObj( (side + "_wrist_GRP"), "transform", ShoulderJnt, 0,0,0 )
		WristCtrl = helper.makeObj( (side + "_wrist"), "angledCompass", HandWristJnt, 0,0,'90deg' )
		cmds.parent( WristCtrl, WristGrp )

		##################
		##Hand SDKs
		##################
		channels = ["spread", "thumb", "index", "middle", "ring", "pinky", "twist" ]
		helper.addChannels( WristCtrl, -10, 10, 0, channels )

		##hand :: fingers
		keys = [[0,0], [10,-90], [-10,90]]
		hands = [Thumb, Index, Middle, Ring, Pinky]
		channel = []
		for finger in hands:
			for joint in finger:
				joint = (helper.parseNames(joint) + "_BIND_JNT")
				if joint == finger[-1]:
					continue
				if joint.find("thumb") != -1:
					channel = "thumb"
				elif joint.find("index") != -1:
					channel = "index"
				elif joint.find("middle") != -1:
					channel = "middle"
				elif joint.find("ring") != -1:
					channel = "ring"
				elif joint.find("pinky") != -1:
					channel = "pinky"
				else:
					continue
				helper.addSDKs( (str(WristCtrl) + "." + str(channel)), (joint + ".rotateX"), keys )

		##hand :: spread
		keys = []
		for finger in hands:
			joint = (helper.parseNames(finger[0]) + "_BIND_JNT")
			if finger[0].find("thumb") != -1:
				keys = [[0,0],[10,-35],[-10,45]]
			elif finger[0].find("index") != -1:
				keys = [[0,0],[10,-50],[-10,50]]
			elif finger[0].find("middle") != -1:
				keys = [[0,0],[10,-15],[-10,15]]
			elif finger[0].find("ring") != -1:
				keys = [[0,0],[10,40],[-10,-20]]
			elif finger[0].find("pinky") != -1:
				keys = [[0,0],[10,55],[-10,-35]]
			else:
				continue
			helper.addSDKs( (str(WristCtrl) + ".spread"), (joint + ".rotateZ"), keys )

		#arms.jpmSingletonArm( "trans_CTRL", WristCtrl, ShoulderJnt, ElbowJnt, ArmWristJnt )
		if FKIK:
			ikJoints = arms.jpmIKFKArm( WristCtrl, ShoulderJnt, ElbowJnt, ArmWristJnt )
		else:
			limbIK = cmds.ikHandle(n=(str(ShoulderJnt) + "_IK"), sj=ShoulderJnt, ee=ArmWristJnt )
			cmds.parentConstraint( WristCtrl, limbIK[0], mo=True)
	
		if stretchy:
			arms.jpmTwoBoneStretch( "trans_CTRL", WristCtrl, ikJoints[0], ikJoints[1], ikJoints[2], 5, 0, 1, 0 )

		UlnaIK = cmds.ikHandle( n=(side + "Ulna_IK"), sj=UlnaJnt[0], ee=UlnaJnt[1] )
		RadiusIK = cmds.ikHandle( n=(side + "Radius_IK"), sj=RadiusJnt[0], ee=RadiusJnt[1] )

		return ShoulderCtrl, WristGrp

	if limbType == "spine":
		WaistPlace = anchors[0]
		UpperBodyPlace = anchors[1]

		rootJnt = joints[0]
		spineRootJnt = joints[1]
		hipRootJnt = joints[2]
		spineJoints = joints[3]
		##################
		##Waist CTRLs
		##################
		waistCtrl = helper.makeObj( "waist", "straightCompass", spineRootJnt, 0,0,0 )
		cmds.parentConstraint(  waistCtrl, spineRootJnt, mo=True )
		cmds.parent( waistCtrl, "pivot_CTRL" )

		hipCtrl = helper.makeObj( "hip", "straightCompass", spineRootJnt, 0,'45deg',0 )
		cmds.parentConstraint( hipCtrl, hipRootJnt, mo=True )
		cmds.parent( hipCtrl, "pivot_CTRL" )

	