#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yongbin
#
# Created:     19-09-2012
# Copyright:   (c) yongbin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import fnmatch
import shutil
import xlrd
import sys

def main():
    ## input check
    
    
#     if len(sys.argv) != 3:
#         print("usage : scancopy 'excelfile' 'destination folder' 'partname'")
#         print("partname - model, ani, layout, light, fx")
#         return
#         
#     file = sys.argv[1].replace("\\", "/") # excelfile
#     destroot = sys.argv[2].replace("\\", "/") # dest folder
#     part = sys.argv[3] # department

    file = "W:/01_Project_Movie/SM_MV/01_DOC/00.CG_LIST/120729_SM_CGLIST.xls"
    part = "fx"    
    destroot = "C:/tmp"
    
    
    # file check
    if os.path.isfile(file) != 1:
        print("wrong file : {0}".format(file))
        return
        
    # part check
    partinputlist = ['model', 'ani', 'layout', 'light', 'fx']
    partmaplist = ['model', 'animation', 'layout', 'lighting', 'FX']
    
    if part in partinputlist:
        partindex = partinputlist.index(part)
        part = partmaplist[partindex]
    else:
        print("select appropriate part - model, ani, layout, light, fx")
        
    
    # find project folder
    # 엑셀파일에 프로젝트폴더 위치가 기입되어있으면 함.
    filesplit = file.split("/")
    
    if file.startswith("T:"):
        projectfolder = "01_3D_server"
    elif file.startswith ("W:"):
        projectfolder = "01_Project_Movie"
    else:
        print("cannot find project")
        return
        
    print projectfolder
    print filesplit
    try:
        end = filesplit.index(projectfolder)
    except:
        print("cannot set project root")
        return
        
    print end
    projectroot = "/".join(filesplit[:end+2])
    
    print(projectroot)
    
    
    ## OPEN EXCEL FILE
    myexcel =xlrd.open_workbook(file)
    cglist = myexcel.sheet_by_name("CG-LIST")
    numrows = cglist.nrows
    numcols = cglist.ncols

    ## find cglink column
    
    link = 'shot Name'
    findlink = 0
    for j in range(numcols):
        for i in range(numrows):
            if link == cglist.cell(i,j).value:
                shotcol = j
                findlink = 1
                break
    if findlink == 0:
        print("your link wasn't mapped")
        return
        

    
    
    ## find cell of user's part
    findpart = 0
    for j in range(numcols):
        for i in range(numrows):
            if part == cglist.cell(i,j).value:
                partcell = (i,j)
                findpart = 1
                break
    if findpart == 0:
        print("your part wasn't mapped")
        return


    ## if find appropriate part then 
    ##
    partcol = cglist.col_values(partcell[1])

    copyrows = []

    for row in range(partcell[0], len(partcol)):
        if partcol[row] != '':
            copyrows.append((row,shotcol))


    ## find excel's link list
    ## if the link is matched with  then export srcpath to 
    linkmap = cglist.hyperlink_map
    

    copydata = []
    for cell_num, srcpath in linkmap.items():
        if cell_num in copyrows:
            x,y = cell_num
            copydata.append((cglist.cell(x,y).value, srcpath.url_or_path, cell_num))
    
#     print(copydata)



    ## copy start
    print("copy start!")
    for shot, address, cell in copydata:
        
        srcroot = "/".join([projectroot, address])
        destpath = "/".join([destroot, shot])
        for path, dirs, files in os.walk(srcroot):
            path = path.replace("\\", "/")
            for dirname in fnmatch.filter(dirs, 'jpeg'):
                relpath = os.path.relpath(path, srcroot)   
                
                if relpath == '.': # if srcfolder is direct child of srcroot 
                    relpath = ''
                
                srcpath = "/".join([path, dirname])
                eachdest = "/".join([destpath, relpath])
                
                if(os.path.isdir(destpath)!=True):
                    print("copy {0} to {1}".format(srcpath, eachdest))
                    #shutil.copytree(srcpath, destpath)
                else:
                    print("{0} is already exist. skip!".format(eachdest))
                    print("for your information search cell : {0}".format(cell))
# 
#         if(os.path.isdir(destpath)!=True):
#             print("{0} copying!".format(destpath))
#             shutil.copytree(srcpath, destpath)  #, ignore=shutil.ignore_patterns('*.db')
#         
# 

    print("done")



if __name__ == '__main__':

    main()

