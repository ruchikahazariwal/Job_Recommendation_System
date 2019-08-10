# Job recommendation system

## Overview
The personalized recommender system is proposed to solve the problem of information overload and widely applied in many domains. The job recommender systems for job recruiting domain have emerged and enjoyed explosive growth in the last decades. User profiles and recommendation technologies in the job recommender system have gained attention and investigated in academia and implemented for some application cases in industries. I introduce some basic concepts of user profile and some common recommendation technologies based on the existing research

## Dataset
The job descriptions have been scraped from linkedin.com and kaggle 
The data has been scraped by providing various keywords for technologies and title. However, there is some redundant data, rows with missing values etc.
This data has been preprocessed to remove redundancies and missing values to get more reliable output.

## Approaches
* Item based collaborative filtering:
In this algorithm, jobs are represented as two vectors that contain the user IDE and jobs ID. The similarity between user ID and job ID is calculated by the cosine of the angle between the two vectors. Matrix of vectors is generated with rows and columns as User ID and job ID. Number represented in a row is matched to the job ID.
* Jaccard Similarity:
The Jaccard similarity index (sometimes called the Jaccard similarity coefficient) compares members for two sets to see which members are shared and which are distinct. It’s a measure of similarity for the two sets of data, with a range from 0% to 100%. The higher the percentage, the more similar the two populations. Although it’s easy to interpret, it is extremely sensitive to small samples sizes and may give erroneous results, especially with very small samples or data sets with missing observations.

## Repo Structure
```
├── data
|   |── app.tsv
|   |── app1.tsv
|   |── app2.tsv
|   |── jobs.tsv
|   └── user_history.tsv
|
├── result
|   └── contains popular jobs files for each user
|
├── data-scraping
|   ├── has script to scrape the data
|
├── jaccard_adv_popular_jobs.py
|   ├── script to predict popular jobs using jaccard similarity
|
├── collaborative_popular_jobs.py
|   ├── script to predict popular jobs using item based collaborative filtering
|
├── map
|   ├── to find the map value algorthims
|
├── split_script.py
|   ├── to split the data between train and test
|
├── script.sh
|   ├── to run the script
```
## For Output
Please run script.sh or script1.sh

