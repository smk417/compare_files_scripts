# -------------------------------------------------------------------
# --Chipspirit Proprietary
# --Copyright (C) 2020 Chipspirit
# --All Rights Reserved
# -------------------------------------------------------------------
# --File Name		: compare_files.py
# --Creation Date	: 12-05-2020
# --Last Modified       : Tuesday 12 May 2020 03:14:14 PM IST
# --Author 		: Sumit Kavathekar
# --Author's Email	: sumit.kavathekar@chipspirit.com
# --Project Name 	: ABHED-1
# --Department		: RTL Design 
# --Description 	: 1st input file is 1st argument to be passed :golden
# --                      2nd input file is 2nd argument to be passed :received
# --                      3rd argument : Block_length
# --Use as              : python compare_block.py gldn.txt rcvd.txt 5

# --Detailed Description  :

# This script takes in 3 input arguments named as 1. golden txt file , 2. received txt file and 3. blk_len (for first comparison with group of entries)
# This will take the first blk_len number of entries from the rcvd.txt file and then it will traverse that whole group of entries
# with entries in gldn.txt file till it matches all the selected blk_len number of entries 
# Even if one of the blk_len number of entries does not match then it will ignore that blk entries from gldn.txt and will increase the blk by 1 then again 
# it will check from  (x+1 to x+1+blk_len)
# Once the first blk_len entries are matched then script sets that matched location in gldn.txt file as new first entry and ignores previous entries if any
# Then script takes the next of matched blk_len onwards entries and compares it with entries in gldn.txt 
# If all matches after first match then COMPARISON SUCCESS else FAILURE !




import sys
import difflib
import fileinput

error = 0

def file_len(file_name):
  with open(file_name) as f:
    for i, l in enumerate(f):
      pass
  return i+1
 
depth_glden=file_len(sys.argv[1])
depth_rcvd=file_len(sys.argv[2])
print("\n==============================================\n");
print("depth of gldn.txt --> %s" %depth_glden)
print("depth of rcvd.txt --> %s\n" %depth_rcvd)

gldn=open(sys.argv[1],"r")
rcvd=open(sys.argv[2],"r")

num_lines_block=sys.argv[3]
num_lines_block_int=int(num_lines_block)

if(num_lines_block_int > depth_rcvd):
  print("num_lines_block --> %s" %num_lines_block)
  print('ERROR : Blk_length passed is greater than file length \n')
  error=1
else:  
  print("num_lines_block --> %d" %num_lines_block_int)
  print("\n==============================================\n");
 
  req_gldn_list = [ ]
  rcvd_line_list_blk = [ ]
  gldn_line_list_full = [ ]
  rcvd_line_list_full = [ ]
  rcvd_line_list_after_lock = [ ]
  gldn_line_list_after_lock = [ ]
   
  for rcvd_len in range (0,depth_rcvd,1):
    rcvd_line_list_full.append(rcvd.readline())
 
  for gldn_len in range (0,depth_glden,1):
    gldn_line_list_full.append(gldn.readline())
 
  for blk_len in range(0,num_lines_block_int,1):
    rcvd_line_list_blk.append(rcvd_line_list_full[blk_len])
 
  j=0
 
  while (j != depth_glden-1):
    if(j+num_lines_block_int > depth_glden):
      error=1
      print('\n\nSCRIPT_INFO : COMPARE_BLOCK_PYTHON -- golden.txt EOF reached : TEST FAILED \n\n')
      break
    else:
      for blk_len in range(j,j+num_lines_block_int,1):
        req_gldn_list.append(gldn_line_list_full[blk_len])
   
    if rcvd_line_list_blk == req_gldn_list:
      error=0
      print('\n\nSCRIPT_INFO : COMPARE_BLOCK_PYTHON : LOCK ACHIEVED at index %s to %s of gldn.txt'%(j+1,(j+num_lines_block_int)))

      last_matched_location_gldn = j+num_lines_block_int
      last_matched_location_rcvd = num_lines_block_int

      effective_min_depth=min((depth_glden-(j-1)),depth_rcvd)

      for loop_rcvd in range (last_matched_location_rcvd,effective_min_depth,1):
        rcvd_line_list_after_lock.append(rcvd_line_list_full[loop_rcvd])

      for loop_gldn in range (last_matched_location_gldn,last_matched_location_gldn+effective_min_depth-last_matched_location_rcvd,1):
        gldn_line_list_after_lock.append(gldn_line_list_full[loop_gldn])

      if(rcvd_line_list_after_lock == gldn_line_list_after_lock):
        error=0
        print('\nSCRIPT_INFO : COMPARE_BLOCK_PYTHON : TEST PASSED\n\n')
      else:
        error=1
        print('\nSCRIPT_INFO : COMPARE_BLOCK_PYTHON : DATA MISMATCH : TEST FAILED AFETR INITIAL BLOCK MATCHED \n\n')

      break

    else:
      del req_gldn_list[:]
      error=1
      j=j+1
  if(j==depth_glden-1):
    print('SCRIPT_INFO : COMPARE_BLOCK_PYTHON : LOCK NOT ACHIEVED : TEST FAILED \n\n')

#sys.exit(error)

gldn.close()
rcvd.close()
