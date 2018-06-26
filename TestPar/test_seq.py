_Author_ = "Karthik Vaidhyanathan and Mohammand Abouei Mehrizi"

# Parallelizing Test cases using PRADET approach
# Course project on Software Testing
# Gran Sasso Science Institute
# Script to execute the test cases in a sequential manner
import time
import os
from ConfigParser import SafeConfigParser

global test_dir

CONFIG_FILE = "settings.conf"
CONFIG_SECTION = "settings"

def read_configuratoins():
    global test_dir
    # Reads from the configuration file
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE)
    test_dir = parser.get(CONFIG_SECTION,"test_dir")

def find_sequential():
    # Function that basically finds all the sequential test cases by comparison with the original one
    print "sequential"


def get_test_cases(test_dir):
    #path = "/Users/karthik/Documents/GSSI_Coursework/core/Software/Testing/pradet-replication/experimental-study/xmlsecurity/"
    path = test_dir
    fileName = "test-execution-order"
    complete_name = path + fileName
    f = open(complete_name, 'r')
    difference_list= []
    file_list = []
    for line in f:
        # The script section
        split_text = line.strip("\n").split('.')
        last_text = line.rsplit('.', 1)[0]
        file_list.append(line.strip("\n"))
        # print last_text + "#" + split_text[-1]
        new_text = last_text + "#" + split_text[-1]

        script_text = "mvn -Dtest="+new_text+ " test"
        #print script_text
        directory = "cd " + test_dir

        command =  directory + ";"+script_text
        #print command
        #out = os.popen(command)
        #print out.readlines()[-5]

    #print file_list



if __name__ == '__main__':
    global test_dir
    start = time.time()
    print "start time " , start
    read_configuratoins()
    get_test_cases(test_dir)
    end = time.time()
    print "end time ", end
    print "elapsed ", end-start