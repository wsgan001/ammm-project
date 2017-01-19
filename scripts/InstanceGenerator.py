'''
Project AMMM
Instance Generator

Juan Francisco Martinez Vera
juan.francisco.martinez@est.fib.upc.edu
'''

import sys
import math, random
import time

NUM_CITIES=10
SPACE_DIM=0 # init
MAX_DISTANC=720
RAND_SEED=int(time.time())

NICE=False

def generatePoints(ncities, dim):
    # The coordinates sources is in the middle
    # of the plane.

    random.seed(RAND_SEED)
    cities=[]
    for i in range(ncities):
        posx=random.uniform(-dim/2, dim/2)
        posy=random.uniform(-dim/2, dim/2)

        cities.append([posx,posy])
    return cities

def calculeDistances(ncities, poscities):
    # Calcule cartesian distances
    distances=list()
    
    for i in range(ncities):
        dists=[]
        for j in range(ncities):
            if i==j: dists.append(0)
            else:
                d=math.sqrt((poscities[i][0]-poscities[j][0])**2 + \
                        (poscities[i][1]-poscities[j][1])**2)
                # Our model only permits INTs
                # also, we are getting the floor round value
                dists.append(int(d))
        distances.append(dists)

    return distances
    
def calculeDistances2(ncities, poscities, stLocation):
    # Calcule cartesian distances
    # stLocation is on (0,0)
    distances=list()
    
    for i in range(ncities):
        dists=[]
        for j in range(ncities):
            if i==j: 
                dists.append(0)
            elif i==stLocation-1:
                d=math.sqrt((0-poscities[j][0])**2 + (0-poscities[j][1])**2)
                
                dists.append(int(d))
            elif j==stLocation-1:
                d=math.sqrt((poscities[i][0]-0)**2 + (poscities[i][1]-0)**2)
                dists.append(int(d))
            else:
                d=math.sqrt((poscities[i][0]-poscities[j][0])**2 + \
                        (poscities[i][1]-poscities[j][1])**2)
                
                dists.append(int(d))
        distances.append(dists)

    return distances

def calculeTask(ncities, distances, stLocation):
    task=[]
    for i in range(ncities):
        from_st = distances[stLocation-1][i]
        to_st = distances[i][stLocation-1]
        
        task_time = random.randrange(0, (720-from_st-to_st))
        task.append(task_time)
    
    return task

def calculeWindows(ncities, distances, tasks, stLocation, maxwsize):
    minW=[]
    maxW=[]
    
    for i in range(ncities):
        if i == stLocation-1: continue
        
        from_st = distances[stLocation-1][i]
        #Purelly random
        #min_w = random.randrange(0, from_st)
        #max_w = random.randrange(from_st, 720)
        
        # Random with max windows size
        min_w = random.randrange(max(0,from_st-maxwsize), from_st-1)
        max_w = random.randrange(from_st, min(720,from_st+maxwsize))
        
        maxW.append(max_w)
        minW.append(min_w)
        
    minW.insert(stLocation-1,0)
    maxW.insert(stLocation-1,720)
    return minW, maxW
    
def main(argc, argv):
    if argc < 4:
        print("Error on parameters.")
        print("./{0} <nlocations> <maxwinsize> <SCAT | GATH>".format(argv[0]))
        return(0)
        
    # Parsing params
    ncities = int(argv[1])
    maxwinsize = int(argv[2])
    scattered = (argv[3] == "SCAT")
    
    # Generating data
    SPACE_DIM=math.sqrt( (MAX_DISTANC/2)**2/2)
    stLocation = random.randrange(1,ncities)
    
    if scattered == True:
        poscities = generatePoints(ncities, 2*SPACE_DIM)
        distances = calculeDistances2(ncities, poscities, stLocation)
    else:
        poscities = generatePoints(ncities, SPACE_DIM)
        distances = calculeDistances(ncities, poscities)
        
    citytask  = calculeTask(ncities, distances, stLocation)
    citytask[stLocation-1]=0
    minW, maxW  = calculeWindows(ncities, distances, citytask, stLocation, maxwinsize)
    
    windows_sizes = []
    windows_sum = 0
    
    for i in range(ncities): windows_sizes.append(maxW[i]-minW[i])
    for w in windows_sizes: windows_sum += w
        
    windows_mean = windows_sum / ncities

    # Writting results
    
    filename="./instance_{0}_{1}.dat".format(ncities, RAND_SEED)
    outfile=open(filename, "w")
    
    import pprint
    pp = pprint.PrettyPrinter(indent=4, depth=200, stream=outfile)
        
    outfile.write("// Generated by InstanceGenerator.py v0.1\n")
    outfile.write("// Juan Francisco Martinez Vera\n")
    outfile.write("// AMMM - MIRI, FIB UPC\n")
    outfile.write("//\n// RAND_SEED={0}\n\n".format(RAND_SEED))
    
    outfile.write("bigM=100000;\n\n")
    outfile.write("nLocations={0};\n".format(ncities))
    outfile.write("startLocation={0};\n".format(stLocation))
    outfile.write("distances="); pp.pprint(distances)
    outfile.write(";\ntask="); pp.pprint(citytask)
    outfile.write(";\nminW="); pp.pprint(minW)
    outfile.write(";\nmaxW="); pp.pprint(maxW)
    outfile.write(";")
    outfile.write("// Mean windows sizes: {0}".format(windows_mean))
    
    print ("{0} input file has been generated.".format(filename))

if __name__=="__main__":
	main(len(sys.argv), sys.argv)
