anchors[0] = left_elbow_PLACE_GEO
anchors[1] = left_wrist_PLACE_GEO

def splitJoint(anchors=[]):
	forearmDist = helper.getDistance( anchors[0], anchors[1] )
	startPos = helper.getPositions( anchors[0] )
	numOfJoints = 3
	thisOffset = [forearmDist[1]/numOfJoints, forearmDist[2]/numOfJoints, forearmDist[3]/numOfJoints]
	forearmJoints = []
	for i in range(1,numOfJoints+1):
		thisName = ("foreArm" + str(i))
		thisPos = helper.addDistance(startPos, (thisOffset * 1))
		forearmJoints.append( helper.makeJoint( thisName, thisPos, "BIND" ) )
		#forearmJoints.append( helper.makeJoint( ("spine" + str(i)), helper.addDistance(startPos, (thisOffset * i), "BIND" ) )
		startPos = helper.addDistance(startPos, thisOffset)
	helper.multiParent( forearmJoints )
	#cmds.parent( forearmJoints[0], spineRootJnt )

	joints = [ forearmJoints ]
	return joints