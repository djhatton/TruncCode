import os
import sys

def main():
        x_file = open(sys.argv[1],'r')
        x_lines = x_file.readlines()

        y_file = open(sys.argv[2],'r')
        y_lines = y_file.readlines()

        z_file = open(sys.argv[3],'r')
        z_lines = z_file.readlines()

	new_x_lines = []
	new_y_lines = []
	new_z_lines = []

	for i in range(len(x_lines)):
		x_line = x_lines[i].split()
		y_line = y_lines[i].split()
		z_line = z_lines[i].split()
		x_line[0] = sys.argv[4]
		y_line[0] = sys.argv[4]
		z_line[0] = sys.argv[4]
		new_x_line = ''
		new_y_line = ''
		new_z_line = ''
		for j in range(len(x_line)):
			new_x_line += x_line[j]+'   '
			new_y_line += y_line[j]+'   '
			new_z_line += z_line[j]+'   '
		new_x_line += '\n'
		new_y_line += '\n'
		new_z_line += '\n'
		new_x_lines.append(new_x_line)
		new_y_lines.append(new_y_line)
		new_z_lines.append(new_z_line)		

        new_lines = new_x_lines+new_y_lines+new_z_lines
        for line in new_lines:
                sys.stdout.write(line)

if __name__ == "__main__":
    sys.exit(main())
