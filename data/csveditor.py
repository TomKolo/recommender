import csv
import pandas as pd
import random
import numpy as np

# \/ \/ \/ \/ EDITING DATA IN DATASET TO RATING MODE \/ \/ \/ \/
#  This file can be deleted LATER

#with open("official_song_dataset.csv", "rt", encoding='utf-8') as input, open('temp.csv', 'wt', encoding='utf-8') as output:
 #   reader = csv.reader(input, delimiter = ',')
 #   writer = csv.writer(output, delimiter = ',')

 #   all = []
 #   row = next(reader)
 #   row.insert(0, 'songID')
   # all.append(row)
   # for k, row in enumerate(reader):
  #      all.append([str(k+1)] + row)
   # writer.writerows(all)




#import pandas as pd
#f=pd.read_csv("songs_ratings.csv")
#keep_col = ['userId','song_id']
#new_f = f[keep_col]
#new_f.to_csv("xd2.csv", index=False)


stary = pd.read_csv("song_dataset.csv")
nowy = pd.read_csv("songs_ratings.csv")

#with open("song_dataset.csv", "r") as f:
 #   reader = csv.reader(f)
  #  for line_num, content in enumerate(reader):
   #     for ind in nowy.index:
    #        if content[1] == nowy['song_id'][ind]:
     #           print(content, line_num + 1)

#thiss = 1
#for ind in nowy.index:
    #for ind2 in stary.index:
        #if nowy['song_id'][ind] == stary['song_id'][ind2]:
            #xd = stary.at[ind2, 'songId']
            #nowy.at[ind, 'songId'] = xd
            #print(nowy['songId'][ind])
            
#nowy.to_csv("xd2.csv", index=False)



#f=pd.read_csv("xd2.csv")
#f.insert(2, 'rating', np.random.randint(1,6, f.shape[0]))
#f.to_csv("songs_ratings.csv", index=False)

nowy = nowy.iloc[:280000]
nowy.to_csv("xd2.csv", index=False)