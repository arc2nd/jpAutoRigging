import maya.cmds as cmds
import maya.mel as mm


##read in the placementCubes file and run it
def jpmAutoRig_makePlaceCubes(button):
	pickedTab = cmds.tabLayout( "autoRigTabs", q=1, st=1 )
	print pickedTab

	myCubesFile = ""
	myCubesContents = helper.jpReadFile(myCubesFile)
	mm.eval(myCubesContents)
	print button

##mirror the left hand placement cubes into the right
def jpmAutoRig_mirrorPlaceCubes(button):
	pickedTab = cmds.tabLayout( "autoRigTabs", q=1, st=1 )
	print pickedTab

	lefties = ["left_clavicle_PLACE_GEO", "left_hip_PLACE_GEO"]
	cmds.select( lefties )
	cmds.duplicate
	group = cmds.group
	cmds.setAttr( (group + ".scaleX"), -1 )


##################
##Ewww,... it's all GUI
##################
def jpmAutoRig():
	winName = "jpmAutoRig"
	if ( cmds.window( winName, exists=True) ):
		cmds.deleteUI( winName )
	cmds.window( winName, t="jpmAutoRig", rtf=True )
	
	
	autoRigForm = cmds.formLayout( "autoRigForm", numberOfDivisions=100 )
	autoRigTabs = cmds.tabLayout( "autoRigTabs", scr=1, innerMarginWidth=5, innerMarginHeight=5 )

	##Layout for the Biped Tab
	cmds.setParent( autoRigTabs )
	bipedTab = cmds.rowColumnLayout("Biped", nc=2, cs=(1,10))
	
	cmds.rowColumnLayout()
	cmds.text( l="    Arms", fn="boldLabelFont" )
	cmds.checkBox( "armsFKIK", label="Fk/Ik", value=0 )
	cmds.checkBox( "armsRibbonIK", label="Ribbon IK", value=0 )
	cmds.checkBox( "armsStretchy", label="Stretchy", value=0 )
	cmds.checkBox( "armsSingle", label="Single Joints", value=0 )
	cmds.checkBox( "armsRadius", label="Radius/Ulna", value=0 )
	cmds.checkBox( "arms4Joint", label="4 joint forearm", value=0 )
	cmds.checkBox( "armsChicken", label="Chicken Arms", value=0 )
	cmds.checkBox( "armsFingers", label="FK Fingers", value=0 )
	cmds.setParent( bipedTab )
	cmds.rowColumnLayout()
	cmds.text( l="    Legs", fn="boldLabelFont" )
	cmds.checkBox( "legsFKIK", label="Fk/Ik", value=0 )
	cmds.checkBox( "legsRibbonIK", label="Ribbon IK", value=0 )
	cmds.checkBox( "legsStretchy", label="Stretchy", value=0 )
	cmds.checkBox( "legsSingle", label="Single Joints", value=0 )
	
	##Layout for the Quadraped Tab
	cmds.setParent( autoRigTabs )
	quadrapedTab = cmds.rowColumnLayout("Quadraped", nc=3, cs=(1,10))
	
	cmds.rowColumnLayout()
	cmds.text( l="    Front Legs", fn="boldLabelFont" )
	cmds.checkBox( "frontLegsFKIK", label="Fk/Ik", value=0 )
	cmds.checkBox( "frontLegsRibbonIK", label="Ribbon IK", value=0 )
	cmds.checkBox( "frontLegsStretchy", label="Stretchy", value=0 )
	cmds.checkBox( "frontLegsSingle", label="Single Joints", value=0 )
	cmds.checkBox( "frontLegsRadius", label="Radius/Ulna", value=0 )
	cmds.checkBox( "frontLegs4Joint", label="4 joint forearm", value=0 )
	cmds.checkBox( "frontLegsChicken", label="Chicken Arms", value=0 )
	cmds.checkBox( "frontLegsFingers", label="FK Fingers", value=0 )
	cmds.setParent( quadrapedTab )
	cmds.rowColumnLayout()
	cmds.text( l="    Back Legs", fn="boldLabelFont" )
	cmds.checkBox( "backLegsFKIK", label="Fk/Ik", value=0 )
	cmds.checkBox( "backLegsRibbonIK", label="Ribbon IK", value=0 )
	cmds.checkBox( "backLegsStretchy", label="Stretchy", value=0 )
	cmds.checkBox( "backLegsSingle", label="Single Joints", value=0 )
	cmds.checkBox( "backLegsToes", label="FK Toes", value=0 )
	cmds.setParent( quadrapedTab )
	cmds.rowColumnLayout()
	cmds.text( l="    Tail", fn="boldLabelFont" )
	cmds.checkBox( "tailFKIK", label="Fk/Ik", value=0 )
	cmds.checkBox( "tailStretchy", label="Stretchy", value=0 )
	cmds.checkBox( "tailCloth", label="Cloth Sim", value=0 )

	
	##Layout for the Car Tab
	cmds.setParent( autoRigTabs )
	carTab = cmds.columnLayout("Car")
	cmds.radioButtonGrp( l="Suspension", la4=["Nurbs", "Cross", "Square", "X"], sl=1, nrb=4, vr=0,cw5=(60,50,50,60,50), cl5=("left","left","left","left","left") )
	##cmds.checkBox( "fourPoint", label="4 Point Suspension", value=0 )
	cmds.checkBox( "tireBulge", label="Tire Bulge", value=0 )
	cmds.checkBox( "wheelCamber", label="Wheel Camber", value=0 )
	cmds.checkBox( "tireFlat", label="Tire Flat", value=0 )
	cmds.checkBox( "autoRot", label="Auto Wheel Rotation", value=0 )

	##Layout for the Motorcycle Tab
	cmds.setParent( autoRigTabs )
	carTab = cmds.columnLayout("Motorcyle")
	
	##Layout for the Prop Plane Tab
	cmds.setParent( autoRigTabs )
	carTab = cmds.columnLayout("Prop Plane")
	
	##Layout for the Jet Tab
	cmds.setParent( autoRigTabs )
	carTab = cmds.columnLayout("Jet")
	
	##Layout for the Helicopter Tab
	cmds.setParent( autoRigTabs )
	carTab = cmds.columnLayout("Helicopter")

	##Layout for the buttons
	cmds.setParent(autoRigForm)
	buttonsLayout = cmds.rowColumnLayout(nc=3)
	cmds.button( "makeCubesButton", h=25, w=125, en=True, al="left", l="Make Place Cubes") ##, c=jpmAutoRig_makePlaceCubes )
	cmds.button( "mirrorCubesButton", h=25, w=125, en=True, al="left", l="Mirror Place Cubes") ##, c=jpmAutoRig_mirrorPlaceCubes )
	cmds.button( "makeRigButton", h=25, w=125, en=True, al="left", l="Make Rig") ##, c=jpmAutoRig_collectAndCall )

	cmds.formLayout( autoRigForm, edit=1, attachForm=((autoRigTabs,"top",0),(autoRigTabs,"left",0),(autoRigTabs,"bottom",25),(autoRigTabs,"right",0)))
	cmds.formLayout( autoRigForm, edit=1, attachForm=((buttonsLayout,"left",0),(buttonsLayout,"bottom",0),(buttonsLayout,"right",0)))
	
	cmds.showWindow( winName )

def jpmAutoRig_collectAndCall():
	armsFKIK = cmds.checkBox( "armsFkIk", q=1, v=1 )
	armsStretchy = cmds.checkBox( "armsStretchy", q=1, v=1 )
	armsSingle = cmds.checkBox( "armsSingle", q=1, v=1 )
	armsRadius = cmds.checkBox( "armsRadius", q=1, v=1 )
	arms4Joint = cmds.checkBox( "arms4Joint", q=1, v=1 )
	armsChicken = cmds.checkBox( "armsChicken", q=1, v=1 )
	armsFingers = cmds.checkBox( "armsFingers", q=1, v=1 )

	legsFKIK = cmds.checkBox( "legsFkIk", q=1, v=1 )
	legsStretchy = cmds.checkBox( "ligsStretchy", q=1, v=1 )
	legsSingle = cmds.checkBox( "legsSingle", q=1, v=1 )

	jpmBuildRig( armsFKIK, armsStretchy, armsSingle, armsRadius, arms4Joint, armsChicken, armsFingers, legsFKIK, legsStretchy, legsSingle )