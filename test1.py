import pandas as pd
import string_source as ss

client_code1 = pd.read_csv('동화약품 배송DB_20221102.csv')

print(client_code1)
print(client_code1['local_code'])
print(client_code1['CUST_NM'])