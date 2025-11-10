import pandas as pd

# giving path
customers =  pd.read_csv("../data resources/customers.csv") # add double dot file reading . means current folder and .. means im currently in this folder go to the parent
products = pd.read_csv("../data resources/products.csv")
orders = pd.read_csv("../data resources/orders.csv")

# print the head and the data
print('Customers: \n ',customers.head()) #.head displaye on top 5 rows
print('Products: \n',products.head())
print('Orders: \n',orders.head())

# Step 3 transform (T)


# clean customer names and cities

customers['name'] = customers['name'].str.title()
customers['city'] = customers['city'].str.title()
customers['join_date'] = pd.to_datetime(customers['join_date'])

#Ensrue order date is a valid date
orders['orders_date'] = pd.to_datetime(orders['order_date'])

# add derived columns
orders['avg_price_per_items'] = orders['total_amount'] / orders['quantity']

# join orders with products to include category this is a left join
orders = orders.merge(products[['product_id','category']], on=
                      'product_id', how='left')
print('Customers: \n',customers.head())


#load it in schema
# we need to install the lib in this pycharm
# pip install google-cloud-bigquery

# load into bigquery

# then connect and load

from google.cloud import bigquery # it is a module

client = bigquery.Client(project='my-project-rev-4155')


#  default credentials error after uploading all of this into bigquery authentication error



customer_table = "my-project-rev-4155.ecommerce_data.customers"
product_table = "my-project-rev-4155.ecommerce_data.products"
order_table = "my-project-rev-4155.ecommerce_data.orders"


# Load dataframes into bigquery

client.load_table_from_dataframe(customers, customer_table).result()
client.load_table_from_dataframe(products, product_table).result()
client.load_table_from_dataframe(orders,order_table).result()


print("Data Loaded Successfully into BigQuery!")


# insetitnf data into bigquery dimension table first and fact table which will have the primary key first
# the key u have finally add this file