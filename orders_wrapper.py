#some comment
import urllib
from urllib import request
from decouple import config

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')

api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/graphql.json"
headers = {}
headers["Content-Type"] = "application/graphql"
headers["X-Shopify-Access-Token"] = access_token

data = b"""
{
    orders(first: 5) {
      edges {
        node {
          id
          email 
        }
      }
      pageInfo {
        hasNextPage
      }
    }
}
"""

req = request.Request(api_url, data=data, headers=headers, method="POST")

response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
