##James Parks
##Maya arm building functions.

##PATTERN
## Ribbon IK Joints
##	--Singleton Joints
##		--Placement Joints
##			-- FK/IK Switch Joints



import maya.cmds as cmds
import maya.mel as mm


def jpmSingletonArm( mainControl, control, root, flex, end ):
	##Find Joints
	rootPos = getPositions( root )
	flexPos = getPositions( flex )
	endPos = getPositions( end )

	rootParse = parseNames( root )
	flexParse = parseNames( flex )
	endParse = parseNames( end )

	cmds.select( cl=True )

	##Make Joints
	rootSingle = cmds.joint( oj="yxz", sao="xdown", zso=True, p=rootPos, n=(str(rootParse) + "_SINGLE_JNT") )
	flexSingle = cmds.joint( oj="yxz", sao="xdown", zso=True, p=flexPos, n=(str(flexParse) + "_SINGLE_JNT") )
	endSingle = cmds.joint( oj="yxz", sao="xdown", zso=True, p=endPos, n=(str(endParse) + "_SINGLE_JNT") )

	cmds.select( rootSingle )
	cmds.joint( e=True, oj="yxz", sao="xdown", zso=True, ch=True )
	cmds.select( cl=True )

	##Make Controls
	flexCtrl = cmds.circle( n=(flexParse + "_SINGLE_CTRL"), c=flexPos, fp=flexPos, fc=True, r=1, ch=False, nr=[0,1,0])
	mm.eval( "CenterPivot" )
	cmds.addAttr( flexCtrl[0], ln="switch", at="float",  min=0, max=1, dv=1 )
	cmds.setAttr( (flexCtrl[0] + ".switch"), e=True, keyable=True )
	endCtrl = cmds.circle( n=(endParse + "_SINGLE_CTRL"), c=endPos, fp=endPos, fc=True, r=1, ch=False, nr=[0,1,0])
	mm.eval( "CenterPivot" )

	print str(flexCtrl)
	cmds.select( cl=True )

	##Make IK
	flexIK = cmds.ikHandle( n=(str(flexParse) + "_IK"), sj=rootSingle, ee=flexSingle )
	endIK = cmds.ikHandle( n=(str(endParse) + "_IK"), sj=flexSingle, ee=endSingle )
	cmds.parentConstraint( flexCtrl, flexIK[0] )
	cmds.parentConstraint( endCtrl, endIK[0] )

	##Make Stretchy
	flexLoc = jpmSingleStretch( mainControl, flexCtrl[0], rootSingle, flexSingle, 10, 0, 1, 0 )
	endLoc = jpmSingleStretch( mainControl, endCtrl[0], flexSingle, endSingle, 10, 0, 1, 0 )

	cmds.parent( flexLoc, flexCtrl )
	cmds.parent( endLoc, control )

	flexGrp = cmds.group( flexCtrl, n=(str(flexParse) + "_CTRLGRP"), r=True )
	mm.eval( "CenterPivot" )
	endGrp = cmds.group( endCtrl, n=(str(endParse) + "_CTRLGRP"), r=True )
	mm.eval( "CenterPivot" )
	flexCon = cmds.parentConstraint( flex, flexGrp, mo=True )
	cmds.parentConstraint( root, flexGrp, mo=True )
	cmds.parentConstraint( end, endGrp, mo=True )

	revNode = cmds.shadingNode( "reverse", asUtility=True, n=(flexParse + "_REV") )
	cmds.connectAttr( (flexCtrl[0] + ".switch"), (revNode + ".inputX") )
	cmds.connectAttr( (flexCtrl[0] + ".switch"), (flexCon[0] + "." + flex + "W0") )
	cmds.connectAttr( (revNode + ".outputX"), (flexCon[0] + "." + root + "W1") )

	cmds.setAttr( (flexCon[0] + ".interpType"), 2 )


