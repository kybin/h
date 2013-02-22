import maya.cmds as mc

path=(mc.file(q=True,sn=True))
fileName=(mc.file(q=True,sn=True,shn=True))

if fileName!='':
 temp=path.partition(fileName)
 mc.workspace(temp[0],openWorkspace=True)
 
 print 'File Inherit Project Set'
else:
 mc.workspace(( (mc.optionVar( q='ProjectsDir' ))), openWorkspace=True )
 
 print 'Default Project Set'

 # setproject $newProject