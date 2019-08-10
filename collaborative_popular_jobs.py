#!/usr/bin/python
import csv
from collections import defaultdict as ddict

wd = "./" # The directory that the data files are in

user_ke_jobs = ddict(list)
job_ke_users = ddict(list)
user_ke_predicted_jobs = ddict(lambda: ddict(list))
print "Recording job loc"
job_info = {}
with open(wd + "./data/jobs.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() 
    for line in reader:
        (Jobid, WindowId, Title, Description, Requirements, City, State, 
        Country, Zip5, StartDate, EndDate) = line
        job_info[str(Jobid)] = [int(WindowId), State, City, 0]

print "Counting applications..."
with open(wd + "./data/apps1.tsv") as infile:
    reader = csv.reader(infile, delimiter="\t")
    reader.next()
    for line in reader:
        (UserId, WindowID, Split, ApplicationDate, JobId) = line
        if WindowID == 2: break
        user_ke_jobs[UserId].append(JobId)
        job_ke_users[JobId].append(UserId)

print "Finding similar jobs"
with open(wd + "./data/users.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() 
    for line in reader:
        (UserId, WindowId, Split, City, State, Country, ZipCode,
        DegreeType, Major, GraduationDate, WorkHistoryCount,
        TotalYearsExperience, CurrentlyEmployed, ManagedOthers,
        ManagedHowMany) = line
        if Split == "Train":
            continue
        for job_id in user_ke_jobs[UserId]:
           for user_id1 in job_ke_users[job_id]:
              for job_id1 in user_ke_jobs[user_id1]:
                 if job_id1 in user_ke_jobs[UserId]: break
                 if user_ke_predicted_jobs[UserId].has_key(job_id1):
                    user_ke_predicted_jobs[UserId][job_id1] += 1
                 else:
                    user_ke_predicted_jobs[UserId][job_id1] = 1

print "Sorting collaborative filtering jobs..."
predicted_job_tuples = ddict(list)
for user_id in user_ke_predicted_jobs.keys():
   for job_id, count in user_ke_predicted_jobs[user_id].items():
      predicted_job_tuples[user_id].append((job_id, count))
   predicted_job_tuples[user_id].sort(key=lambda x: x[1])
   predicted_job_tuples[user_id].reverse()

print "Sorting jobs on based on popularity..."
top_city_jobs = ddict(lambda: ddict(lambda: ddict(list)))
top_state_jobs = ddict(lambda: ddict(list))
for (job_id, (window, State, City, count)) in job_info.items():
    top_city_jobs[window][State][City].append((job_id, count))
    top_state_jobs[window][State].append((job_id, count))
for window in [1]:
    for state in top_city_jobs[window]:
        for city in top_city_jobs[window][state]:
            top_city_jobs[window][state][city].sort(key=lambda x: x[1])
            top_city_jobs[window][state][city].reverse()
    for state in top_state_jobs[window]:
        top_state_jobs[window][state].sort(key=lambda x: x[1])
        top_state_jobs[window][state].reverse()

print "Making predictions..."
with open(wd + "./data/users.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() # burn the header
    with open("./result/popular_jobs1.csv", "w") as outfile:
        outfile.write("UserId, JobIds\n")
        for line in reader:
            (UserId, WindowId, Split, City, State, Country, ZipCode,
            DegreeType, Major, GraduationDate, WorkHistoryCount,
            TotalYearsExperience, CurrentlyEmployed, ManagedOthers,
            ManagedHowMany) = line
            if Split == "Train":
                continue
            top_jobs = predicted_job_tuples[UserId]
            if len(top_jobs) < 150:
               top_jobs += top_city_jobs[int(WindowId)][State][City]
            if len(top_jobs) < 150:
                top_jobs += top_state_jobs[int(WindowId)][State]
            top_jobs = top_jobs[0:150]
            outfile.write(str(UserId) + "," + " ".join([x[0] for x in top_jobs]) + "\n")
