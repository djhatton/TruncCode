import os
import sys

def main():
	in_file = sys.argv[1]
	fin = open(in_file,'r')
	lines = fin.readlines()
	for index,line in enumerate(lines):
		lines[index] = int(line)
		sys.stdout.write(str(((lines[index]-(19*(5*index+60)/5)%(48/16))/(48/16)))+'\n')

if __name__ == "__main__":
    sys.exit(main())
