

def generatedepthList(start,end,steplen):
    max_depth = []
    for i in range(start,end,steplen):
        max_depth.append(i)
    return max_depth

def generatetrajList(start,end,steplen):
    traj = []
    for i in range(start,end,steplen):
        traj.append(i)
    return traj


foconf = open("config", "r")

text = foconf.readline()
textlist = text.split("=")
threadNum = int(textlist[1])

text = foconf.readline()
textlist = text.split("=")
PositionNum = int(textlist[1])

text = foconf.readline()
textlist = text.split("=")
numGame = int(textlist[1])

text = foconf.readline()
textlist = text.split("=")
depstart = int(textlist[1])
text = foconf.readline()
textlist = text.split("=")
depend = int(textlist[1])
text = foconf.readline()
textlist = text.split("=")
depStepLen = int(textlist[1])

text = foconf.readline()
textlist = text.split("=")
trajstart = int(textlist[1])
text = foconf.readline()
textlist = text.split("=")
trajend = int(textlist[1])
text = foconf.readline()
textlist = text.split("=")
trajStepLen = int(textlist[1])
print("123")
fileList = []
for j in range(0,threadNum):
	filename = "mutitest"+str(j)+".txt"
	fileList.append(filename)

deplist = generatedepthList(depstart,depend,depStepLen)
trajlist = generatetrajList(trajstart,trajend,trajStepLen)

#fixed lists!
deplist = [4,5,7,10,14,16,18,19,20,22,24,25]
trajlist = [7000,9000,11000,13000,15000,17000,19000]
#fixed lists!

foResult = open("initdiff.txt", "w")
foResult.write("maxdepth,num_Runs,avgstep\n")
FilePtr = []
for j in range(0,threadNum):
	fo = open(fileList[j], "r")
	FilePtr.append(fo)

for j in range(0,threadNum):
	text = FilePtr[j].readline()
Positionavg = 0
for max_depth in deplist:
	for num_Runs in trajlist:
		Positionavg = 0
		for j in range(0,threadNum):
			text = FilePtr[j].readline()
			print(text)
			textList = text.split(",")
			print(textList)
			Positionavg += float(textList[2])
		Positionavg = Positionavg/threadNum
		foResult.write(str(max_depth)+","+str(num_Runs)+","+str(Positionavg)+"\n")
foResult.close()



