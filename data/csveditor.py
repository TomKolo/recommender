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
#f=pd.read_csv("ratings.csv")
#keep_col = ['userId','songID','timestamp']
#new_f = f[keep_col]
#new_f.to_csv("ratingsWithoutFailedRates.csv", index=False)


f=pd.read_csv("ratingsWithoutFailedRates.csv")
f.insert(2, 'rating', np.random.randint(1,6, f.shape[0]))
print(f)
f.to_csv("song_ratings.csv", index=False)