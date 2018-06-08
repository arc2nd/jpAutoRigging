##James Parks
##06-20/12

import maya.cmds as cmds
import maya.mel as mm

import jpmConstraintSnap as snap


def jpmAutoCluster( object, name ):
	clusterName = cmds.cluster( object, n=(name + "_cls") )[1]
	locatorName = cmds.spaceLocator( n=(name + "_loc") )[0]
	
	print clusterName
	print locatorName
	
	snap.jpmConstraintSnap( clusterName, locatorName )
	
	cmds.parent( clusterName, locatorName )
	cmds.makeIdentity( locatorName, apply=1 )
	
	return locatorName, clusterName