def jpmIKFKArm( control, root, flex, end ):
	rootPos = getPositions( root )
	flexPos = getPositions( flex )
	endPos = getPositions( end )

	rootParse = parseNames( root )
	flexParse = parseNames( flex )
	endParse = parseNames( end )
	controlParse = parseNames( control )

	cmds.select( cl=True )
	rootIK = cmds.joint( p=rootPos, n=(str(rootParse) + "_IK_JNT") )
	flexIK = cmds.joint( p=flexPos, n=(str(flexParse) + "_IK_JNT") )
	endIK = cmds.joint( p=endPos, n=(str(endParse) + "_IK_JNT") )
	cmds.joint( rootIK, oj="yxz", sao="zup", zso=True, e=1)
	cmds.joint( flexIK, oj="yxz", sao="zup", zso=True, e=1)
	cmds.joint( endIK, oj="yxz", sao="zup", zso=True, e=1)



	##cmds.select( rootIK) 
	##cmds.joint( e=True, oj="yxz", sao="xdown", ch=True, zso=True )
	##cmds.select( cl=True )

	cmds.select( cl=True )
	rootFK = cmds.joint( p=rootPos, n=(str(rootParse) + "_FK_JNT") )
	flexFK = cmds.joint( p=flexPos, n=(str(flexParse) + "_FK_JNT") )
	endFK = cmds.joint( p=endPos, n=(str(endParse) + "_FK_JNT") )
	cmds.joint( rootFK, oj="yxz", sao="zup", zso=True, e=1)
	cmds.joint( flexFK, oj="yxz", sao="zup", zso=True, e=1)
	cmds.joint( endFK, oj="yxz", sao="zup", zso=True, e=1)

	#cmds.select( rootFK )
	#cmds.joint( e=True, oj="yxz", sao="xdown", ch=True, zso=True )
	#cmds.select( cl=True )

	##Make Controls
	rootCtrl = cmds.circle( n=(rootParse + "_FK_CTRL"), c=rootPos, fp=rootPos, fc=True, r=1, ch=False, nr=[0,1,0] )
	mm.eval( "CenterPivot" )
	flexCtrl = cmds.circle( n=(flexParse + "_FK_CTRL"), c=flexPos, fp=flexPos, fc=True, r=1, ch=False, nr=[0,1,0] )
	mm.eval( "CenterPivot" )
	endCtrl = cmds.circle( n=(endParse + "_FK_CTRL"), c=endPos, fp=endPos, fc=True, r=1, ch=False, nr=[0,1,0] )
	mm.eval( "CenterPivot" )

	cmds.parent( flexCtrl, rootCtrl )
	cmds.parent( endCtrl, flexCtrl )

	cmds.parentConstraint( rootCtrl, rootFK, mo=True )
	cmds.parentConstraint( flexCtrl, flexFK, mo=True )
	cmds.parentConstraint( endCtrl, endFK, mo=True )

	cmds.select( cl=True )

	##Make IK
	limbIK = cmds.ikHandle( n=(str(rootParse) + "_IK"), sj=rootIK, ee=endIK )
	cmds.parentConstraint( control, limbIK[0], mo=True)

	##Add Attributes
	cmds.select ( cl=True )
	cmds.addAttr( control, ln="FkIk", at="float",  min=0, max=1, dv=1 )
	cmds.setAttr( (control + ".FkIk"), e=True, keyable=True )

	##Make Constraints and Connections
	rootCon = cmds.parentConstraint( rootIK, root, mo=True )
	flexCon = cmds.parentConstraint( flexIK, flex, mo=True )
	endCon = cmds.parentConstraint( endIK, end, mo=True )
	cmds.parentConstraint( rootFK, root, mo=True )
	cmds.parentConstraint( flexFK, flex, mo=True )
	cmds.parentConstraint( endFK, end, mo=True )

	revNode = cmds.shadingNode( "reverse", asUtility=True, n=(controlParse + "_REV") )
	cmds.connectAttr( (control + ".FkIk"), (revNode + ".inputX") )
	cmds.connectAttr( (revNode + ".outputX"), (rootCon[0] + "." + rootFK + "W1") )
	cmds.connectAttr( (revNode + ".outputX"), (flexCon[0] + "." + flexFK + "W1") )
	cmds.connectAttr( (revNode + ".outputX"), (endCon[0] + "." + endFK + "W1") )

	cmds.connectAttr( (control + ".FkIk"), (rootCon[0] + "." + rootIK + "W0") )
	cmds.connectAttr( (control + ".FkIk"), (flexCon[0] + "." + flexIK + "W0") )
	cmds.connectAttr( (control + ".FkIk"), (endCon[0] + "." + endIK + "W0") )

	cmds.connectAttr( (revNode + ".outputX"), (rootCtrl[0] + ".visibility") )
	cmds.connectAttr( (revNode + ".outputX"), (flexCtrl[0] + ".visibility") )
	cmds.connectAttr( (revNode + ".outputX"), (endCtrl[0] + ".visibility") )

	return rootIK, flexIK, endIK


