import maya.cmds as cmds
import maya.mel as mm
import os
import sys

#myPath = "//nitro.canary.media/tech/Python/jpmAutoRigging"
#os.chdir( myPath )
#myPath = os.getcwd()
#print myPath
#sys.path.append( myPath )

import jpmArms as arms
import jpmCreateControls as ctrls
import jpmAutoClusterCurve as clsCrvs



#Helper Functions
def getPositions(object):
	thisType = cmds.ls( object, st=True )[1]
	if thisType != "joint":
		thisPos = cmds.objectCenter( cmds.listRelatives(object, s=True )[0], gl=True )
	else:
		#thisPos = cmds.objectCenter( object, gl=True)
		thisPos = cmds.xform(object, q=True, t=True, a=True, ws=True)
	return thisPos

def makeObj(name, objType, place, rotX, rotY, rotZ):
	if objType == "transform":
		thisObj = cmds.createNode( objType, n=name )
	elif objType == "pvArrow":
		thisObj = ctrls.jpmCreatePVArrow( name )
	elif objType == "pivot":
		thisObj = ctrls.jpmCreatePivotCTRLShape( name )
	elif objType == "topTrans":
		thisObj = ctrls.jpmCreateTopTransCTRLShape( name )
	elif objType == "cubeTwo":
		thisObj = ctrls.jpmCreateCubeTwoCTRLShape( name )
	elif objType == "straightCompass":
		thisObj = ctrls.jpmCreateStraightCompass( name )
	elif objType == "angledCompass":
		thisObj = ctrls.jpmCreateAngledCompass( name )
	elif objType == "cirlce":
		thisObj = cmds.circle( c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=1, ut=0, tol=0.01, s=16, ch=1, n=(name + "_CTRL") ) 
	elif objType == "triangle":
		thisObj = ctrls.jpmCreateTriangle( name )
	elif objType == "locator":
		thisObj = cmds.spaceLocator( n=name )
	if place != "origin":
		cmds.xform( thisObj, t=(getPositions( place )), a=True, ws=True )
	cmds.rotate( rotX, rotY, rotZ, thisObj, r=True, os=True )
	cmds.makeIdentity( thisObj, apply=True, t=1, r=1, s=1, n=2 )
	return thisObj

def setPositions(object, thisPos):
	cmds.xform(object, t=thisPos, a=True, ws=True)

##remove certain strings from an object name
def parseNames(object):
	parsed = ""
	removeTags = []
	theseTags = object.split("_")
	badTags = ["BIND", "PLACE", "JNT", "IK", "FK", "SINGLE", "CTRL", "GRP", "CTRLGRP", "GEO"]
	for tag in theseTags:
		for bad in badTags:
			if tag == bad:
				removeTags.append(tag)
	for tag in removeTags:
		theseTags.remove(tag)
	parsed = "_".join(theseTags)
	return parsed

##make a joint with the specified name, in the same spot as the specified object, with the specified tag string
def makeJoint( name, object, jntType ):
	print type(object)
	cmds.select( cl=True )
	if type(object) == type([]):
		print "Vector"
		cmds.select( cl=True )
		thisJoint = cmds.joint( p=object, n=(name + "_" + jntType + "_JNT") )
	#elif type(object) == type(""):
	else:
		print "String"
		thisPos = getPositions(object)
		##thisParse = parseNames(name)
		thisJoint = cmds.joint( p=thisPos, n=(name + "_" + jntType + "_JNT") )
		##thisJoint = cmds.joint( zso=True, p=thisPos, n=(name + "_" + jntType + "_JNT") )
	return thisJoint

def orientJoint( name ):
	cmds.makeIdentity( name, apply=1 )
	cmds.joint( name, e=1, oj="yzx", sao="yup", zso=1 )
	
##parent lots of objects in a string, one after the other
def multiParent( objects=[] ):
	for i in range(len(objects)):
		try:
			cmds.parent(objects[i+1], objects[i])
		except:
			print ""
			break

