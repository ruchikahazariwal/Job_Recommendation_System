#!/usr/bin/python
import sys

result_file_name = sys.argv[1]
test_file_name = 'apps2.tsv'

user_predicted_jobs = {}
with open(result_file_name, 'r') as result_file:
   result_file.readline()
   for line in result_file:
      user_id = line.strip().split(",")[0]
      jobs = line.strip().split(",")[1].split(" ")[0:150]
      jobs_set = set()
      user_predicted_jobs[user_id] = [x for x in jobs if x not in jobs_set and not jobs_set.add(x)]
      
user_actual_jobs = {}
with open(test_file_name, 'r') as test_file:
   test_file.readline()
   for line in test_file:
       (UserId, WindowID, Split, ApplicationDate, JobId) = line.strip().split('\t')
       if user_actual_jobs.has_key(UserId):
          user_actual_jobs[UserId].append(JobId)
       else:
          user_actual_jobs[UserId] = []

total_map = 0.0
for user_id in user_predicted_jobs:
   if not user_actual_jobs.has_key(user_id):
      continue
   total = len(user_actual_jobs[user_id])
   if total == 0: continue
   count = 0
   total_ap = 0.0
   for i in range(1,150):
      if len(user_predicted_jobs[user_id])<i: break
      if user_predicted_jobs[user_id][i-1] in user_actual_jobs[user_id]:
         count += 1
         total_ap += float(count)/i
   total_map += (total_ap/min(total, 10))
print total_map/len(user_predicted_jobs)
