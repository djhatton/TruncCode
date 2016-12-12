###########################################################################
# Dan Hatton								  #
# December 2016								  # 
# Merges gpl files for different source and sink operator combinations	  #
# A bit painfully done at the moment					  #
###########################################################################



import os
import sys
import gvar as gv

def main():
	pp_file = open(sys.argv[1],'r')
	pp_lines = pp_file.readlines()

	ps_file = open(sys.argv[2],'r')
        ps_lines = ps_file.readlines()
        
	sp_file = open(sys.argv[3],'r')
        sp_lines = sp_file.readlines()

	ss_file = open(sys.argv[4],'r')
        ss_lines = ss_file.readlines()
        
	new_lines = pp_lines+ps_lines+sp_lines+ss_lines
	for line in new_lines:
		sys.stdout.write(line)

if __name__ == "__main__":
    sys.exit(main())
