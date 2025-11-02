from shutil import nt

import nt
import pandas as pd


data = [1,2,3,4,5,]
print(data)
series = pd.Series(data)
print(series)



data = {
    'Name' : ['Raju', 'Omkar', 'Ramen Shinde', 'ashish'],
    'Age' : [22 , 22 , 22 , 22],
    'City' : ['Japan' , 'Tollywood', 'Shindevasti' , 'Jai Jagannath']
      }
df = pd.DataFrame(data)
print(df)


print('head \n', df.head()) # first 5 rows by default
print('tail; -2 \n', df.tail(2))

print(df.info())
print('desc \n', df.describe())


# selecting columns

# print(def['Name'])
# print(df[['Name','Age']])
