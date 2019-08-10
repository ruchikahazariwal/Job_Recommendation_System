from collections import defaultdict as ddict

ratio = 0.65
with open("apps.tsv") as infile:
   with open("apps1.tsv", "w") as outfile1:
      with open("apps2.tsv", "w") as outfile2:
         check = True
         first_line = infile.readline()
         outfile1.write(first_line)
         outfile2.write(first_line)
         previous_line = infile.readline()
         (UserId, WindowID, Split, ApplicationDate, JobId) = previous_line.strip().split('\t')
         while True:
              this_user_lines = []
              previous_id = UserId
              check = False
              for line1 in infile:
                 this_user_lines.append((UserId, WindowID, Split, ApplicationDate, JobId))
                 previous_line = line1
                 this_split = Split
                 (UserId, WindowID, Split, ApplicationDate, JobId) = previous_line.strip().split('\t')
                 if UserId != previous_id:
                    check = True
                    length = len(this_user_lines)
                    for i in range(int(ratio*length)+1):
                       outfile1.write("\t".join(this_user_lines[i])+"\n")
                    if this_split == 'Train':
                       for i in range(int(ratio*length)+1, length):
                          outfile1.write("\t".join(this_user_lines[i])+"\n")
                    else:
                       for i in range(int(ratio*length)+1, length):
                          outfile2.write("\t".join(this_user_lines[i])+"\n")
                    break
              if not check:
                 this_user_lines.append((UserId, WindowID, Split, ApplicationDate, JobId))
                 length = len(this_user_lines)
                 for i in range(int(ratio*length)+1):
                    outfile1.write("\t".join(this_user_lines[i])+"\n")
                 if this_split == 'Train':
                    for i in range(int(ratio*length)+1, length):
                       outfile1.write("\t".join(this_user_lines[i])+"\n")
                 else:
                    for i in range(int(ratio*length)+1, length):
                       outfile2.write("\t".join(this_user_lines[i])+"\n")
                 break
