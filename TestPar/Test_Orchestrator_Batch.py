_Author_ = "Karthik Vaidhyanathan and Mohammand Abouei Mehrizi"

# Parallelizing Test cases using PRADET approach
# Course project on Software Testing
# Gran Sasso Science Institute

from ConfigParser import SafeConfigParser
from Logging import logger
import csv
import Queue
import threading
import time
import os
import traceback
import test_seq

CONFIG_FILE = "settings.conf"
CONFIG_SECTION = "settings"

global exitFlag  # This is for the mult-threading to symbolize when the queue is empty
exitFlag = 0
global threadID
threadID = 1
inverse_map = {} # For the multi threading module
finished_list = [] # To keep track of the nodes that have finished executing parallely
queue_list = []   # To keep track of the elements in the queue
dictionary_list = [] # For providing the reverse mapping
global thread_list   # for the threads to be filled
thread_list = []
global sequence_list
sequence_list = []  # To store the nodes in sequence
threads = [] # To keep track of the running threads

class Test_Orchestrator():
    # Main class that is responsible for reading config files
    # Handling the pre-processing the functions

    file_name = "deps.csv"    # Default name for the dependencies for CSV
    data_path = ""
    test_dir = ""
    num_threads = ""
    threadID = 1
    test_execution_order = "test-execution-order"
    def __init__(self):
        logger.info("Initializing the orchestrator")
        parser = SafeConfigParser()
        parser.read(CONFIG_FILE)
        try:
            global thread_list
            self.file_name = parser.get(CONFIG_SECTION, "fileName")
            self.data_path = parser.get(CONFIG_SECTION,"data")
            self.test_dir  = parser.get(CONFIG_SECTION,"test_dir")
            self.num_threads = parser.get(CONFIG_SECTION,"num_threads")
            self.test_execution_order = parser.get(CONFIG_SECTION,"test_order_file")
            # Initializ the thread list as per the number of threads in the configuration
            for index in range(0, int(self.num_threads), 1):
                thread_list.append("Thread-" + str(index))
            #print thread_list
        except:
            traceback.print_exc()
            logger.error("Error in reading configuration file")



    def label_generator(self, csv_object):
        # Take the graph and give labels to each of the nodes
        # This is particulary used for performing computation of Strongly connected components
        logger.info("Generating the label map")
        label_map = {}
        key = 0  # This is the start value
        for row in csv_object:
            if row[0] not in label_map:
                label_map[row[0]] = key
                key = key + 1
            if row[1] not in label_map:
                label_map[row[1]] = key
                key = key + 1

        return label_map


    def inverse_label_generator(self,label_map):
        # This inverses the total dictionary
        #inv_map = {v: k for k, v in label_map.iteritems()}
        logger.info("Generating the inverse label map")
        reverse_map = {}
        for key,value in label_map.iteritems():
            split_text = key.split('.')
            last_text = key.rsplit('.', 1)[0]
            #print last_text + "#" + split_text[-1]
            new_text = last_text + "#" + split_text[-1] # This step is done for Maven test execution from command line
            reverse_map[value] = new_text
        return reverse_map

    def reverse_adjacency(self, adjacency_list):
        # This will pring the adjacency list in the reverse way so that it can be used to compute the nodes with no incoming
        # arcs to be used for parallel execution

        logger.info("Generating the reverse adjacency")
        reverse_list = {}
        for node in adjacency_list:
            reverse_list[node] = []

        for node in adjacency_list:
            for edge in adjacency_list[node]:
                reverse_list[edge].append(node)
        return reverse_list

    def node_list_generator(self,reverse_adj_list):
        # This function is used to output the nodes that does not have any incoming arcs
        logger.info(" Generating the node list")
        node_list = []
        for node in reverse_adj_list:
            if len(reverse_adj_list[node]) == 0:
                node_list.append(str(node))

        return node_list

    def sequential_test_set_generator(self,label_map):
        # This finds the test cases that needs to be executed sequentially if they are not in the dependency file
        # Take label map as input and then compare
        logger.info("inside the sequential test case executor")
        reverse_dict = {}
        reverse_dict = {value: key for key, value in label_map.iteritems()}
        file_name = self.test_dir + self.test_execution_order
        try:
            file_object = open(file_name, 'r')
            sequence_list = []         # To find the test cases that needs to be executed in sequence
            for line in file_object:
                test_case = line.strip("\n")
                if test_case not in reverse_dict:
                    sequence_list.append(test_case)

            return sequence_list    # Returns the sequence of test case that needs to be executed

        except Exception as e:
            logger.error("Error in executing test cases in sequence ",e)


    def adjacency_list_generator(self,csv_obj,label_map):
        # Create the adjacecny list representation
        # use the csv_obj  and label_map as input to create the list representation
        logger.info("Adjacency list generator")
        adjacency_map = {} # Initializ the map with 0 values
        for row in csv_obj:
            adjacency_map[label_map[row[0]]] = []
            adjacency_map[label_map[row[1]]] = []

        csv_obj2 = read_csv()
        for row2 in csv_obj2:
            adjacency_map[label_map[row2[1]]].append(label_map[row2[0]])

        return adjacency_map



