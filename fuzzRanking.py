import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#download file 'restoran.xlsx'
!gdown --id 1cxn1sYnDR3RRyrs6CyFz9RjfzkR4H5sz

# membaca data pada file restoran.xls ke array resto
rd = pd.read_excel('restoran.xlsx')
restoran = []
stop = len(rd)
for i in range(stop):
  restoran.append([rd['id'][i],rd['pelayanan'][i],rd['makanan'][i]])

#Linear membership fuzzifikasi
#service
def good_serv(x):
  if (x > 90):
    atas = 1
  elif (x <= 70):
    atas = 0
  else:
    atas = (x - 70) / (90 - 70)
  return atas

def avg_serv(x):
  if (x <= 30) or (x > 90):
    tengah = 0
  elif (x > 30) and (x <= 50):
    tengah = (x - 30) / (50 - 30)
  elif (x > 50) and (x <= 70):
    tengah = 1
  else:
    tengah = (90 - x) / (90 - 70)
  return tengah

def bad_serv(x):
  if (x > 50):
    bawah = 0
  elif (x <= 30):
    bawah = 1
  else:
    bawah = (50 - x) / (50 - 30)
  return bawah

#food
def good_food(x):
  if (x > 9):
    atas = 1
  elif (x <= 7):
    atas = 0
  else:
    atas = (x - 7) / (9 - 7)
  return atas

def avg_food(x):
  if (x <= 3) or (x > 9):
    tengah = 0
  elif (x > 3) and (x <= 5):
    tengah = (x - 3) / (5 - 3)
  elif (x > 5) and (x <= 7):
    tengah = 1
  else:
    tengah = (9 - x) / (9 - 7)
  return tengah

def bad_food(x):
  if (x > 5):
    bawah = 0
  elif (x <= 3):
    bawah = 1
  else:
    bawah = (5 - x) / (5 - 3)
  return bawah

# Fuzzification
service = [[good_serv(resto[1]), bad_serv(resto[1]), avg_serv(resto[1])] for resto in restoran]
food = [[good_food(resto[2]), bad_food(resto[2]), avg_food(resto[2])] for resto in restoran]

# Inference
# --- service --- food --- result
# --- bad       --- good    --- rejected
# --- bad       --- avg     --- rejected
# --- bad       --- bad     --- rejected
# --- avg       --- bad     --- rejected
# --- good      --- bad     --- considered
# --- avg       --- avg     --- considered
# --- avg       --- good    --- accepted
# --- good      --- avg     --- accepted
# --- good      --- good    --- accepted

#Inference List
acceptedList = [[max(service[i][2], food[i][1]), max(service[i][1], food[i][2]), max(service[i][1], food[i][1])] for i in range(len(restoran))]
rejectedList = [[max(service[i][0], food[i][1]), max(service[i][0], food[i][2]), max(service[i][0], food[i][0]), max(service[i][2], food[i][0])] for i in range(len(restoran))]
consideredList = [[max(service[i][1], food[i][0]), max(service[i][2], food[i][2])] for i in range(len(restoran))]
inference = [[np.max(acceptedList[i]), np.max(rejectedList[i]), np.max(consideredList[i])] for i in range(len(restoran))]

# Constant Defuzzification
acceptedScore, rejectedScore, consideredScore = 100, 50, 70
worthy = [[restoran[i][0], ((inference[i][1] * acceptedScore) + (inference[i][0] * rejectedScore) + 
                            (inference[i][2] * consideredScore)) / (inference[i][1] + inference[i][0] + inference[i][2])] for i in range(len(inference))]

# Sort based on the highest worthy score
worthy = sorted(worthy, key=lambda x: x[1], reverse=True)

# Insert restoran id to rating
resto_rating = [x[0] for x in worthy[0:10]]
ratingScore = [x[1] for x in worthy[0:10]]

# output to peringkat.xls
restorating = pd.DataFrame({
  'resto id' : resto_rating,
  'rating' : ratingScore
})

restorating.to_excel('peringkat.xlsx')
