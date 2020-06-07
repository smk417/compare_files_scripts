# -------------------------------------------------------------------
# --Chipspirit Proprietary
# --Copyright (C) 2020 Chipspirit
# --All Rights Reserved
# -------------------------------------------------------------------
# --File Name		  : compare_lock.py
# --Creation Date	  : 12-05-2020
# --Last Modified         : Tuesday 12 May 2020 03:14:14 PM IST
# --Author 		  : Sumit Kavathekar
# --Author's Email	  : sumit.kavathekar@chipspirit.com
# --Project Name 	  : ABHED-1
# --Department		  : RTL Design 
# --Description 	  : 1st input file is 1st argument to be passed :golden
#                           2nd input file is 2nd argument to be passed :received
# --Run as                : python compare_block.py gldn.txt rcvd.txt

# --Detailed Description  :

# This script takes in 2 input arguments named as 1. golden txt file and 2. received txt file
# This will take the first entry in the rcvd.txt file and then it will traverse that in gldn.txt file till it matches the entry
# Once the first entry is matched then script sets that matched location in gldn.txt file as first entry and ignores previous entries if any
# Then script takes the second onwards entries and compares it with entries in gldn.txt 
# If all matches after first match then COMPARISON SUCCESS else FAILURE !

import sys
import difflib
import fileinput

error=0

def file_len(file_name):
  with open(file_name) as f:
    for i, l in enumerate(f):
      pass
  return i+1
 
depth_glden=file_len(sys.argv[1])
depth_rcvd=file_len(sys.argv[2])

min_depth=min(depth_rcvd,depth_glden)

if(depth_rcvd > depth_glden):
  error=1

print("depth of gldn.txt --> %s" %depth_glden)
print("depth of rcvd.txt --> %s" %depth_rcvd)
print("min depth --> %s" %min_depth)
print("\n##########################################\n");

gldn=open(sys.argv[1],"r")
rcvd=open(sys.argv[2],"r")

rcvd_line=rcvd.readline()

for line1 in range (1,depth_glden+1,1):
  glden_line=gldn.readline()
  if glden_line!=rcvd_line:
    if(line1==depth_glden):
      error=1
  else:
    first_match_in_gldn=line1
    print('first match in glden at line %s'%first_match_in_gldn)
    break

effective_min_depth=min((depth_glden-(first_match_in_gldn-1)),depth_rcvd)
print('eff min depth = %s'%effective_min_depth)

for line2 in range (1,effective_min_depth,1):
  rcvd_line=rcvd.readline()
  #print('rcvd line = %s'%rcvd_line)
  glden_line=gldn.readline()
  if(glden_line!=rcvd_line):
    error=1
    break

if(error==1):
  print('COMPARISION FAILED ---> compare_lock.py::error = %s'%error)
else:
  print('COMPARISION SUCCESSFUL')
  
#sys.exit(error)

gldn.close()
rcvd.close()
