import maya.cmds as cmds
import maya.mel as mm

def jpmACCurve(manipulatorType, controlType, groupThings):
	selectedObjs = cmds.ls( sl=True)
	createdControls = []
	createdClusters = []
	for selectedCurve in selectedObjs:
		if( manipulatorType == 3 ):
			if( selectedCurve == selectedObjs[-1] ):
				break
		objType = "nurbsCurve"
		if( objType == "nurbsCurve" ):
			spanCount = cmds.getAttr( (selectedCurve + ".spans") )
			degCount = cmds.getAttr( (selectedCurve + ".degree") )
			cvCount = spanCount + degCount
			for i in range(cvCount):
				cmds.cluster( (selectedCurve + ".cv[" + str(i) + "]") )
				clustName = cmds.ls( sl=True )
				if( manipulatorType == 1 ):
					locName = cmds.spaceLocator()
				if( manipulatorType == 2 ):
					locName = cmds.circle( c=(0, 0, 0), nr=(0, 0, 1), r=1, s=8 )
				if( manipulatorType == 3 ): 
					numberOfObjs = size(selectedObjs)
					locName = cmds.duplicate( selectedObjs[numberOfObjs - 1] )


				##place locator on top of cluster
				cmds.select( (clustName[0], locName[0]) )
				point = cmds.pointConstraint( n="tempPoint", weight=1 )
				orient = cmds.orientConstraint( n="tempOrient", weight=1 )
				scale = cmds.scaleConstraint( n="tempScale", weight=1 )

				##cleanup
				cmds.select( (point[0], orient[0], scale[0]) )
				cmds.delete()

				if( controlType == 1 ):
					cmds.parent( clustName[0], locName[0] )
				if( controlType == 2 ):
					point = cmds.pointConstraint( locName[0], clustName[0], weight=1 )
				if( controlType == 3 ):
					cmds.connectAttr( (locName[0] + ".t"), (clustName[0] + ".t") )

				cmds.select( locName[0] )
				mm.eval( "FreezeTransformations" )
				cmds.setAttr( (clustName[0] + ".visibility"), 0 )

				if( manipulatorType == 1 ):
					locName[0] = cmds.rename( locName[0], (selectedCurve + "_clusterLoc_" + str(i)) )
				if( manipulatorType == 2 ):
					locName[0] = cmds.rename( locName[0], (selectedCurve + str(i) + "_CTRL" ) )
				if( manipulatorType == 3 ):
					locName[0] = cmds.rename( locName[0], (selectedCurve + str(i) + "_CTRL") )

				clustName[0] = cmds.rename( clustName[0], (selectedCurve + str(i) + "_CLS") )

				createdControls.append( locName[0] )
				createdClusters.append( clustName[0] )
			
			if( groupThings == 1 ):
				cmds.select( createdControls )
				ctrlGrp = cmds.group( n=(selectedCurve + "_controls") )
				if( controlType != 1 ):
					cmds.select( createdClusters )
					clsGrp = cmds.group( n=(selectedCurve + "_clusters") )

			return ctrlGrp, clsGrp

def jpmAutoClusterCurve():
	winName = "jpAutoClusterCurve"
	if( cmds.window( winName, exists=True ) ):
		cmds.deleteUI( winName )
	cmds.window( winName, t="Auto Cluster Curve v1.1", wh=(200, 70), rtf=1 )

	cmds.rowColumnLayout( nc=1, w=210, cw=(1, 210) )
	cmds.text( label="Manipulator Type" )
	cmds.radioButtonGrp( "manipulatorType", w=300, h=25, nrb=3, cw=((1,60),(2,50),(3,100)), cal=((1,"left"),(2,"left"),(3,"left")), l1="Locator", l2="Circle", l3="Last Selected", sl=2 )
	cmds.text( label="Control Type" )
	cmds.radioButtonGrp( "parentConstrainGrp", w=300, h=25, nrb=3, cw=((1,60),(2,75),(3,60)), l1="Parent", l2="Constrain", l3="Connect", sl=1 )
	cmds.checkBoxGrp( "groupResultsGrp", ncb=1, label="Group Results" )
	cmds.button( "clusterizeButton", w=50, l="Clusterize", c="jpmACcollectAndCall()" )

	cmds.showWindow( winName )

def jpmACcollectAndCall():
	manipType = cmds.radioButtonGrp( "manipulatorType", q=True, sl=True )
	contType = cmds.radioButtonGrp( "parentConstrainGrp", q=True, sl=True )
	grpThings = cmds.checkBoxGrp( "groupResultsGrp", q=True, v1=True )
	jpmACCurve( manipType, contType, grpThings )