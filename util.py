import os
import shutil

def delAllFiles(rootdir):
	filelist=[]
	filelist=os.listdir(rootdir)                #list all the files
	for f in filelist:
		filepath = os.path.join( rootdir, f )   #path-absolute path
		if os.path.isfile(filepath):            #is file?
			os.remove(filepath)                 #delete file
		elif os.path.isdir(filepath):
			shutil.rmtree(filepath,True)        #is dir