test_orch_object = Test_Orchestrator() # Instantiate the object to call the calss to create the inverse  map
# Better to keep the thread processing outside the class
# Add the threading logic here
workQueue = Queue.Queue(100)
queueLock = threading.Lock()  # For accessing the critical region when performing the writes


def process_data(threadName, q):
   while not exitFlag:
      #queueLock.acquire()
      if not workQueue.empty():
          data = q.get()
          script_text = "mvn -Dtest="+ inverse_map[int(data)]+" test"
          directory = "cd " + test_orch_object.test_dir

          #print directory + ";" + script_text

          #out = os.popen(directory+ ";" +script_text)

          queueLock.acquire()
          # print out.readlines()[-6]
          #print threadName, list(workQueue.queue)
          finished_list.append(int(data))
          if int(data) in dictionary_list.keys():
              for edges in dictionary_list[int(data)]:
                  if edges not in finished_list and edges not in queue_list:
                      q.put(edges)
                      queue_list.append(edges)
          #print list(q.queue)
          queueLock.release()

          logger.info("%s processing test case%s" % (threadName, data))

def read_csv():
    # Reads the csv and returns the file object
    logger.info(" reading the dependency file")
    try:
        fname = test_orch_object.data_path + test_orch_object.file_name
        file = open(fname, 'ra')
        csv_f = csv.reader(file, delimiter=',')
        return csv_f

    except:
        logger.error("Error in reading the input dependency file")

    return None

class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print "Starting " + self.name
      process_data(self.name, self.q)
      print "Exiting " + self.name

def parallel_executor(node_list):
    # This is responsible for the parallel execution of the test cases
    # Get the node list from the calling function and use it to fill the inital queue for execution

    #logger.info("start time ",start_time)
    global exitFlag
    global threadID
    logger.info("Starting the parallel execution")
    #print thread_list
    for tName in thread_list:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    queueLock.acquire()
    for node in node_list:
        workQueue.put(node)
        queue_list.append(node)
    queueLock.release()

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    print "Exiting Main Thread"

    #logger.info("end time ",end_time)
    #logger.info("Elapsed time :",end_time-start_time)


def get_test_cases(lablel_map):
    # Takes the label map as the input to find the test cases that has to be executed in sequence
    logger.info("Checking for sequential test cases")
    path = test_orch_object.test_dir
    fileName = "test-execution-order"
    complete_name = path + fileName
    f = open(complete_name, 'r')
    difference_list= []
    file_list = []
    for line in f:
        # The script section
        item = line.strip("\n")
        if item not in label_map.keys():
            file_list.append(item)

    return file_list

if __name__ == '__main__':

    #global sequence_list
    csv_object = read_csv()
    label_map = test_orch_object.label_generator(csv_object)

    sequence_list = get_test_cases(label_map)

    # add all the nodes to the lab;
    start_key = max(label_map.values()) + 1
    for test in sequence_list:
        label_map[test] = start_key
        start_key = start_key + 1

    inverse_map = test_orch_object.inverse_label_generator(label_map)

    csv_object2 = read_csv() # To reinitialize the object as the old object would be closed
    dictionary_list = test_orch_object.adjacency_list_generator(csv_object2,label_map)
    print dictionary_list
    reverse_list = test_orch_object.reverse_adjacency(dictionary_list)
    print reverse_list
    #dictionary_list = reverse_list
    #print dictionary_list
    node_list = test_orch_object.node_list_generator(reverse_list)
    print node_list
    #print node_list
    #print node_list

    #print len(dictionary_list.keys())
    #print len(sequence_list)

    #print set(sequence_list).intersection(set(dictionary_list.keys()))    # to verify the correctness

    start_time = time.time()
    print "start time : ", start_time
    #print sequence_list
    #print label_map.keys()
    #if len(sequence_list) > 0:
    #    test_seq.get_test_cases(test_orch_object.test_dir,sequence_list)

    for node in sequence_list:
        node_list.append(label_map[node])

    parallel_executor(node_list)

    end_time = time.time()
    print "end time : ", end_time
    print "elapsed time ", end_time - start_time

    #print sequence_list
    #print len(sequence_list)









