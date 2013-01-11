import prjutil
reload(prjutil)
import classbox
import env
import os
reload(env)

def copyFusion(inputnodes):
	ifdnodes = [node for node in inputnodes if node.type().name() == 'ifd']
	if len(ifdnodes) == 0:
		return ""

	supportFormatDict = {'tif':'TiffFormat', 'exr':'OpenEXRFormat', 'tga':'TargaFormat', 'jpg':'JpegFormat', 'jpeg':'JpegFormat'}
	mainscript = []
	for i, node in enumerate(ifdnodes):

		inputpath = node.parm('vm_picture').evalAsString()
		fusionpath = classbox.path(inputpath).path

		format = inputpath.split('.')[-1]
		if supportFormatDict.has_key(format):
			formatID = supportFormatDict[format]
		else:
			print(" : ".join(['unsupported format passed', format]))
			continue

		startf, endf, incf = node.parmTuple('f').eval()
		lenseq = endf-startf+1
		sourcein, sourceout = 0, lenseq-1

		numpass = node.parm('vm_numaux').eval()
		for j in range(numpass+1):
			if j == 0:
				r, g, b, a = "R", "G", "B", "A"
			else:
				passname = node.parm('vm_variable_plane'+str(j)).evalAsString()
				passtype = node.parm('vm_vextype_plane'+str(j)).evalAsString()
				
				if passtype == 'float':
					r, g, b = passname, passname, passname
					a = 'SomethingThatWontMatchHopefully'
				elif passtype == 'vector':
					r, g, b = "".join([passname,'.r']), "".join([passname,'.g']), "".join([passname,'.b'])
					a = 'SomethingThatWontMatchHopefully'
				elif passtype == 'vector4':
					r, g, b = "".join([passname,'.r']), "".join([passname,'.g']), "".join([passname,'.b'])
					a = "".join([passname,'.a'])	

			posx = 800 + j*100
			posy = 200 + i*40



			fragment_basic = """
		Loader%s = Loader {
			Clips = {
				Clip {
					ID = "Houdini_Clip",
					Filename = "%s",
					FormatID = "%s",					
					StartFrame = %s,
					Length = %s,
					LengthSetManually = true,
					TrimIn = %s,
					TrimOut = %s,
					ExtendFirst = 0,
					ExtendLast = 0,
					Loop = 1,
					AspectMode = 0,
					Depth = 0,
					TimeCode = 0,
					GlobalStart = %s,
					GlobalEnd = %s,
					},
				},""" % ('_'.join([str(i),str(j)]), fusionpath, formatID, startf, lenseq, sourcein, sourceout, sourcein, sourceout)



			fragment_pass = """
				Inputs = {
				EnableClipList = Input { Value = 0, },
				["Houdini_Clip.%s.Channels"] = Input { Value = 1, },
				["Houdini_Clip.%s.RedName"] = Input { Value = FuID { "%s", }, },
				["Houdini_Clip.%s.GreenName"] = Input { Value = FuID { "%s", }, },
				["Houdini_Clip.%s.BlueName"] = Input { Value = FuID { "%s", }, },
				["Houdini_Clip.%s.AlphaName"] = Input { Value = FuID { "%s", }, },
			},
			ViewInfo = OperatorInfo { Pos = { %s, %s, }, },
		},
		""" % (formatID, formatID, r, formatID, g, formatID, b, formatID, a , posx, posy)

			mainscript.append("".join([fragment_basic,fragment_pass]))

	mainscript = "\n".join(mainscript)
	prescript = "{\n	Tools = ordered() {"
	postscript = "\n}, }"

	fullscript = prescript + mainscript + postscript
	return fullscript

def input_y_or_n(question=''):
	while True:
		answer = raw_input(question)
		if answer == 'y' or 'n':
			return answer
		else:
			print("please type 'y' or 'n'")

def selectPrj(prjRoot):

	message = ''
	while True:
		prjList = [prj for prj in os.listdir(prjRoot) if not prj.startswith('_')]
		prjList = [prj for prj in prjList if os.path.isdir('/'.join([prjRoot, prj]))]
		print('\n'*2)
		print(prjList)

		prjLowerList = [prj.lower() for prj in prjList]
		prjInput = raw_input("\nSet project name. 'quit' will Quit this program\n\n")

		if message != '':
			print('<-- {0} -->'.format(message))
		message = ''

		if prjInput == '':
			message = "create project : 'prjname.'"
			continue
		
		if prjInput.lower() == 'quit':
			print('\nBye')
			return False
		elif prjInput in ['.']:
			print('')
			print('please type project name fist'.upper())
			print('')
		elif prjInput[-1]=='.':
			prjutil.makeDirTree("/".join([prjRoot, prjInput]), 'project')
			print('')
			print('Created {0} Project'.format(prjInput).upper())
			print('')
		elif prjInput.lower() not in prjLowerList:
			print('')
			print('the project not exist.'.upper())
			print("if want to create prj, add [.] end of project name".upper())
			print('')
		else:
			index = prjLowerList.index(prjInput.lower())
			prjName = prjList[index]
			prjPath = "/".join([prjRoot, prjInput])
			return prjName

