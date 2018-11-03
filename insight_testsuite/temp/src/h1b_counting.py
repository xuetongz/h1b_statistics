#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 18:52:18 2018

@author: xuetong
"""
class H1B:
    def __init__(self, infile):
        '''
        initializing class, infile is the path of the dataset,
        required to be csv, header needed
        '''
        self.infile_path=infile
        self.wanted_fields = {}
        self.certified_count = 0

    def read_file(self,status,field_list):
        infile=open(self.infile_path)
        header=infile.readline().split(';')
        index_dic={}
        status_index=0
        for i in field_list:
            index_dic[i]= 0

        for i,field_name in enumerate(header):
             if 'STATUS' in field_name:
                  status_index=i
        for field in field_list:
            for i,field_name in enumerate(header):
                if field in field_name:
                    index_dic[field]=i

        for row in field_list:
            self.wanted_fields[row] = {}

        for data in infile.readlines():
            data= data.split(';')
            data = [x.strip('"') for x in data]
            for row_name in self.wanted_fields.keys():
                wanted_index = index_dic[row_name]
                if data[status_index]=='CERTIFIED':
                    self.certified_count+=1
                    if data[wanted_index] not in self.wanted_fields[row_name]:
                        self.wanted_fields[row_name][data[wanted_index]]=1
                    else:
                        self.wanted_fields[row_name][data[wanted_index]]+=1
        self.certified_count=self.certified_count/len(field_list)

    def sort_wanted_fields(self):
        for row_name, row_dict in self.wanted_fields.items():
            transfered_dict = [(k, v) for k, v in row_dict.items()]
            sroted_row_dict = sorted(transfered_dict, key=lambda x:(-x[1], x[0]))
            self.wanted_fields[row_name] = sroted_row_dict

    def get_top_n(self, row_name, top_n):
        '''
        input: a dictionary, and "n", the number of top items
        output: list of tuple sorted by value of dictionary list alphabetically
        '''
        return self.wanted_fields[row_name][:top_n]

    def write_file(self, row_name, wanted_name, top_n, path):
        with open(path, 'w') as f:
            f.write("TOP_{};NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n".format(wanted_name.upper()))
            for text, number in self.get_top_n(row_name, top_n):
                percentage = number*100 / self.certified_count
                line = ';'.join((str(text), str(number), "{0:.1f}%".format(percentage)))
                f.write(line + '\n')




if __name__ == '__main__':
    import sys
    input_path=sys.argv[1]
    occupation_path=sys.argv[2]
    state_path=sys.argv[3]
    h1b = H1B(input_path)
    h1b.read_file('CERTIFIED', ['SOC_NAME', 'WORKSITE_STATE'])
    h1b.sort_wanted_fields()
    h1b.write_file(
        "SOC_NAME",
        "occupations",
        10,
        path=occupation_path
    )
    h1b.write_file(
        "WORKSITE_STATE",
        "STATES",
        10,
        path=state_path
    )
