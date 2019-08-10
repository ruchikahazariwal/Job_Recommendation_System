touch results
rm results
echo "MAP value for simple collaborative algorithm:" >> results
python collaborative_popular_jobs.py; python map.py popular_jobs.csv >> results