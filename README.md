# Twitter_Geoprocessing
This is an assignment for Cluster and Cloud Computing.
In this project, an parallelised application is designed leveraging SPARTON (the University of Melbourne HPC facility）to analyse tweets based on their geographic locations. This application allow a given number of nodes and cores to be utilized. In the report, the running time under:  
• 1 node and 1 core;  
• 1 node and 8 cores;  
• 2 nodes and 8 cores (with 4 cores per node).  is compared.
## Files description 
The *melbGrid.json* file contains the id and coordinates information of sixteen grids of Melbourne.  
The *bigTwitter.json*(tinyTwitter.json) file contains a large number of tweets and relevant information such as the coordinates of each tweet, the tweet texts and so on.
## Goals
This assignment is to search the large Twitter data set (bigTwitter.json) to identify Twitter activity around Melbourne and the most frequently used hashtags in each of the grid cells (A1...D5). Specifically,

• Order (rank) the Grid boxes based on the total number of Twitter posts made in each box and return the total count of posts in each box, e.g.  
o C3: 23,456 posts,   
o B2: 22,345 posts,   
o D1: 21,234 posts,   
o...  
o Down to the square with the least number of posts;  

• Order (rank) the top 5 hashtags in each Grid cells based on the number of occurrences of those hashtags, e.g.   
o C3: ((#maccas, 123),(#qanda, 121),(#trump,100),(#unimelb,66),(#dominos,41))  
o B2: ((#maccas, 82),(#vicroads,81), etc etc....)  
o...  
o Down to the top 5 hashtags in the grid cell with the least number of posts;  
  
