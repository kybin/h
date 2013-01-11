import prjutil
import toolbox
import env
reload(prjutil)
reload(toolbox)
reload(env)


prjroot = env.path().ProjectRoot


while True:
    prjname = prjutil.selectPrj(prjroot)
    if prjname is not False:
        result = prjutil.selectShot(prjname)
        if result == 'up':
            continue
        elif type(result) is list:
            shotpathList = result
            shotpathList.insert(0, prjname)
            shotpath = '/'.join(shotpathList)
            tempfile = open('c:/temp_path.txt', 'w')
            tempfile.write(shotpath)
            tempfile.close()
            break
        else:
            print('unknown error')
            break
    break
