import os
import sys
import gvar as gv

def full_average(file_name):
        data_set = gv.dataset.Dataset(file_name)
        return gv.dataset.avg_data(data_set)

def get_gpl_data(file_name,num_cfgs,num_time_sources):
        fin = open(file_name,'r')
        vec_list = []
	for i in range(3):
		cfg_list = []
        	for j in range(num_cfgs):
                	time_source_list = []
                	for k in range(num_time_sources):
                        	line_num = 0
                        	current_line = fin.readline()
                        	split_line = current_line.split()
                        	time_list = []
                        	tag = split_line[0]
                        	for p in range(1,len(split_line)):
                                	time_list.append(gv.gvar(float(split_line[p]),0.))
                        	current_dict = {tag:time_list}
                        	time_source_list.append(current_dict)
                	cfg_list.append(time_source_list)
		vec_list.append(cfg_list)
        fin.close()
        return vec_list

def vector_average(gpl_data):
        result = []
	for i in range(len(gpl_data[0])):
		time_source_list = []
        	for j in range(len(gpl_data[0][0])):
                	fout = open('temp.gpl','w')
                	for k in range(len(gpl_data)):
                        	tag = gpl_data[k][i][j].keys()[0]
                        	fout.write(tag+'   ')
                        	for p in range(len(gpl_data[k][i][j][tag])):
                                	fout.write(str(gpl_data[k][i][j][tag][p].mean)+'   ')
                        	fout.write('\n')
                	fout.close()
                	time_source_list.append(full_average('temp.gpl'))
                	os.remove('temp.gpl')
		result.append(time_source_list)
        return result

def write_gpl_file(out_file,gpl_data):
        for i in range(len(gpl_data)):
		for j in range(len(gpl_data[i])):
                	tag = gpl_data[i][j].keys()
                	out_file.write(tag[0] + '     ')
                	for k in range(len(gpl_data[i][j][tag[0]])):
                        	out_file.write(str(gpl_data[i][j][tag[0]][k].mean) + '     ')
                	out_file.write('\n')
        out_file.close()
        return None

def main():
	vec_file = sys.argv[1]
	n_cfgs = int(sys.argv[2])
	n_time_sources = int(sys.argv[3])
	vec_data = get_gpl_data(vec_file,n_cfgs,n_time_sources)
	vec_avg_data = vector_average(vec_data)
	write_gpl_file(sys.stdout,vec_avg_data)

if __name__ == "__main__":
    sys.exit(main())
