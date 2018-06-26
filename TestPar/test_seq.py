_Author_ = "Karthik Vaidhyanathan and Mohammand Abouei Mehrizi"

# Parallelizing Test cases using PRADET approach
# Course project on Software Testing
# Gran Sasso Science Institute
# Script to execute the test cases in a sequential manner
import time
import os


def find_sequential():
    # Function that basically finds all the sequential test cases by comparison with the original one
    print "sequential"


def get_test_cases():
    path = "/Users/karthik/Documents/GSSI_Coursework/core/Software/Testing/pradet-replication/experimental-study/xmlsecurity/"
    fileName = "test-execution-order"
    complete_name = path + fileName
    f = open(complete_name, 'r')
    difference_list= []
    for line in f:
        # The script section
        split_text = line.strip("\n").split('.')
        last_text = line.rsplit('.', 1)[0]
        # print last_text + "#" + split_text[-1]
        new_text = last_text + "#" + split_text[-1]

        script_text = "mvn -Dtest="+new_text+ " test"
        #print script_text
        directory = "cd " + "/Users/karthik/Documents/GSSI_Coursework/core/Software/Testing/pradet-replication/experimental-study/xmlsecurity/"

        command =  directory + ";"+script_text
        #print command
        out = os.popen(command)
        #print out.readlines()[-5]




if __name__ == '__main__':
    start = time.time()
    print "start time " , start

    get_test_cases()

    end = time.time()
    print "end time ", end

    print "elapsed ", end-start