temp = """
def jpmRibbonIKArm( name, root, end ):
	cmds.select( cl=True )

	##################
	##Make the joints
	##################
	firstJointName = (name + "_firstRibbon_JNT")
	firstJoint = cmds.joint( p=(0,0,0), n=firstJointName )
	secondJointName = (name + "_secondRibbon_JNT")
	secondJoint = cmds.joint( -p 1 0 0 -name secondJointName )
	cmds.joint( -e -zso -oj xyz -sao yup firstJoint )

	cmds.select( cl=True )

	thirdJointName = (name + "_thirdRibbon_JNT")
	thirdJoint = cmds.joint( -p 0 0 0 -name thirdJointName )
	fourthJointName = (name + "_fourthRibbon_JNT")
	fourthJoint = cmds.joint( -p 1 0 0 -name fourthJointName )
	cmds.joint( -e -zso -oj xyz -sao yup thirdJoint )

	##################
	##Make the IK handles
	##################
	cmds.select -r (firstJoint + ".rotatePivot") 
	cmds.select -add (secondJoint + ".rotatePivot") 
	firstIKName = (name + "_firstRibbon_IK")
	firstIK[] = cmds.ikHandle( -s sticky -name firstIKName )

	cmds.select -r (thirdJoint + ".rotatePivot") 
	cmds.select -add (fourthJoint + ".rotatePivot") 
	secondIKName = (name + "_secondRibbon_IK") 
	secondIK[] = cmds.ikHandle( -s sticky -name secondIKName )

	##################
	##Make the upVectors
	##################
	tmpUpVector = cmds.spaceLocator()
	firstUpVector = cmds.rename( tmpUpVector[0], (name + "_firstUpVector") )
	cmds.parent( firstUpVector, firstJoint )
	cmds.select( cl=True )
	cmds.select( firstUpVector )
	cmds.select( add=firstIK[0] )
	cmds.poleVectorConstraint( w=1 )
	cmds.setAttr( (firstUpVector + ".translateY"), 1 )
	cmds.setAttr( (firstUpVector + ".scale"), (0.1,0.1,0.1) )

	tmpUpVector[] = cmds.spaceLocator()
	secondUpVector = cmds.rename( tmpUpVector[0], (name + "_secondUpVector") )
	jpConstraintSnap(thirdJoint, secondUpVector)
	cmds.parent( secondUpVector, thirdJoint )
	cmds.select( cl=True )
	cmds.select( secondUpVector )
	cmds.select( add=secondIK[0] )
	cmds.poleVectorConstraint( w=1 )
	cmds.setAttr( (secondUpVector + ".translateY"), 1 )
	cmds.setAttr( (secondUpVector + ".scale"), (0.1,0.1,0.1) )

	##################
	##Make center joint
	##################
	cmds.select( cl=True )
	centerJointName = ($name + "_centerRibbon_JNT")
	centerJoint = cmds.joint( p=(0,0,0), n=centerJointName )

	##################
	##Place joints
	##################
	jpConstraintSnap(startJoint, firstJoint)
	jpConstraintSnap(endJoint, thirdJoint)
	cmds.setAttr( (firstJoint + ".scale"), (1,1,1) )
	cmds.setAttr( (thirdJoint + ".scale"), (1,1,1) )

	cmds.select( cl=True )
	cmds.select( firstJoint )
	cmds.select( add=thirdJoint )
	tempOrient = cmds.orientConstraint( offset=(0,0,0), w=1 )
	cmds.delete( tempOrient[0] )

	cmds.select( firstJoint )
	cmds.select( add=centerJoint )
	constraint = cmds.parentConstraint( w=1 )

	cmds.select( thirdJoint )
	cmds.select( add=centerJoint )
	cmds.parentConstraint( w=1 )

	cmds.delete( constraint[0] )

	jpConstraintSnap(centerJoint, firstIK[0])
	jpConstraintSnap(centerJoint, secondIK[0])

	##################
	##Create center control
	##################
	string $centerCTRLName = ($name + "_Ribbon_CTRL");
	string $centerCTRLs[] = `circle -c 0 0 0 -nr 1 0 0 -sw 360 -r 1 -d 1 -ut 0 -tol 0.01 -s 16 -ch 1 -name $centerCTRLName`; 
	jpConstraintSnap($centerJoint, $centerCTRLs[0]);
	cmds.select -clear;
	cmds.select $firstJoint;
	cmds.select -add $centerCTRLs[0];
	string $tempOrient[] = `orientConstraint -offset 0 0 0 -w 1`;
	cmds.delete $tempOrient[0];
	cmds.select $centerCTRLs;
	cmds.makeIdentity -apply true -t 1 -r 1 -s 1;
	cmds.parent $firstIK[0] $centerJoint;
	cmds.parent $secondIK[0] $centerJoint;

	cmds.select $centerCTRLs[0];
	cmds.select -add $centerJoint;
	cmds.parentConstraint -weight 1;
	cmds.scaleConstraint -weight 1;

	##################
	##Clean up and Group thingies
	##################
	string $centerGRP = `group $centerJoint`;// -name "centerJoint_GRP"`;
	$centerGRP = `rename $centerGRP ($name + "_Ribbon_CenterGRP")`;
	string $controlGRP = `group $centerCTRLs[0]`;// -name "controlOffset_GRP";
	$controlGRP = `rename $controlGRP ($name + "_Ribbon_CTRLGRP")`;
	cmds.select -clear;
	cmds.select $startJoint;
	cmds.select -add $controlGRP;
	cmds.parentConstraint -mo -w 1;
	string $allGRP = `group $centerGRP $firstJoint $thirdJoint`;// -name "ribbonJoint_GRP"`;
	$allGRP = `rename $allGRP ($name + "_Ribbon_JNTGRP")`;
	cmds.parent $allGRP $startJoint;
	cmds.parent $firstUpVector $allGRP;
	cmds.parent $secondUpVector $allGRP;

	##################
	##Time to make the Ribbon
	##################
	float $startPos[] = `xform -q -a -ws -t $startJoint`;
	float $endPos[] = `xform -q -a -ws -t $endJoint`;
	string $distance = jpDistance($startPos, $endPos);

	string $ribbonName = ($name + "_Ribbon");
	string $ribbon[] =`nurbsPlane -p 0 0 0 -ax 0 1 0 -w $distance -lr .1 -d 3 -u 5 -v 1 -ch 0 -name $ribbonName`;
	jpConstraintSnap($firstIK[0], $ribbon[0]);
	cmds.select -clear;
	cmds.select $firstJoint;
	cmds.select -add $ribbon[0];
	string $tempOrient[] = `orientConstraint -offset 0 0 0 -w 1`;
	cmds.delete $tempOrient[0];
	cmds.select $ribbon[0];
	cmds.makeIdentity -apply true -t 1 -r 1 -s 1;

	cmds.select( cl=True )
	cmds.select( (firstJoint, thirdJoint, centerJoint, ribbon[0]) )
	ribbonSkin = cmds.skinCluster( n=(name + "_RibbonSkinCluster"), tsb=True, dr=10, mi=5 )

	##################
	##Paint Weights
	##################
	cmds.skinPercent( tv=(centerJoint) 0 (ribbonSkin[0]) (ribbon[0] + ".cv[0][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0.1 (ribbonSkin[0]) (ribbon[0] + ".cv[1][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0.3 (ribbonSkin[0]) (ribbon[0] + ".cv[2][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0.75 (ribbonSkin[0]) (ribbon[0] + ".cv[3][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0.75 (ribbonSkin[0]) (ribbon[0] + ".cv[4][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0.3 (ribbonSkin[0]) (ribbon[0] + ".cv[5][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0.1 (ribbonSkin[0]) (ribbon[0] + ".cv[6][0:3]") )
	cmds.skinPercent( tv=(centerJoint) 0 (ribbonSkin[0]) (ribbon[0] + ".cv[7][0:3]") )

	cmds.skinPercent( tv=(firstJoint) 0.90 (ribbonSkin[0]) (ribbon[0] + ".cv[1][0:3]") )
	cmds.skinPercent( tv=(firstJoint) 0.70 (ribbonSkin[0]) (ribbon[0] + ".cv[2][0:3]") )
	cmds.skinPercent( tv=(firstJoint) 0.25 (ribbonSkin[0]) (ribbon[0] + ".cv[3][0:3]") )
	cmds.skinPercent( tv=(firstJoint) 0 (ribbonSkin[0]) (ribbon[0] + ".cv[4][0:3]") )

	cmds.skinPercent( tv=(thirdJoint) 0.25 (ribbonSkin[0]) (ribbon[0] + ".cv[4][0:3]") )
	cmds.skinPercent( tv=(thirdJoint) 0.70 (ribbonSkin[0]) (ribbon[0] + ".cv[5][0:3]") )
	cmds.skinPercent( tv=(thirdJoint) 0.90 (ribbonSkin[0]) (ribbon[0] + ".cv[6][0:3]") )
	cmds.skinPercent( tv=(thirdJoint) 1.0 (ribbonSkin[0]) (ribbon[0] + ".cv[7][0:3]") )

	numOfDivs = 5.0

	for i in range(numOfDivs):
		##Create Rivets
		float $division = (1/($numOfDivs-1)) * $i;
		cmds.select -r ($ribbon[0] + ".uv[" + $division + "][.5]");
		$rivetNames[$i] = `rivet`;
		$rivetNames[$i] = `rename $rivetNames[$i] ($name + "_" + $i + "_RIVET")`;
		cmds.setAttr ($rivetNames[$i] + ".scale") 0.1 0.1 0.1;
		
		##Create Joints
		string $thisJointName = ($name + "_" + $i + "_BIND_JNT"); 
		string $thisJoint = `joint -p 0 0 0 -name $thisJointName`;
		jpConstraintSnap($rivetNames[$i], $thisJoint);
	##	parent $thisJoint $rivetNames[$i];

		##Create Controls
		string $rivetCTRLName = ($name + "_" + $i + "_Ribbon_CTRL");
		string $rivetCTRLs[] = `circle -c 0 0 0 -nr 1 0 0 -sw 360 -r 1 -d 1 -ut 0 -tol 0.01 -s 16 -ch 1 -name $rivetCTRLName`; 
		jpConstraintSnap($thisJoint, $rivetCTRLs[0]);
		cmds.select -clear;
		cmds.select $rivetNames[$i];
		cmds.select -add $rivetCTRLs[0];
		string $tempOrient[] = `orientConstraint -offset 0 0 0 -w 1`;
		cmds.delete $tempOrient[0];
		cmds.select $rivetCTRLs;
		cmds.makeIdentity -apply true -t 1 -r 1 -s 1;

		string $rivetOffsetGRP = `group $rivetCTRLs`;
		$rivetOffsetGRP = `rename $rivetOffsetGRP ($name + "_" + $i + "_OffsetGRP")`;
		cmds.select -clear;
		cmds.select $rivetNames[$i];
		cmds.select -add $rivetOffsetGRP;
		cmds.parentConstraint( mo=True, w=1 )
		cmds.scaleConstraint( mo=True, w=1 )
		cmds.parent $rivetOffsetGRP $centerCTRLs[0];
		cmds.select $rivetCTRLs[0];
		mm.eval( "DeleteHistory" )

		cmds.select( cl=True )
		cmds.select $rivetCTRLs[0];
		cmds.select -add $thisJoint;
		cmds.parentConstraint( mo=True, w=1 )
		cmds.scaleConstraint( mo=True, w=1 )
"""

