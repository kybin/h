softwareinfo = {
			'houdini':
			{'dir':'scenes', 'read':['hip'], 'write':'hip', 'batch':'hython', 'execute': 'houdini',
			'initscript' : '''
hou.hipFile.clear()

hou.setFrame({fps})
hou.hscript('tset {start}, {end}')

ip = hou.node('out').createNode('ifd', 'ip')
ip.parm('vm_picture').set('ip')

seq = hou.node('out').createNode('ifd', '{shot}_{task}')
seq.parm('vm_picture').set('$OUT/v01/$OS.$F4.exr')
seq.parm('vm_image_comment').set('$HIP/$HIPNAME')
seq.setPosition(hou.Vector2(2,0))

hou.hscript('set -g SHOW = {show}')
hou.hscript('set -g SEQ = {seq}')
hou.hscript('set -g SCENE = {scene}')
hou.hscript('set -g SHOT = {shot}')
hou.hscript('set -g TASK = {task}')

hou.hscript('set -g SHOWPATH = {showpath}')
hou.hscript('set -g SEQPATH = {seq}')
hou.hscript('set -g SCENEPATH = {scenepath}')
hou.hscript('set -g SHOTPATH = {shotpath}')
hou.hscript('set -g TASKPATH = {taskpath}')
hou.hscript('set -g DATAPATH = {showpath}/assets')

hou.hscript('set -g JOB = {shotpath}')
hou.hscript('set -g OUT = {renderpath}')

hou.hipFile.save('{filepath}')'''
			},

			'maya':
			{'dir':'scenes', 'read':['ma', 'mb'], 'write':'mb', 'batch':'mayabatch.exe -script', 'execute': 'maya.exe',
			'initscript':'''
file -rn "{file}";
file -s;'''
			},

			'max':
			{'dir':'scenes', 'read':['max'], 'write':'max', 'batch':'3dsmax.exe -mxs', 'execute': '3dsmax',
			'initscript':'''
'''			}
		}
