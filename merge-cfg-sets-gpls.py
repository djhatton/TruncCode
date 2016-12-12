import os
import sys

def main():
        file_01 = open(sys.argv[1],'r')
        lines_01 = file_01.readlines()

        file_02 = open(sys.argv[2],'r')
        lines_02 = file_02.readlines()

	n_cfgs_01 = int(sys.argv[3])
	n_cfgs_02 = int(sys.argv[4])
	n_comp = int(sys.argv[5])

	new_tag_lines_02 = []
	
        new_lines_01 = []
        new_lines_02 = []

	if len(lines_01) != n_comp*n_cfgs_01*4:
		print len(lines_01)
		print n_comp*n_cfgs_01*4
		print 'Wrong number of cfgs or smearings'
		return None

	if len(lines_02) != n_comp*n_cfgs_02*4:
		print len(lines_02)
		print n_comp*n_cfgs_02*4
                print 'Wrong number of cfgs or smearings'
                return None

        for i in range(4):
		curr_smear = []
   		for j in range(n_comp*n_cfgs_01):
			curr_smear.append(lines_01[n_comp*n_cfgs_01*i + j])
                new_lines_01.append(curr_smear)
        
	for i in range(len(lines_02)):
		line_02 = lines_02[i].split()
		if i < n_cfgs_02*n_comp:
			tag = lines_01[0].split()[0]
		elif i < 2*n_cfgs_02*n_comp:
			tag = lines_01[n_cfgs_01*n_comp].split()[0]
		elif i < 3*n_cfgs_02*n_comp:
			tag = lines_01[2*n_cfgs_01*n_comp].split()[0]
		elif i < 4*n_cfgs_02*n_comp:
                        tag = lines_01[3*n_cfgs_01*n_comp].split()[0]
		line_02[0] = tag
		curr_line = ''
		for j in range(len(line_02)):
			curr_line += line_02[j]+'   '
		curr_line += '\n'
		new_tag_lines_02.append(curr_line)

	for i in range(4):
                curr_smear = []
                for j in range(n_cfgs_02*n_comp):
                        curr_smear.append(new_tag_lines_02[n_cfgs_02*n_comp*i + j])
                new_lines_02.append(curr_smear)	

        for i in range(4):
		new_lines = new_lines_01[i]+new_lines_02[i]
        	for line in new_lines:
                	sys.stdout.write(line)

if __name__ == "__main__":
    sys.exit(main())
