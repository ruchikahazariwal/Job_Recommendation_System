#!/usr/bin/python
import csv
import re
from collections import defaultdict as ddict

wd = "./" # The directory that the data files are in

def filter(strin):
      remove_spec = lambda(x): x if x.isalnum() else " "
      alpha_strin = "".join(remove_spec(word) for word in strin.strip())
      alpha_strin = re.sub(' +', ' ', alpha_strin)
      all_words = [word.lower()[0:4] for word in alpha_strin.split(" ") if len(word) > 3]
      #filtered_words = [re.sub('[aeiou]', '', word) for word in all_words]
      return all_words

def word_similarity(word1, word2):
   if word1 == word2:
   	  return 1
   else:
      return 0
   	  
def list_of_words_similarity(list1, list2):
   if (len(list1) == 0 or len(list2) == 0): return 0.0
   total_similarity = 0.0
   for word1 in list1:
      for word2 in list2:
         total_similarity += word_similarity(word1, word2)
   return total_similarity/(len(list1)*len(list2))

print "Recording user histories..."
user_history_map = ddict(list)
with open(wd + "user_history.tsv", "r") as history_file:
   reader = csv.reader(history_file, delimiter="\t",
   quoting=csv.QUOTE_NONE, quotechar="")
   reader.next()
   previous_id = 0
   for line in reader:
      (UserID, WindowID, Split, Sequence, JobTitle) = line
      title_words = filter(JobTitle)
      if not user_history_map.has_key(UserID): 
         user_history_map[UserID] = title_words
      else:
         user_history_map[UserID] = user_history_map[UserID] + title_words


job_title_map = ddict(list)
user_ke_jobs = ddict(list)
job_ke_users = ddict(list)
user_ke_predicted_jobs_lvl1 = ddict(lambda: ddict(list))
user_ke_predicted_jobs = ddict(lambda: ddict(list))
print "Recording job data..."
job_info = {}
with open(wd + "jobs.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() # burn the header
    for line in reader:
        (Jobid, WindowId, Title, Description, Requirements, City, State, 
        Country, Zip5, StartDate, EndDate) = line
        job_info[str(Jobid)] = [int(WindowId), State, City, 0]
        title_words = filter(Title)
        job_title_map[Jobid] = title_words

print "Counting applications..."
with open(wd + "apps1.tsv") as infile:
    reader = csv.reader(infile, delimiter="\t")
    reader.next() # burn the header
    for line in reader:
        (UserId, WindowID, Split, ApplicationDate, JobId) = line
        if WindowID == 2: break
        user_ke_jobs[UserId].append(JobId)
        job_ke_users[JobId].append(UserId)

user_degrees = ddict()
user_majors = ddict()
user_experience = ddict()
print "Recording user data..."
with open(wd + "users.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() # burn the header
    for line in reader:
        (UserId, WindowId, Split, City, State, Country, ZipCode,
        DegreeType, Major, GraduationDate, WorkHistoryCount,
        TotalYearsExperience, CurrentlyEmployed, ManagedOthers,
        ManagedHowMany) = line
        user_degrees[UserId] = DegreeType
        user_majors[UserId] = Major
        user_experience[UserId] = TotalYearsExperience

print "Finding similar jobs..."
with open(wd + "users.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() # burn the header
    for line in reader:
        (UserId, WindowId, Split, City, State, Country, ZipCode,
        DegreeType, Major, GraduationDate, WorkHistoryCount,
        TotalYearsExperience, CurrentlyEmployed, ManagedOthers,
        ManagedHowMany) = line
        if Split == "Train":
            continue
        for job_id in user_ke_jobs[UserId]:
           for user_id1 in job_ke_users[job_id]:
              union_size = len(set(user_ke_jobs[UserId] + user_ke_jobs[user_id1]))
              for job_id1 in user_ke_jobs[user_id1]:
                 if job_id1 in user_ke_jobs[UserId]: break
                 score = 1.0
                 if (user_degrees[UserId] != 'None' and user_degrees[UserId] == user_degrees[user_id1]): score *= 1.1
                 if (user_majors[UserId] != 'None' and user_majors[UserId] == user_majors[user_id1]): score *= 1.1
                 if user_experience[UserId].isdigit() and user_experience[user_id1].isdigit(): score *= 1 + 5/(10+abs(int(user_experience[UserId]) - int(user_experience[user_id1])))
                 if user_ke_predicted_jobs[UserId].has_key(job_id1):
                    user_ke_predicted_jobs[UserId][job_id1] += score/union_size
                 else:
                    user_ke_predicted_jobs[UserId][job_id1] = score/union_size

print "Text similarity..."
for user_id in user_ke_predicted_jobs:
   for job_id in user_ke_predicted_jobs[user_id]:
      user_ke_predicted_jobs[user_id][job_id] = user_ke_predicted_jobs[user_id][job_id]*(0.1+list_of_words_similarity(user_history_map[user_id], job_title_map[job_id]))

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
with open(wd + "users.tsv", "r") as infile:
    reader = csv.reader(infile, delimiter="\t", 
    quoting=csv.QUOTE_NONE, quotechar="")
    reader.next() # burn the header
    with open("popular_jobs20.csv", "w") as outfile:
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
