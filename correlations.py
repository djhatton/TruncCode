import os
import sys
import copy
import gvar as gv
from gvar import sqrt

def full_average(file_name):
        data_set = gv.dataset.Dataset(file_name)
        return gv.dataset.avg_data(data_set)

def cfg_average(gpl_data):
        cfg_copy = copy.deepcopy(gpl_data[0])
        for i in range(1,len(gpl_data)):
                tag = gpl_data[i].keys()[0]
                for j in range(len(gpl_data[i][tag])):
                        cfg_copy[tag][j] += gpl_data[i][tag][j]
        for p in range(len(cfg_copy[tag])):
                cfg_copy[tag][p] = gv.gvar(cfg_copy[tag][p].mean/float(len(gpl_data)),cfg_copy[tag][p].sdev/float(len(gpl_data)))
        return cfg_copy

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

def ts_sigma(data,time_sources):
        deltas = delta_func(data,time_sources)
        tag = deltas[0].keys()[0]
        delta_squareds = []
        for i in range(len(data)):
                curr_delta_squared = []
                curr_delta_squared_dict = gv.BufferDict()
                for j in range(len(deltas[i][tag])):
                        curr_delta_squared.append(deltas[i][tag][j]**2)
                curr_delta_squared_dict.update({tag:curr_delta_squared})
                delta_squareds.append(curr_delta_squared_dict)
        sigma_squared = cfg_average(delta_squareds)
        tag = sigma_squared.keys()[0]
        sigma = gv.BufferDict()
        sigma_list = []
        for i in range(len(sigma_squared[tag])):
                sigma_list.append(sqrt(sigma_squared[tag][i]))
        sigma.update({tag:sigma_list})
        return sigma

def delta_func(data,time_sources):
        fout = open('temp.gpl','w')
        for i in range(len(data)):
                write_gpl_file_no_close(fout,data[i][time_sources[i]])
        fout.close()
        expectation_vals = full_average('temp.gpl')
	os.remove('temp.gpl')
        deltas = []
        tag = data[0][0].keys()[0]
        tag_02 = expectation_vals.keys()[0]
        for i in range(len(data)):
                delta = []
                delta_dict = gv.BufferDict()
                for j in range(len(data[i][time_sources[i]][tag])):
                        delta.append(data[i][time_sources[i]][tag][j] - expectation_vals[tag_02][j])
                delta_dict.update({tag:delta})
                deltas.append(delta_dict)
        return deltas

def correlation_ggp(data,time_source_01,time_source_02):
        sigma_01 = ts_sigma(data,time_source_01)
        sigma_02 = ts_sigma(data,time_source_02)
        delta_01 = delta_func(data,time_source_01)
        delta_02 = delta_func(data,time_source_02)
        deltas = delta_mult(delta_01,delta_02,data,data)
        numerator = cfg_average(deltas)
        tag = data[0][0].keys()[0]
        tag_01 = sigma_01.keys()[0]
        tag_02 = sigma_02.keys()[0]
        sigma_product = gv.BufferDict()
        sigma_product_list = []
        for i in range(len(sigma_01[tag])):
                sigma_product_list.append(sigma_01[tag_01][i]*sigma_02[tag_02][i])
        sigma_product.update({tag_01:sigma_product_list})
        tag = numerator.keys()[0]
        result = gv.BufferDict()
        result_list = []
        for i in range(len(numerator[tag])):
                result_list.append(numerator[tag][i]/sigma_product[tag_01][i])
        result.update({tag:result_list})
        return result

def ts_sigma(data,time_sources):
        deltas = delta_func(data,time_sources)
        tag = deltas[0].keys()[0]
        delta_squareds = []
        for i in range(len(data)):
                curr_delta_squared = []
                curr_delta_squared_dict = gv.BufferDict()
                for j in range(len(deltas[i][tag])):
                        curr_delta_squared.append(deltas[i][tag][j]**2)
                curr_delta_squared_dict.update({tag:curr_delta_squared})
                delta_squareds.append(curr_delta_squared_dict)
        sigma_squared = cfg_average(delta_squareds)
        tag = sigma_squared.keys()[0]
        sigma = gv.BufferDict()
        sigma_list = []
        for i in range(len(sigma_squared[tag])):
                sigma_list.append(sqrt(sigma_squared[tag][i]))
        sigma.update({tag:sigma_list})
        return sigma