def jpmSingleStretch( mainControl, control, root, end, maxStretch, x, y, z ):
	##Add Attributes
	cmds.select ( cl=True )
	cmds.addAttr( control, ln="autoStretchy", at="long",  min=0, max=1, dv=1 )
	cmds.setAttr( (control + ".autoStretchy"), e=True, keyable=True )
	cmds.addAttr( control, ln="manualStretchy", at="float", min=1, dv=1 )
	cmds.setAttr( (control + ".manualStretchy"), e=True, keyable=True )
	cmds.addAttr( control, ln="minStretchy", at="double", min=1, dv=0 )
	cmds.setAttr( (control + ".minStretchy"), e=True, keyable=True )
	cmds.addAttr( control, ln="maxStretchy", at="double", min=1, dv=maxStretch )
	cmds.setAttr( (control + ".maxStretchy"), e=True, keyable=True )

	rootPos = cmds.xform( root, q=True, a=True, ws=True, t=True )
	#print rootPos
	endPos = cmds.xform( end, q=True, a=True, ws=True, t=True )
	#print endPos

	##find the initial distance
	jointDistanceNode = cmds.distanceDimension( sp=rootPos, ep=endPos )
	initialDistance = cmds.getAttr( (jointDistanceNode + ".distance") )

	#########################
	##Do that stretchy thing -- make the stretchy nodes
	########################
	##	make the dimension node and find out the names of the locators it made
	jointDistNodeStartLocShape = cmds.connectionInfo( (jointDistanceNode + ".startPoint"), sfd=True )
	jointDistNodeStartLocShape = jointDistNodeStartLocShape.split(".")[0]
	cmds.select( jointDistNodeStartLocShape )
	startLoc = cmds.pickWalk( d="up" )

	jointDistNodeEndLocShape = cmds.connectionInfo( (jointDistanceNode + ".endPoint"), sfd=True )
	jointDistNodeEndLocShape = jointDistNodeEndLocShape.split(".")[0]
	cmds.select( jointDistNodeEndLocShape )
	endLoc = cmds.pickWalk( d="up" )

	cmds.parent( startLoc, root )
	cmds.parent( endLoc, control )

	##make the utility nodes and connections
	##	multiply initial distance by current scale
	mainScaleNode = cmds.shadingNode( "multiplyDivide", asUtility=True, n=(mainControl + "_MD") )
	cmds.setAttr( (mainScaleNode + ".input1X"), initialDistance )
	cmds.setAttr( (mainScaleNode + ".input1Y"), initialDistance )
	cmds.setAttr( (mainScaleNode + ".input1Z"), initialDistance )
	cmds.connectAttr( (mainControl + ".scaleX"), (mainScaleNode + ".input2X") )
	cmds.connectAttr( (mainControl + ".scaleY"), (mainScaleNode + ".input2Y") )
	cmds.connectAttr( (mainControl + ".scaleZ"), (mainScaleNode + ".input2Z") )

	##	divide current distance by initial distance
	scaleNode = cmds.shadingNode( "multiplyDivide", asUtility=True, n=(control + "_MD") )
	cmds.setAttr( (scaleNode + ".operation"), 2 )

	cmds.connectAttr( (mainScaleNode + ".outputX"), (scaleNode + ".input2X") )
	cmds.connectAttr( (mainScaleNode + ".outputY"), (scaleNode + ".input2Y") )
	cmds.connectAttr( (mainScaleNode + ".outputZ"), (scaleNode + ".input2Z") )

	cmds.connectAttr( (jointDistanceNode + ".distance"), (scaleNode + ".input1X") )
	cmds.connectAttr( (jointDistanceNode + ".distance"), (scaleNode + ".input1Y") )
	cmds.connectAttr( (jointDistanceNode + ".distance"), (scaleNode + ".input1Z") )


	##	auto/manual stretch condition
	autoStretchConditionNode = cmds.shadingNode("condition", asUtility=True, n=(control + "_autoStretchCon") )
	cmds.connectAttr( (control + ".autoStretchy"), (autoStretchConditionNode + ".firstTerm") )
	cmds.setAttr( (autoStretchConditionNode + ".secondTerm"), .5 )
	cmds.setAttr( (autoStretchConditionNode + ".operation"), 2 )
	cmds.connectAttr( (scaleNode + ".outputX"), (autoStretchConditionNode + ".colorIfTrueR") )
	cmds.connectAttr( (scaleNode + ".outputY"), (autoStretchConditionNode + ".colorIfTrueG") )
	cmds.connectAttr( (scaleNode + ".outputZ"), (autoStretchConditionNode + ".colorIfTrueB") )

	cmds.connectAttr( (control + ".manualStretchy"), (autoStretchConditionNode + ".colorIfFalseR") )
	cmds.connectAttr( (control + ".manualStretchy"), (autoStretchConditionNode + ".colorIfFalseG") )
	cmds.connectAttr( (control + ".manualStretchy"), (autoStretchConditionNode + ".colorIfFalseB") )


	##	clamp scale between 0 and maxStretch
	clampNode = cmds.shadingNode( "clamp", asUtility=True, n=(control + "_clamp") )
	cmds.setAttr( (clampNode + ".minR"), 0 )
	cmds.setAttr( (clampNode + ".minG"), 0 )
	cmds.setAttr( (clampNode + ".minB"), 0 )

	cmds.connectAttr( (control + ".maxStretchy"), (clampNode + ".maxR") )
	cmds.connectAttr( (control + ".maxStretchy"), (clampNode + ".maxG") )
	cmds.connectAttr( (control + ".maxStretchy"), (clampNode + ".maxB") )
	cmds.connectAttr( (control + ".minStretchy"), (clampNode + ".minR") )
	cmds.connectAttr( (control + ".minStretchy"), (clampNode + ".minG") )
	cmds.connectAttr( (control + ".minStretchy"), (clampNode + ".minB") )

	cmds.connectAttr( (autoStretchConditionNode + ".outColor"), (clampNode + ".input") )

	##	connect to the joints scale
	if(x == 1):
		cmds.connectAttr( (clampNode + ".outputR"), (root + ".scaleX") )
	if(y == 1):
		cmds.connectAttr( (clampNode + ".outputG"), (root + ".scaleY") )
	if(z == 1):
		cmds.connectAttr( (clampNode + ".outputB"), (root + ".scaleZ") )

	#Cleanup
