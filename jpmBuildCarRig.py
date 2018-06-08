##James Parks
##06-15-12

import maya.cmds as cmds
import maya.mel as mm
##import math
##import os
##import sys
import jpmFourPoint as fourPoint
import jpmTireBulge as tireBulge
import jpmTireFlat as tireFlat
import jpmWheelCamber as wheelCamber

def jpmBuildCarRig():
	##Find placer nodes
	
	##Build 4 point suspension
	fourPoint.make4point("suspension", fourPointAnchors)
	
	##Build 4 point wheels
	fourPoint.make4point("wheels", fourPointAnchors)
	
	##Build Tire Bulge
	tireBulge.doTireBulge( wheels[], controls[], attaches[], squashes[])
	
	##Build Wheel Camber
	wheelCamber.doTireBulge( wheels[], controls[], attaches[], squashes[])
	
	##Build Tire Flat
	tireFlat.doTireFlat(wheels, controls)
	
	##Build Body joint
	makeBodyJoint(anchors[])
	
	##Do Steering and Wheel Rotation