def correlation_ggp(data,time_source_01,time_source_02):
        sigma_01 = ts_sigma(data,time_source_01)
        sigma_02 = ts_sigma(data,time_source_02)
        delta_01 = delta_func(data,time_source_01)
        delta_02 = delta_func(data,time_source_02)
        deltas = delta_mult(delta_01,delta_02,data,data)
        numerator = cfg_average(deltas)
        tag = data[0][0].keys()[0]
        tag_01 = sigma_01.keys()[0]
        tag_02 = sigma_02.keys()[0]
        sigma_product = gv.BufferDict()
        sigma_product_list = []
        for i in range(len(sigma_01[tag])):
                sigma_product_list.append(sigma_01[tag_01][i]*sigma_02[tag_02][i])
        sigma_product.update({tag_01:sigma_product_list})
        tag = numerator.keys()[0]
        result = gv.BufferDict()
        result_list = []
        for i in range(len(numerator[tag])):
                result_list.append(numerator[tag][i]/sigma_product[tag_01][i])
        result.update({tag:result_list})
        return result

def delta_mult(delta_01,delta_02,data_01,data_02):
        deltas = []
        tag_01 = data_01[0][0].keys()[0]
        tag_02 = data_02[0][0].keys()[0]
        for i in range(len(data_01)):
                delta = []
                delta_dict = gv.BufferDict()
                for j in range(len(data_01[i][0][tag_01])):
                        delta.append(delta_01[i][tag_01][j]*delta_02[i][tag_02][j])
                delta_dict.update({tag_01:delta})
                deltas.append(delta_dict)
        return deltas

def correlation_R(data,time_source_range,num_cfgs):
        rs = []
        for time_source_01 in range(time_source_range):
                for time_source_02 in range(time_source_range):
                        if time_source_01 != time_source_02:
				time_source_list_01 = [time_source_01]*num_cfgs
				time_source_list_02 = [time_source_02]*num_cfgs
                                rs.append(correlation_ggp(data,time_source_list_01,time_source_list_02))
        rs_copy = copy.deepcopy(rs[0])
        for i in range(1,len(rs)):
                tag = rs[i].keys()[0]
                for j in range(len(rs[i][tag])):
                        rs_copy[tag][j] += rs[i][tag][j]
        for p in range(len(rs_copy[tag])):
                rs_copy[tag][p] = gv.gvar(rs_copy[tag][p].mean/float(len(rs)**2),rs_copy[tag][p].sdev/float(len(rs)**2))
        return rs_copy

def correlation_rg(data,data_appx,time_sources,num_cfgs):
	zeros = [0]*num_cfgs
        sigma = ts_sigma(data,zeros)
        sigma_appx = ts_sigma(data_appx,time_sources)
        delta = delta_func(data,zeros)
        delta_appx = delta_func(data_appx,time_sources)
        numerator = cfg_average(delta_mult(delta,delta_appx,data,data_appx))
        tag = data[0][0].keys()[0]
        tag_01 = sigma.keys()[0]
        tag_02 = sigma_appx.keys()[0]
        sigma_product = gv.BufferDict()
        sigma_product_list = []
        for i in range(len(sigma[tag])):
                sigma_product_list.append(sigma[tag_01][i]*sigma_appx[tag_02][i])
        sigma_product.update({tag_01:sigma_product_list})
        tag = numerator.keys()[0]
        result = gv.BufferDict()
        result_list = []
        for i in range(len(numerator[tag])):
                result_list.append(numerator[tag][i]/sigma_product[tag_01][i])
        result.update({tag:result_list})
        return result

def write_gpl_file_no_close(fout,gpl_data):
        tag = gpl_data.keys()
        fout.write(tag[0] + '     ')
        for j in range(len(gpl_data[tag[0]])):
                fout.write(str(gpl_data[tag[0]][j].mean) + '     ')
        fout.write('\n')
        return None

def read_ts_file(file_name):
        fin = open(file_name,'r')
        file_lines = fin.readlines()
        result = []
        for line in file_lines:
                result.append(int(line))
        return result

def main():
	fine_file = sys.argv[1]
	sloppy_file = sys.argv[2]
	ts_file = sys.argv[3]
	n_cfgs = int(sys.argv[4])
	
	ts_data = read_ts_file(ts_file)
	fine_data = get_gpl_data(fine_file,n_cfgs,1)
	sloppy_data = get_gpl_data(sloppy_file,n_cfgs,16)
	#zeros = [0]*n_cfgs
	#print ts_sigma(fine_data,zeros)
	#print ts_sigma(sloppy_data,ts_data)
	#delta = delta_func(fine_data,zeros)
        #delta_appx = delta_func(sloppy_data,ts_data)
        #numerator = cfg_average(delta_mult(delta,delta_appx,fine_data,sloppy_data))
	#print numerator
	R = correlation_R(sloppy_data,16,n_cfgs)
	#rg = correlation_rg(fine_data,sloppy_data,ts_data,n_cfgs)
	print R
        #print rg
		
if __name__ == "__main__":
    sys.exit(main())