#	cmds.rename( jointDistanceNode, (root + "_DD") )
	return endLoc

temp = """
def jpmSplineStretch( mainControl, curve, root, end, maxStretch, x, y, z):
	##prep the control to receive stretcy-ness
	cmds.select( cl=True )
	cmds.select( mainControl )
	if(!cmds.attributeExists( "autoStretchy", mainControl ) ):
		cmds.addAttr( mainControl, ln="autoStretchy", at="long", min=0, max=1, dv=1 )
		cmds.setAttr( ($mainControl + ".autoStretchy"), e=True, keyable=True )
	if(!cmds.attributeExists( "maxStretchy", mainControl ) ):
		cmds.addAttr( mainControl, ln="maxStretchy", at="long", min=1, dv=maxStretch )
		cmds.setAttr( ($mainControl + ".maxStretchy"), e=True, keyable=True )
	
	##	dupe the splineIKcurve for a reference length
	baselineCurve = cmds.duplicate( n=(curve + "_baseline"), curve )

	##	make and connect the curveInfo nodes to find the lengths
	activeLength = cmds.createNode( "curveInfo", n=(curve + "_CI") )
	baselineLength = cmds.createNode( "curveInfo", n=(baselineCurve[0] + "_CI") )

	cmds.connectAttr( (curve + ".worldSpace[0]"), (activeLength + ".inputCurve") )
	cmds.connectAttr( (baselineCurve[0] + ".worldSpace[0]"), (baselineLength + ".inputCurve") )

	##	compare the lengths 
	multiplyDivide = cmds.shadingNode( "multiplyDivide", asUtility=True, n=(curve + "_MD") )
	cmds.setAttr( (multiplyDivide + ".operation"), 2 )
	cmds.setAttr( (multiplyDivide + ".input1Y"), 1 )
	cmds.setAttr( (multiplyDivide + ".input1Z"), 1 )

	cmds.connectAttr( (activeLength + ".arcLength"), (multiplyDivide + ".input1X") )
	cmds.connectAttr( (baselineLength + ".arcLength"), (multiplyDivide + ".input2X") )


	##clamp to greater than 1
	clampNode = cmds.shadingNode( "clamp", asUtility=True, n=(curve + "_clamp") )
	cmds.connectAttr( (multiplyDivide + ".output"), (clampNode + ".input") )

	cmds.setAttr( (clampNode + ".minR"), 1 )
	cmds.setAttr( (clampNode + ".minG"), 1 )
	cmds.setAttr( (clampNode + ".minB"), 1 )

	cmds.connectAttr( (mainControl + ".maxStretchy"), (clampNode + ".maxR") )
	cmds.connectAttr( (mainControl + ".maxStretchy"), (clampNode + ".maxG") )
	cmds.connectAttr( (mainControl + ".maxStretchy"), (clampNode + ".maxB") )


	##	auto/manual stretch condition
	autoStretchConditionNode = cmds.shadingNode( "condition", asUtility=True, n=(mainControl + "_autoStretchCon") )
	cmds.connectAttr( (mainControl + ".autoStretchy"), (autoStretchConditionNode + ".firstTerm") )
	cmds.setAttr( (autoStretchConditionNode + ".secondTerm"), .5 )
	cmds.setAttr( (autoStretchConditionNode + ".operation"), 2 )

	cmds.connectAttr( (clampNode + ".output"), (autoStretchConditionNode + ".colorIfTrue") )
	
	cmds.setAttr( (autoStretchConditionNode + ".colorIfFalseR"), 1 )
	cmds.setAttr( (autoStretchConditionNode + ".colorIfFalseG"), 1 )
	cmds.setAttr( (autoStretchConditionNode + ".colorIfFalseB"), 1 )



	##make an intermediate locator for scale
	scaleLoc = cmds.spaceLocator( n=(curve + "_scale_loc") )
	cmds.connectAttr( (autoStretchConditionNode + ".outColorR"), (scaleLoc[0] + ".scaleX") )
	cmds.connectAttr( (autoStretchConditionNode + ".outColorR"), (scaleLoc[0] + ".scaleY") )
	cmds.connectAttr( (autoStretchConditionNode + ".outColorR"), (scaleLoc[0] + ".scaleZ") )



	##find all the joints involved and connect them to the scale locator
	cmds.select( hi=root )
	involvedJoints = cmds.ls( sl=True )
	#print involvedJoints
	#print "\n"
	ikJoints = jpTypeFilterList(involvedJoints, "joint")

	for joint in ikJoints:
		print (joint + "\n");
		if(x == 1)
			cmds.connectAttr( (scaleLoc[0] + ".scaleX"), (joint + ".scaleX") )
		if(y == 1)
			cmds.connectAttr( (scaleLoc[0] + ".scaleY"), (joint + ".scaleY") )
		if(z == 1)
			cmds.connectAttr( (scaleLoc[0] + ".scaleZ"), (joint + ".scaleZ") )
		if(joint == end)
			break
"""

