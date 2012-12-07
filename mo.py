#! /usr/bin/python
import pymongo
import time

NUM = 10000
SAFING = True	# Experimentally, this seems to make Mongo about 3 times slower

print "SAFE=",SAFING

def spong(a):
# Because most pymongo calls are "lazy", we "use" the results to force it to actually do the work ... with this dummy call
	# print a
	pass

db = pymongo.Connection().exampledatabase
collection = db.things

print NUM,"Inserts"
t1 = time.time()
c1 = time.clock()
for x in range(NUM):
	collection.insert({"x":1, "tags": ["dog","cat"]}, safe=SAFING)
t2 = time.time()

print "Find"
docs1 = collection.find({"x" : {"$exists" : True}})	# Find all objects which have an attribute x
docs1_count=0
for doc in docs1:
	spong(doc)	
	docs1_count+=1
t3 = time.time()

print "Update"
# collection.update({"x" : 1},{"x" : 2}, safe=SAFING)	# Only updates 1 match
collection.update({"x" : 1}, {"$set" : {"x" : 2}}, multi=True, safe=SAFING) # $set changes just that one attribute of each matching document
t4 = time.time()

print "Find"
docs2 = collection.find({"x" : {"$exists" : True}})
docs2_count = 0
for doc in docs2:
	spong(doc)
	docs2_count+=1
t5 = time.time()

collection.remove({"x" : {"$exists" : True}}, safe=SAFING)	# Remove ALL matching docs!
t6 = time.time()
c6 = time.clock()

print "Inserting "+str(NUM)+" objects took",t2-t1,"secs (",int(NUM/(t2-t1)),"/sec)"
print "Finding",docs1_count," objects took",t3-t2,"secs (",int(docs1_count/(t3-t2)),"/sec)"
print "Updating took",t4-t3,"secs"
print "Finding",docs2_count," objects took",t5-t4,"secs"
print "Removing objects took",t6-t5,"secs"
print
print "Total elapsed realtime:",t6-t1,"secs"
print "Total CPU time:",c6-c1,"secs"