def selectShot(prjname):	
	prjDir = env.projectpath(prjname)
	shotRoot = '/'.join([prjDir, 'work'])
	outRoot = '/'.join([prjDir, 'output'])
	prjName = prjDir.split('/')[-1]

	saveIDList = ['.', '/']
	message = ''
	shotPathList = []
	while True:
		# UPDATE STATUS
		print(shotPathList)
		shotPath = '/'.join(shotPathList)
		if shotPath != '':
			curDir = '/'.join([shotRoot, shotPath])
			outDir = '/'.join([outRoot, shotPath])
			viewpath = '/'.join([prjName, shotPath])
		else:
			curDir = shotRoot
			outDir = outRoot
			viewpath = prjName

		fullList = os.listdir(curDir)
		fullList = [shot for shot in os.listdir(curDir) if not shot.startswith('_')]
		fullList = [shot for shot in fullList if os.path.isdir('/'.join([curDir, shot]))]
		subnetList = [item for item in fullList if os.path.isfile('/'.join([curDir, item, '.isSubnet']))]
		shotList = [item for item in fullList if os.path.isfile('/'.join([curDir, item, '.isShot']))]
		undefinedList = list(set(fullList) - set(subnetList) - set(shotList))
		subnetList.sort()
		shotList.sort()

		#===================================== SHOW TERM =======================================
		# dir info
		print('\n'*40)
		print('You are here : {0}'.format(viewpath))
		print('-'*50)
		prSubList = [':'.join(['@'+str(num), subnet]) for num, subnet  in list(enumerate(subnetList))]
		prShotList = [':'.join([str(num), shot]) for num, shot  in list(enumerate(shotList))]
		print('subnet : {0}'.format(', '.join(prSubList)))
		print('shot : {0}'.format(', '.join(prShotList)))
		if len(undefinedList) != 0:
			print('(undefined : {0})'.format(', '.join(undefinedList)))
		if len(fullList) == 0:
			print("Don't have any shot/subnet. Create one with 'shotname.' or 'subnetname/'")
		print('')

		# message
		if message != '':
			print('<-- {0} -->\n'.format(message))
		message = '' # throw old message

		#===================================== INPUT TERM =======================================
		try:
			userInput = raw_input('shot name : ')
		except:
			print('not allowed action')

		# special case
		if userInput.lower() == 'quit':
			print('\nQuit\n')
			return False
		elif userInput == '':
			message = "\nCreate : 'shotname.' or 'subnetname/'\nUp : '..'\nQuit : 'quit'\n"
			continue
		elif userInput == '..':  # move up directory
			shotPathList = shotPathList[:-1]
			continue
		elif userInput.startswith('_'):
			message = "cannot start with '_' please try another name"
			continue
		elif userInput in saveIDList:
			message = 'please type shot/subnet name fist'
			continue

		# body split
		saveID = False
		if userInput[-1] in saveIDList:
			# find save ID			
			saveID = userInput[-1]
			userInput = userInput[:-1]	

		# number convert to shot name
		if userInput.startswith('@'):
			if userInput[1:].isdigit():
				userInput = subnetList[int(userInput[1:])]
			else:
				message = 'undefined selection'
				continue
		elif userInput.isdigit():
			userInput = shotList[int(userInput)]

		# correct shot name
		shotExist = False
		lowerList = [shot.lower() for shot in fullList]
		lowerDict = dict(zip(lowerList, fullList))
		if lowerDict.has_key(userInput.lower()) == True:
			shotExist = True
			userInput = lowerDict[userInput.lower()]

		# create
		if saveID != False:				
			print('create')
			if shotExist:
				message = '{0} already exist'.format(userInput)
			elif saveID=='.': 
				shotPath = '/'.join([curDir, userInput])
				outPath = '/'.join([outDir, userInput])
				prjutil.makeDirTree(shotPath, 'shot')
				prjutil.makeDirTree(outPath, 'out')
				open('/'.join([shotPath, '.isShot']), 'w').close()

				shotPathList.append(userInput)
				return shotPathList
			elif saveID=='/': 
				shotPath = '/'.join([curDir, userInput])
				os.makedirs(shotPath)
				open('/'.join([shotPath, '.isSubnet']), 'w').close()
				shotPathList.append(userInput)
				message = 'Created {0} Subnet'.format(userInput)

		# set
		elif saveID == False:
			print('set')
			if not shotExist:
				message = "'{0}' not exist.".format(userInput)
			else:
				if userInput in subnetList:
					shotPathList.append(userInput)
				elif userInput in shotList:
					shotPathList.append(userInput)
					return shotPathList
				else:
					message = 'cannot access undefined shots'.upper()




        




#def prjshell():
	#prjFolder = "T:/03_RnD_server/Project"
#
	#selectPrj = True
	#selectShot = True
#
	#while selectPrj:
		#prjList = os.listdir(prjFolder)
    	#prjList = [prj for prj in prjList if not prj.startswith('_')]
#		
		#prjName = raw_input('Set project name. just Enter will quit this program\n\n').lower()
#
		#if prjName == '':
	        #print('Quit')
	        #break
	    #elif prjName.startswith('_'):
	        #print('')
	        #print("YOU CAN'T CREATE PROJECT START WITH '_'. PLEASE TRY ANOTHER NAME.")
	        #print('')
	        #continue