def jpmTwoBoneStretch( mainControl, control, root, flex, end, maxStretch, x, y, z ):
	##prep the control to receive stretcy-ness
	cmds.select( cl=True )
	cmds.addAttr( control, ln="autoStretchy", at="long", min=0, max=1, dv=1 )
	cmds.setAttr( (control + ".autoStretchy"), e=True, keyable=True )
	cmds.addAttr( control, ln="manualStretchy", at="float", min=1, dv=1 )
	cmds.setAttr( (control + ".manualStretchy"), e=True, keyable=True )
	cmds.addAttr( control, ln="maxStretchy", at="long", min=1, dv=maxStretch )
	cmds.setAttr( (control + ".maxStretchy"), e=True, keyable=True )

	##find the initial distance of the arm
	rootPos = cmds.xform( root, q=True, a=True, ws=True, t=True )
	flexPos = cmds.xform( flex, q=True, a=True, ws=True, t=True )
	endPos = cmds.xform( end, q=True, a=True, ws=True, t=True )

	##Measure the initial distance
	rootDistanceNode = cmds.distanceDimension( sp=rootPos, ep=flexPos )
	flexDistanceNode = cmds.distanceDimension( sp=flexPos, ep=endPos )
	initialDistance = cmds.getAttr( (rootDistanceNode + ".distance") ) + cmds.getAttr( (flexDistanceNode + ".distance") )

	rootDistNodeStartLocShape = cmds.connectionInfo( (rootDistanceNode + ".startPoint"), sfd=True )
	rootDistNodeStartLocShape = rootDistNodeStartLocShape.split(".")[0]
	cmds.select( rootDistNodeStartLocShape )
	rootStartLoc = cmds.pickWalk( d="up" )

	rootDistNodeEndLocShape = cmds.connectionInfo( (rootDistanceNode + ".endPoint"), sfd=True )
	rootDistNodeEndLocShape = rootDistNodeEndLocShape.split(".")[0]
	cmds.select( rootDistNodeEndLocShape )
	flexStartLoc = cmds.pickWalk( d="up" )

	flexDistNodeEndLocShape = cmds.connectionInfo( (flexDistanceNode + ".endPoint"), sfd=True )
	flexDistNodeEndLocShape = flexDistNodeEndLocShape.split(".")[0]
	cmds.select( flexDistNodeEndLocShape )
	flexEndLoc = cmds.pickWalk( d="up" )
	#########################
	##Do that stretchy thing -- make the stretchy nodes
	########################
	##	make the dimension node and find out the names of the locators it made
	curDistNode = cmds.distanceDimension( sp=rootPos, ep=endPos )
	curDistStartLocShape = cmds.connectionInfo( (curDistNode + ".startPoint"), sfd=True )
	curDistEndLocShape = cmds.connectionInfo( (curDistNode + ".endPoint"), sfd=True )

	##	because the connection info returns the shape node rather than the transform
	##	we have to go through all this shite in order to find out the names of the 
	##	locators that the distance dimension node makes. Highly annoying. 
	curDistStartLocShape = curDistStartLocShape.split(".")[0]
	cmds.select( curDistStartLocShape )
	startLoc = cmds.pickWalk( d="up" )

	curDistEndLocShape = curDistEndLocShape.split(".")[0]
	cmds.select( curDistEndLocShape )
	endLoc = cmds.pickWalk( d="up" )

	try:
		cmds.parent( startLoc, root )
		cmds.parent( endLoc, control )
	except:
		print ""


	##make the utility nodes and connections
	##	multiply initial distance by current scale
	mainScaleNode = cmds.shadingNode( "multiplyDivide", asUtility=True, n=(control + "_MD") )
	cmds.setAttr( (mainScaleNode + ".input1X"), initialDistance )
	cmds.setAttr( (mainScaleNode + ".input1Y"), initialDistance )
	cmds.setAttr( (mainScaleNode + ".input1Z"), initialDistance )
	cmds.connectAttr( (mainControl + ".scaleX"), (mainScaleNode + ".input2X") )
	cmds.connectAttr( (mainControl + ".scaleY"), (mainScaleNode + ".input2Y") )
	cmds.connectAttr( (mainControl + ".scaleZ"), (mainScaleNode + ".input2Z") )

	##	divide current distance by initial distance
	scaleNode = cmds.shadingNode( "multiplyDivide",  asUtility=True, n=(control + "_MD") )
	cmds.setAttr( (scaleNode + ".operation"), 2 )

	cmds.connectAttr( (mainScaleNode + ".outputX"), (scaleNode + ".input2X") )
	cmds.connectAttr( (mainScaleNode + ".outputY"), (scaleNode + ".input2Y") )
	cmds.connectAttr( (mainScaleNode + ".outputZ"), (scaleNode + ".input2Z") )

	cmds.connectAttr( (curDistNode + ".distance"), (scaleNode + ".input1X") )
	cmds.connectAttr( (curDistNode + ".distance"), (scaleNode + ".input1Y") )
	cmds.connectAttr( (curDistNode + ".distance"), (scaleNode + ".input1Z") )


	##	auto/manual stretch condition
	autoStretchConditionNode = cmds.shadingNode("condition", asUtility=True, n=(control + "_autoStretchCon") )
	cmds.connectAttr( (control + ".autoStretchy"), (autoStretchConditionNode + ".firstTerm") )
	cmds.setAttr( (autoStretchConditionNode + ".secondTerm"), .5 )

	cmds.setAttr( (autoStretchConditionNode + ".operation"), 2 )
	cmds.connectAttr( (scaleNode + ".outputX"), (autoStretchConditionNode + ".colorIfTrueR") )
	cmds.connectAttr( (scaleNode + ".outputY"), (autoStretchConditionNode + ".colorIfTrueG") )
	cmds.connectAttr( (scaleNode + ".outputZ"), (autoStretchConditionNode + ".colorIfTrueB") )

	cmds.connectAttr( (control + ".manualStretchy"), (autoStretchConditionNode + ".colorIfFalseR") )
	cmds.connectAttr( (control + ".manualStretchy"), (autoStretchConditionNode + ".colorIfFalseG") )
	cmds.connectAttr( (control + ".manualStretchy"), (autoStretchConditionNode + ".colorIfFalseB") )


	##	clamp scale between 1 and maxStretch
	clampNode = cmds.shadingNode( "clamp", asUtility=True, n=(control + "_clamp") )
	cmds.setAttr( (clampNode + ".minR"), 1 )
	cmds.setAttr( (clampNode + ".minG"), 1 )
	cmds.setAttr( (clampNode + ".minB"), 1 )

	cmds.connectAttr( (control + ".maxStretchy"), (clampNode + ".maxR") )
	cmds.connectAttr( (control + ".maxStretchy"), (clampNode + ".maxG") )
	cmds.connectAttr( (control + ".maxStretchy"), (clampNode + ".maxB") )

	cmds.connectAttr( (autoStretchConditionNode + ".outColor"), (clampNode + ".input") )

	##	connect to the joints scale
	if(x == 1):
		cmds.connectAttr( (clampNode + ".outputR"), (root + ".scaleX") )
		cmds.connectAttr( (clampNode + ".outputR"), (flex + ".scaleX") )
	if(y == 1):
		cmds.connectAttr( (clampNode + ".outputG"), (root + ".scaleY") )
		cmds.connectAttr( (clampNode + ".outputG"), (flex + ".scaleY") )
	if(z == 1):
		cmds.connectAttr( (clampNode + ".outputB"), (root + ".scaleZ") )
		cmds.connectAttr( (clampNode + ".outputB"), (flex + ".scaleZ") )

	##cleanup
	##cmds.select( rootDistanceNode )
	##cmds.pickWalk( d="up" )
	##cmds.delete()
	##cmds.select( flexDistanceNode )
	##cmds.pickWalk( d="up" )
	##cmds.delete()
	##cmds.delete( flexStartLoc )



#Helper Functions
def getPositions(object):
	thisPos = cmds.xform(object, q=True, t=True, a=True, ws=True)
	return thisPos

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