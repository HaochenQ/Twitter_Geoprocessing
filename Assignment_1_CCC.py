#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mpi4py import MPI
import time
from collections import Counter
import json

start_time = time.time()
comm=MPI.COMM_WORLD
size=comm.Get_size()
rank=comm.Get_rank()

file_name='bigTwitter.json'
# Processing melbGrid file, get a dict all_grid contains id
# and border coordinates of each grid.
f1 = open('melbGrid.json', encoding='utf-8')
data = json.load(f1)
all_grid={}
postnum = {}  # save posts number in each grid
postrank = {}  # hold hashtags and occurrence in each grid
for item in data['features']:
   grid={}
   for pro in item['properties']:
       if pro=='id':
           id=item['properties']['id']
           postnum[id] = 0
           postrank[id] = {}
   grid["xmax"] = item['properties']["xmax"]
   grid["xmin"] = item['properties']["xmin"]
   grid["ymax"] = item['properties']["ymax"]
   grid["ymin"] = item['properties']["ymin"]
   # save border coordinates in all_grid
   all_grid[item['properties']['id']] = grid


# processing incoming data(one line of json file)
# updata postnum and postrank
def proess_data(data):
   cordx = data['doc']['coordinates']['coordinates'][0]
   cordy = data['doc']['coordinates']['coordinates'][1]
   for k,v in all_grid.items():  # tell which grid the tweet is in
       if all_grid[k]['xmin'] < cordx <= all_grid[k]['xmax'] and \
       (all_grid[k]['ymin'] <= cordy < all_grid[k]['ymax']):
           postnum[k]+=1  # counting posts number for each grid
           text=data['doc']['text'].split()  # turning text in to a list containing strings
           for string in text:
               # If a string start with # and length is over 1, then it is a hashtag
               if string[0] == "#"and len(string)>1:
                   hashtag = string.lower()  # converting all hashtag string into lower case
                   if  postrank[k].get(hashtag)is None:
                       postrank[k][hashtag] = 1
                   else:
                       postrank[k][hashtag] += 1


# formatting output postnum and postrank
def result(postnum, postrank):
   for grid in postnum.keys():  # use this loop update value of postrank as
       hashtg=postrank[grid]    # dictionary containing top five hashtags
       five_hashtag = tuple(sorted(hashtg.items(), key=lambda x: x[1], reverse=True)[:5])
       postrank[grid] = five_hashtag
   # use sorted function to sort postnum according to its value
   orderd_postnum = sorted(postnum.items(), key=lambda x: x[1], reverse=True)
   # print sorted postnum
   for each in orderd_postnum:
       print(each[0],':',each[1],'posts')
   print('\n')
   # print postrank in with the same order
   for each in orderd_postnum:
       print(each[0], ':', postrank[each[0]])
   print('\n')
   runtime = time.time() - start_time
   print('total running time:', runtime)


# allocating twitter data to different cores
with open(file_name, encoding='utf-8')as twitter:
   line_num=1
   for line in twitter:
       if (line_num-rank-1)%size==0:  # Each core get a line in turn
           try:
               one_post = json.loads(line[0:len(line) - 2])  # delete the coma at then end of line
               proess_data(one_post)
           except:
               try:
                   one_post = json.loads(line[0:len(line) - 1])  # for lines without coma at the end
                   proess_data(one_post)
               except:
                   line_num+=1
                   continue
       line_num+=1


# for multi cores mode, gathering postnum and postrank from each processor
if size ==1 and rank==0:  # for one core mode
   result(postnum, postrank)
elif size>1:  # for multi-cores mode
   #use gather method to merge postnum and postrank when rank ==0
   total_postnum = comm.gather(postnum, root=0)
   total_postrank = comm.gather(postrank, root=0)
   if rank==0:
       # update postnum and postrank
       for each_core in range(size-1):
           total_postnum[each_core+1]=Counter(total_postnum[each_core])+\
                                      Counter(total_postnum[each_core+1])
       postnum = total_postnum[size-1]
       for each_core in range(size-1):
           for k, v in total_postrank[each_core].items():
               total_postrank[each_core+1][k] = Counter(total_postrank[each_core][k]) + \
                                                Counter(total_postrank[each_core+1][k])
       postrank = total_postrank[size-1]
       result(postnum, postrank)



