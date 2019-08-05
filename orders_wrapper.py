#some comment
import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')

api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/graphql.json"
headers = {}
headers["Content-Type"] = "application/graphql"
headers["X-Shopify-Access-Token"] = access_token

query = """
{
    orders(first: 5 {query}) {
        edges {
            node {
                id
                processedAt
                totalPriceSet {
                    shopMoney {
                        currencyCode
                        amount
                    }
                }
                name
                displayFulfillmentStatus
                customer {
                    firstName
                    lastName
                }
            }
        }
        pageInfo {
            hasNextPage
        }
    }
}
"""

def Orders(min_processed_at=None, max_processed_at=None, fulfillment_status=None):
    global query
    data = qu = q = d = ""
    if min_processed_at or max_processed_at or fulfillment_status:
        q+= "query: \"{}\""

    if min_processed_at:
        d += "processed_at:>"+min_processed_at.strftime("%Y-%m-%dT%H-%M-%SZ")+" "

    if max_processed_at:
        d += "processed_at:<"+max_processed_at.strftime("%Y-%m-%dT%H-%M-%SZ")+" "

    if fulfillment_status:
        d += "fulfillment_status="+fulfillment_status

    if d != "":
        qu = q.format(d)

    if qu != "":
        qu = ", "+qu
        data = query.replace("{query}",qu)
    else:
        data = query.replace("{query}","")

    data = data.encode('utf-8')
    req = request.Request(api_url, data=data, headers=headers, method="POST")

    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))

now = datetime.now()
time.sleep(2)
now2 = datetime.now()
Orders(min_processed_at=now,max_processed_at=now2,fulfillment_status="pending")
Orders(min_processed_at=now)
Orders(max_processed_at=now2)
Orders(fulfillment_status="pending")
Orders()
