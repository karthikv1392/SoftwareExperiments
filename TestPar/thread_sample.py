import Queue
import threading
import time
import subprocess # To call the maven script within thread
import os
from Logging import logger
exitFlag = 0
#threadList = ["Thread-1", "Thread-2", "Thread-3","Thread-4","Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10"]
#threadList = ["Thread-1"]
threadList = []

num_threads=3
for index in range(0,num_threads,1):
    threadList.append("Thread-"+str(index))

print threadList
nameList = ["6", "10", "11", "16", "22","25","26","27","29","30","31","32"]
label_map = {0: 'crystal.client.ClientPreferencesTest.testAddProjectPreferences', 1: 'crystal.client.ClientPreferencesTest.testClone', 2: 'crystal.client.ClientPreferencesTest.testDuplicateAddProjectPreferences', 3: 'crystal.client.ProjectPreferencesTest.testProjectPreferences', 4: 'crystal.client.ClientPreferencesTest.testClientPreferences', 5: 'crystal.client.ClientPreferencesTest.testRemoveProjectPreferencesAtIndex', 6: 'crystal.client.ClientPreferencesTest.testDefaultSetting', 7: 'crystal.client.ConflictDaemonTest.testLocalState', 8: 'crystal.client.ClientPreferencesTest.testDuplicateProject', 9: 'crystal.client.ClientPreferencesTest.testRemoveProjectPreferences', 10: 'crystal.client.ClientPreferencesTest.testSavePreferencesToXML', 11: 'crystal.client.ConflictDaemonTest.testAddListener', 12: 'crystal.client.ConflictDaemonTest.testGetInstance', 13: 'crystal.client.ConflictDaemonTest.testPrePerformCalculations', 14: 'crystal.client.ProjectPreferencesTest.testNullInputConstructor', 15: 'crystal.client.ProjectPreferencesTest.testClone', 16: 'crystal.client.ConflictDaemonTest.testRelationship', 17: 'crystal.client.ProjectPreferencesTest.testAddDataSource', 18: 'crystal.client.ProjectPreferencesTest.testDuplicateAddDataSource', 19: 'crystal.client.ProjectPreferencesTest.testGetProjectCheckoutLocation', 20: 'crystal.client.ProjectPreferencesTest.testGetNumOfVisibleSources', 21: 'crystal.client.ProjectPreferencesTest.testRemoveDataSource', 22: 'crystal.model.DataSourceTest.testIsHidden', 23: 'crystal.model.DataSourceTest.testSetField', 24: 'crystal.model.DataSourceTest.testSetCloneString', 25: 'crystal.model.DataSourceTest.testSetCompileCommand', 26: 'crystal.model.DataSourceTest.testSetEnabled', 27: 'crystal.model.DataSourceTest.testSetHistory', 28: 'crystal.model.DataSourceTest.testSetKind', 29: 'crystal.model.DataSourceTest.testSetParent', 30: 'crystal.model.DataSourceTest.testSetRemoteCmd', 31: 'crystal.model.DataSourceTest.testToString', 32: 'crystal.model.LocalStateResultTest.testGetLastAction', 33: 'crystal.model.LocalStateResultTest.testToString'}
inverse_map = {0: 'org.apache.xml.security.test.algorithms.implementations.BlockEncryptionTest#test_AES192', 1: 'org.apache.xml.security.test.algorithms.implementations.BlockEncryptionTest#test_AES128', 2: 'org.apache.xml.security.test.algorithms.implementations.BlockEncryptionTest#test_AES256', 3: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_3DES', 4: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_AES_41', 5: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_AES_42', 6: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_AES_43', 7: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_AES_44', 8: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_AES_45', 9: 'org.apache.xml.security.test.algorithms.implementations.KeyWrapTest#test_AES_46', 10: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315ExclusiveTest#testA', 11: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test31', 12: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test31withComments', 13: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test32', 14: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test33', 15: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test34validatingParser', 16: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test35', 17: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test36', 18: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test37', 19: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#test37byNodeList', 20: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#testRelativeNSbehaviour', 21: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#testTranslationFromUTF16toUTF8', 22: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#testXMLAttributes1', 23: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#testXMLAttributes2', 24: 'org.apache.xml.security.test.c14n.implementations.Canonicalizer20010315Test#testXMLAttributes3', 25: 'org.apache.xml.security.test.c14n.implementations.ExclusiveC14NInterop#test_Y1', 26: 'org.apache.xml.security.test.c14n.implementations.ExclusiveC14NInterop#test_Y2', 27: 'org.apache.xml.security.test.c14n.implementations.ExclusiveC14NInterop#test_Y3', 28: 'org.apache.xml.security.test.c14n.implementations.ExclusiveC14NInterop#test_Y5', 29: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_enveloped_dsa', 30: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_enveloping_b64_dsa', 31: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_enveloping_dsa', 32: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_enveloping_hmac_sha1', 33: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_enveloping_hmac_sha1_40', 34: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_enveloping_rsa', 35: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_external_b64_dsa', 36: 'org.apache.xml.security.test.interop.BaltimoreTest#test_fifteen_external_dsa', 37: 'org.apache.xml.security.test.interop.BaltimoreTest#test_sixteen_external_dsa', 38: 'org.apache.xml.security.test.interop.IAIKTest#test_coreFeatures_signatures_anonymousReferenceSignature', 39: 'org.apache.xml.security.test.interop.IAIKTest#test_coreFeatures_signatures_manifestSignature_core', 40: 'org.apache.xml.security.test.interop.IAIKTest#test_coreFeatures_signatures_manifestSignature_manifest', 41: 'org.apache.xml.security.test.interop.IAIKTest#test_coreFeatures_signatures_signatureTypesSignature', 42: 'org.apache.xml.security.test.interop.IAIKTest#test_signatureAlgorithms_signatures_dSASignature', 43: 'org.apache.xml.security.test.interop.IAIKTest#test_signatureAlgorithms_signatures_hMACShortSignature', 44: 'org.apache.xml.security.test.interop.IAIKTest#test_signatureAlgorithms_signatures_hMACSignature', 45: 'org.apache.xml.security.test.interop.IAIKTest#test_signatureAlgorithms_signatures_rSASignature', 46: 'org.apache.xml.security.test.interop.IAIKTest#test_transforms_signatures_base64DecodeSignature', 47: 'org.apache.xml.security.test.interop.IAIKTest#test_transforms_signatures_c14nSignature', 48: 'org.apache.xml.security.test.interop.IAIKTest#test_transforms_signatures_envelopedSignatureSignature', 49: 'org.apache.xml.security.test.interop.IAIKTest#test_transforms_signatures_xPathSignature', 50: 'org.apache.xml.security.test.interop.RSASecurityTest#test_enveloped', 51: 'org.apache.xml.security.test.interop.RSASecurityTest#test_enveloping', 52: 'org.apache.xml.security.test.transforms.implementations.TransformBase64DecodeTest#test1', 53: 'org.apache.xml.security.test.transforms.implementations.TransformBase64DecodeTest#test2', 54: 'org.apache.xml.security.test.transforms.implementations.TransformBase64DecodeTest#test3'}

queueList = []
dictionary_list = {0: [1, 2, 3], 1: [3], 2: [1, 7, 3], 3: [], 4: [1, 5, 3], 5: [1, 9, 3], 6: [4, 1, 3], 7: [12, 13, 15, 14, 3], 8: [0, 1, 3], 9: [1, 8, 3], 10: [1, 3], 11: [12, 7, 13, 14, 3], 12: [], 13: [12, 14, 3], 14: [], 15: [19, 3], 16: [12, 7, 13, 14, 3], 17: [18, 3], 18: [3], 19: [3, 21], 20: [17, 3], 21: [20, 3], 22: [23], 23: [], 24: [23], 25: [23], 26: [23], 27: [23], 28: [23], 29: [23], 30: [23], 31: [24, 23, 28], 32: [33], 33: []}
finished_list = []
queueLock = threading.Lock()
workQueue = Queue.Queue(100)
threads = []
threadID = 1
start = time.time()
print "start Time ",  start
print (os.system(""))

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

def process_data(threadName, q):
   while not exitFlag:
      #queueLock.acquire()
      if not workQueue.empty():


          data = q.get()
          #print str(data) + "\n"
          #print inverse_map[int(data)]

          script_text = "mvn -Dtest="+ inverse_map[int(data)]+" test"
          directory = "cd " + "/Users/karthik/Documents/GSSI_Coursework/core/Software/Testing/pradet-replication/experimental-study/xmlsecurity/"

          # print finished_list
          #queueLock.release()
          #print script_text
          #print directory
          #subpr    ocess.call(script_text,cwd=directory)
          #os.system(directory+ ";" +script_text)

          queueLock.acquire()
          print threadName, list(workQueue.queue)
          finished_list.append(int(data))
          for edges in dictionary_list[int(data)]:
              if edges not in finished_list and edges not in queueList:
                  q.put(edges)
                  queueList.append(edges)
          queueLock.release()
          #print "%s processing test case%s" % (threadName, data)
      #else:
      #    queueLock.release()
          #time.sleep(1)


# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
    queueList.append(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print "Exiting Main Thread"

end = time.time()
print "end time " , end
print "elapsed time", end-start