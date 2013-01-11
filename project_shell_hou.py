import os
import env
import houbox
reload(env)
reload(houbox)

def run():
    os.system('python T:/03_RnD_server/Project/__setting__/project_shell.py')
    #after project_shell
    
    pathfile = 'c:/temp_path.txt'
    access = 0
    try:
        with open(pathfile) as f:
            path = f.readline()
            access = 1
    except IOError:
        pass

    if access is 1:
        shotpathList = path.split('/')
        prjname = shotpathList[0]
        shotpathList = shotpathList[1:]
        
        print("")
        houbox.setVariable("PRJNAME", prjname)
        
        prjpath = env.projectpath(prjname)
        shotpath = '/'.join(shotpathList)
        shotName = shotpathList[-1]
        
        if len(shotpathList)>1:
            seqName = '/'.join(shotpathList[:-1])
            houbox.setVariable("SEQNAME", seqName)
        houbox.setVariable("SHOTNAME", shotName)
        print("")
        
        houbox.setVariable("PRJ", prjpath)
        houbox.setVariable("SHOT", "/".join([prjpath, "work", shotpath]))
        houbox.setVariable("JOB", "/".join([prjpath, "work", shotpath, "houdini"]))
        houbox.setVariable("OUT", "/".join([prjpath, "output", shotpath]))
        houbox.setVariable("COMMON", "/".join([prjpath, "common"]))

        os.remove(pathfile)





