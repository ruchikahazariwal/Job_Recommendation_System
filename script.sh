touch results
rm results
echo "MAP value for simple collaborative algorithm:" >> results
python collaborative_popular_jobs.py; python map.py collaborative_popular_jobs.csv >> results
echo "MAP value for collaborative algorithm(with Jaccard Index, user degree, major, experience)" >> results
python jaccard_adv_popular_jobs.py; python map.py jaccard_adv_popular_jobs.csv >> results