def getDistance( firstObj, secondObj ):
	import math

	firstPos = getPositions( firstObj )
	secondPos = getPositions( secondObj )

	deltaX = secondPos[0] - firstPos[0]
	deltaY = secondPos[1] - firstPos[1]
	deltaZ = secondPos[2] - firstPos[2]

	powX = pow( deltaX, 2 )
	powY = pow( deltaY, 2 )
	powZ = pow( deltaZ, 2 )

	distance = math.sqrt( powX + powY + powZ )
	return distance, deltaX, deltaY, deltaZ

def addDistance( firstPos, offset ):
	finalPos = [ firstPos[0]+offset[0], firstPos[1]+offset[1], firstPos[2]+offset[2] ]
	return finalPos

	
def midPoint( firstObj, secondObj ):
	initDist = getDistance( firstObj, secondObj )
	startPos = getPositions( firstObj )
	thisOffset = [initDist[1]/2, initDist[2]/2, initDist[3]/2]
	
	midPos = addDistance(startPos, thisOffset)
	
	return midPos	

##Add a channel to an object
def addChannels( control, thisMin, thisMax, thisDV, channels=[] ):
	for chan in channels:
		if thisMin == 0 and thisMax == 0:
			cmds.addAttr( control, ln=chan, at="float", hnv=False, hxv=False, dv=thisDV )
		else:
			cmds.addAttr( control, ln=chan, at="float", min=thisMin, max=thisMax, dv=thisDV )
		cmds.setAttr( (control + "." + chan), e=True, keyable=True )

##Create a Set Driven Key
def addSDKs( driver, driven, keys=[] ):
	startDriver = cmds.getAttr( driver )
	startDriven = cmds.getAttr( driven )
	for key in keys:
		cmds.setAttr( driver, key[0] )
		cmds.setAttr( driven, key[1] )
		cmds.setDrivenKeyframe( driven, cd=driver )
	cmds.setAttr( driver, startDriver )
	cmds.setAttr( driven, startDriven )


##split one joint up into multiple
def splitJoint(name, numOfJoints, anchors=[]):
	initDist = self.getDistance( anchors[0], anchors[1] )
	startPos = self.getPositions( anchors[0] )
	#numOfJoints = 3
	thisOffset = [initDist[1]/numOfJoints, initDist[2]/numOfJoints, initDist[3]/numOfJoints]
	splitJoints = []
	splitJoints.append( self.makeJoint( (name + "0"), startPos, "BIND") )
	for i in range(1,numOfJoints+1):
		thisName = (name + str(i))
		thisPos = self.addDistance(startPos, (thisOffset * 1))
		splitJoints.append( self.makeJoint( thisName, thisPos, "BIND" ) )
		#splitJoints.append( self.makeJoint( ("spine" + str(i)), self.addDistance(startPos, (thisOffset * i), "BIND" ) )
		startPos = self.addDistance(startPos, thisOffset)
	self.multiParent( splitJoints )
	#cmds.parent( splitJoints[0], spineRootJnt )

	joints = [ splitJoints ]
	return joints

##read lines in from a file on disk
def jpReadLines( fileToRead):
	lines = []
	badLines = []

	if os.path.exists(fileToRead) == False:
		print "File Not Found"
	else:
		thisFile = file(fileToRead, "r+")
		badLines = thisFile.readlines()
		thisFile.close()
	for i in range(0, len(badLines)):
		lines.append(badLines[i].strip())
	return lines

##read a whole file in from disk
def jpReadFile(fileToRead):
	readFile = ""
	badFile = ""
	
	if os.path.exists(fileToRead) == False:
		print "File Not Found"
	else:
		thisFile = file(fileToRead, "r+")
		badFile = thisFile.read()
		thisFile.close()
	readFile = badFile.strip()
	return readFile
