import os
import re
import filebox

def play(curnode, token=0):
	parmfile = curnode.parm('vm_picture').eval()
	parmrange = curnode.parm('trange').evalAsString()

	if parmfile in ['ip', 'md']:
		print('cannot display {0}'.format(parmfile))

	elif parmrange == 'off':
		os.system('start mplay {0}'.format(parmfile))

	else: # if user set frame range
		parmframe = curnode.parmTuple('f').eval()
		framestring = " ".join([str(int(frame)) for frame in parmframe])

		frameobj = re.compile('(?P<pre>[_.]*)(\d+)(?P<post>[.]\w+)$')
		filestring = frameobj.sub('\g<pre>$F\g<post>', parmfile)

		sframeobj = re.compile('[_.]*(\d+)[.]')
		singleframe = sframeobj.findall(parmfile)[-1]
		digit = str(len(singleframe))
		# print(filestring, singleframe)

		if token == 0:
			imgscale = 100
		elif token == 1:
			imgscale = 50
		elif token == 2:
			imgscale = 25
		
		os.system('start mplay -f {0} -z {1} -Z {2} {3} '.format(framestring, imgscale, digit, filestring))

def findDigit(path):
		frameobj = re.compile('(\d+)[.]\w+$')

		frame = frameobj.findall(path)
		if len(frame) != 0:
			return len(frame[-1])
		else:
			return False


def pathForNuke(path):
		digit = findDigit(path)
		if digit is not False:
			digitstring = '%0{digit}d'.format(digit=digit)
		else:
			digitstring = ''

		frameobj = re.compile('(?P<pre>[_.]*)(\d*)(?P<post>[.]\w+)$')
		destpath = frameobj.sub('\g<pre>{digit}\g<post>'.format(digit=digitstring), path)

		# print(destpath)
		return destpath

def copyFusion(inputnodes):
	ifdnodes = [node for node in inputnodes if node.type().name() == 'ifd']
	if len(ifdnodes) == 0:
		return ""

	supportFormatDict = {'tif':'TiffFormat', 'exr':'OpenEXRFormat', 'tga':'TargaFormat', 'jpg':'JpegFormat', 'jpeg':'JpegFormat'}
	mainscript = []
	for i, node in enumerate(ifdnodes):

		inputpath = node.parm('vm_picture').evalAsString()
		fusionpath = filebox.path(inputpath).path

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

