#############################################################################
# Dan Hatton                                                                #
# November 2016                                                             # 
# For writing improved estimator gpl file from truncated solver solutions   #
#############################################################################


import os
import sys
import gvar as gv

# gvar averaging of gpl file
# Produces gvar.BufferDict object
def full_average(file_name):
        data_set = gv.dataset.Dataset(file_name)
        return gv.dataset.avg_data(data_set)

# Read gpl file into list
# Individual correlator elements are gvar.gvar objects
def get_gpl_data(file_name,num_cfgs,num_time_sources):
        fin = open(file_name,'r')
	cfg_list = []
        for i in range(num_cfgs):
                time_source_list = []
                for j in range(num_time_sources):
                        line_num = 0
                        current_line = fin.readline()
                        split_line = current_line.split()
                        time_list = []
			#print split_line
                        tag = split_line[0]
                        for k in range(1,len(split_line)):
                                time_list.append(gv.gvar(float(split_line[k]),0.))
                        current_dict = {tag:time_list}
                        time_source_list.append(current_dict)
                cfg_list.append(time_source_list)
        fin.close()
        return cfg_list

# Averages over time sources
# Produces list of dictionaries, one for each configuration
def time_source_average(gpl_data):
        result = []
        for i in range(len(gpl_data)):
		fout = open('temp.gpl','w')
                for j in range(len(gpl_data[i])):
                        tag = gpl_data[i][j].keys()[0]
			fout.write(tag+'   ')
                        for k in range(len(gpl_data[i][j][tag])):
				fout.write(str(gpl_data[i][j][tag][k].mean)+'   ')
			fout.write('\n')
		fout.close()
		result.append(full_average('temp.gpl'))
		os.remove('temp.gpl')
        return result

# Compares two correlators to find differences
# Use on each configuration (after time source averaging) individually
def compare_data(data_01,data_02,new_tag):
        time_list = []
        tag_01 = data_01.keys()[0]
        tag_02 = data_02.keys()[0]
        for i in range(len(data_01[tag_01])):
                time_list.append(data_01[tag_01][i] - data_02[tag_02][i])
        result = {new_tag:time_list}
        return result

# Adds two correlators together
# Produces dictionary containing resulting correlator
def add_data(data_01,data_02,new_tag):
        time_list = []
        tag_01 = data_01.keys()[0]
        tag_02 = data_02.keys()[0]
        for i in range(len(data_01[tag_01])):
                time_list.append(data_01[tag_01][i] + data_02[tag_02][i])
        result = {new_tag:time_list}
        return result

# Writes gpl file
# One line for each configuration
# At this point error from time source averaging is lost; it is contained in gpl_data but not written out
def write_gpl_file(out_file,gpl_data):
        for i in range(len(gpl_data)):
                tag = gpl_data[i].keys()
                out_file.write(tag[0] + '     ')
                for k in range(len(gpl_data[i][tag[0]])):
                        out_file.write(str(gpl_data[i][tag[0]][k].mean) + '     ')
                out_file.write('\n')
   	out_file.close()
        return None

def read_ts_file(file_name):
	fin = open(file_name,'r')
	file_lines = fin.readlines()
	result = []
	for line in file_lines:
		result.append(int(line))
	return result

def main():
	# Fine gpl file must contain only one time source for each configuration
	fine_file = sys.argv[1]
	sloppy_file = sys.argv[2]
	fine_ts_file = sys.argv[3]
	n_cfgs = int(sys.argv[4])
	n_time_sources = 16

	fine_data = get_gpl_data(fine_file,n_cfgs,1)
	#print 'made it through fine'
	sloppy_data = get_gpl_data(sloppy_file,n_cfgs,n_time_sources)
	fine_time_sources = read_ts_file(fine_ts_file)
	
	time_avgd_sloppy_data = time_source_average(sloppy_data)
	time_avgd_fine_data = time_source_average(fine_data)
	imp_data = []
	diffs = []
	for i in range(len(time_avgd_sloppy_data)):
		tag = sloppy_data[0][0].keys()[0]
		diff = compare_data(fine_data[i][0],sloppy_data[i][fine_time_sources[i]],tag)
		diffs.append(diff)
		for j in range(len(sloppy_data[i])):
			imp_data.append(add_data(sloppy_data[i][j],diff,tag))
	write_gpl_file(sys.stdout,imp_data)
	#write_gpl_file(sys.stdout,diffs)

if __name__ == "__main__":
    sys.exit(main())
