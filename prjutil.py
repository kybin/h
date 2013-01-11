import re
import os
import env
import filebox
reload(env)
reload(filebox)

def selectPrj(prjRoot):
    message = ''
    while True:
        prjList = [prj for prj in os.listdir(prjRoot) if not prj.startswith('_')]
        prjList = [prj for prj in prjList if os.path.isdir('/'.join([prjRoot, prj]))]
        prjLowerList = [prj.lower() for prj in prjList]
        os.system('cls')
        enumList = [':'.join([str(i+1), item]) for i,item in enumerate(prjList)]
        print('{0}'.format('\n'.join(enumList)))
        if message != '':
            print('\n<-- {0} -->'.format(message))
        message = ''

        userInput = raw_input("\nSet project name. 'quit' will Quit this program\n\n")

        if userInput == '':
            message = "create project : 'prjname.'"
            continue
        elif userInput == '..':
            message = "root of tree"
            continue
        elif userInput.lower() == 'quit':
            print('\nBye')
            return False        
        else:
            if userInput.isdigit():
                digit = int(userInput)
                if digit <= len(prjList):
                    userInput = prjList[digit-1]
                else:
                    message = 'not a valid project index'
                    continue

            if userInput in ['.']:
                message = 'please type project name fist'.upper()
            elif userInput[-1]=='.':
                filebox.makeTree("/".join([prjRoot, userInput]), 'project')
                message = 'Created {0} Project'.format(userInput).upper()
            elif userInput.lower() not in prjLowerList:
                message = 'the project not exist.\nif want to create prj, add [.] end of project name'.upper()
            else:
                index = prjLowerList.index(userInput.lower())
                prjName = prjList[index]
                prjPath = "/".join([prjRoot, userInput])
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
        # print('\n'*40)
        os.system('cls')
        print('You are here : {0}'.format(viewpath))
        print('-'*50)
        prSubList = [':'.join(['@'+str(num+1), subnet]) for num, subnet  in list(enumerate(subnetList))]
        prShotList = [':'.join([str(num+1), shot]) for num, shot  in list(enumerate(shotList))]
        print('SUBNET')
        print('\t{0}'.format('\n\t'.join(prSubList)))
        print('SHOT')
        print('\t{0}'.format('\n\t'.join(prShotList)))
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
            if len(shotPathList) == 0:
                return 'up'
            else:
                shotPathList = shotPathList[:-1]
                continue
        elif userInput.startswith('_'): # we use _ for hide directory
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
        selType = 0 # type shot
        if userInput.startswith('@'):
            selType = 1 # type subnet
            userInput = userInput[1:]
        if userInput.isdigit():
            digit = int(userInput)
            selList = [shotList,subnetList][selType]
            selName = ['shot', 'subnet'][selType]
            if digit <= len(selList):
                userInput = selList[digit-1]
            else:
                message = 'not a valid {0} index'.format(selName)
                continue
        del selType

        # correct shot name
        shotExist = False
        lowerList = [shot.lower() for shot in fullList]
        lowerDict = dict(zip(lowerList, fullList))
        if lowerDict.has_key(userInput.lower()) == True:
            shotExist = True
            userInput = lowerDict[userInput.lower()]

        # create
        if saveID != False:             

            if shotExist:
                message = '{0} already exist'.format(userInput)
            elif saveID=='.': 
                shotPath = '/'.join([curDir, userInput])
                outPath = '/'.join([outDir, userInput])
                filebox.makeTree(shotPath, 'shot')
                filebox.makeTree(outPath, 'out')
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


