import os
import sys
import gvar as gv

def full_average(file_name):
        data_set = gv.dataset.Dataset(file_name)
        return gv.dataset.avg_data(data_set)

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
                        tag = split_line[0]
                        for k in range(1,len(split_line)):
                                time_list.append(gv.gvar(float(split_line[k]),0.))
                        current_dict = {tag:time_list}
                        time_source_list.append(current_dict)
                cfg_list.append(time_source_list)
        fin.close()
        return cfg_list

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

def write_gpl_file(out_file,gpl_data):
        for i in range(len(gpl_data)):
                tag = gpl_data[i].keys()
                out_file.write(tag[0] + '     ')
                for k in range(len(gpl_data[i][tag[0]])):
                        out_file.write(str(gpl_data[i][tag[0]][k].mean) + '     ')
                out_file.write('\n')
        out_file.close()
        return None

def main():
	gpl_file = sys.argv[1]
	n_cfgs = int(sys.argv[2])
	n_time_sources = 16
	data = get_gpl_data(gpl_file,n_cfgs,n_time_sources)
	result = time_source_average(data)
	write_gpl_file(sys.stdout,result)

if __name__ == "__main__":
    sys.exit(main())
