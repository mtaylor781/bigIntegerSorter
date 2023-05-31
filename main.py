import numpy as np
import os
from memory_profiler import profile

file = open("input_file", 'rb')
tempFiles = np.empty(0)
pointers = np.empty(8)


#creates temp files
for i in range(8):
    newFileName = "file" + str(i)
    tempFiles = np.append(tempFiles, newFileName)
    f = open(newFileName, "wb")
    x = np.fromfile(file, dtype = np.uint64, count = 134217729)
    x = np.sort(x)
    f.write((x).astype(np.uint64))
    x = 0
    f.close()
file.close()


bf0 = open(tempFiles[0], 'r+b')
bf1 = open(tempFiles[1], 'r+b')
bf2 = open(tempFiles[2], 'r+b')
bf3 = open(tempFiles[3], 'r+b')
bf4 = open(tempFiles[4], 'r+b')
bf5 = open(tempFiles[5], 'r+b')
bf6 = open(tempFiles[6], 'r+b')
bf7 = open(tempFiles[7], 'r+b')
buffers = np.array([bf0, bf1, bf2, bf3, bf4, bf5, bf6, bf7])

#initializes pointers
bucket = np.empty(0)
x = 0
for i in buffers:
    z = np.fromfile(i, dtype = np.uint64, count = 1000000)
    pointers[x] = z[-1]
    bucket = np.concatenate((bucket, z), axis = None)
    z = 0
    x = x+1

#creates output file
output = open('newOutput', "wb")
while pointers.size > 0:
    bucket = np.sort(bucket)
    minn = pointers.argmin()
    cap = np.where(bucket == np.amin(pointers))
    output.write((bucket[0:(cap[0][0] + 1)]).astype(np.uint64))
    bucket = bucket[cap[0][0] + 1:]
    try:
        z = np.fromfile(buffers[minn], dtype = np.uint64, count = 1000000)
        pointers[minn] = z[-1]
        bucket = np.concatenate((bucket, z), axis = None)
        z = 0
    except:
        z = np.fromfile(buffers[minn], dtype = np.uint64, count = -1)
        pointers = np.delete(pointers, minn)
        buffers[minn].close()
        buffers = np.delete(buffers, minn)
        bucket = np.concatenate((bucket, z), axis = None)
output.close()


os.remove("file0")
os.remove("file1")
os.remove("file2")
os.remove("file3")
os.remove("file4")
os.remove("file5")
os.remove("file6")
os.remove("file7")


    