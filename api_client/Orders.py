from .HelperFunctions import getQuery, getJSONData

QUERY = """
{
    orders(first: 5 {query} {cursor}) {
        edges {
            cursor
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
                    displayName
                }
            }
        }
        pageInfo {
            hasNextPage
        }
    }
}
"""

def parseOrderNode(node):
    output_node = {}
    output_node['order_id'] = node['node']['id']
    output_node['total_price'] = node['node']['totalPriceSet']['shopMoney']['amount']+" "+node['node']['totalPriceSet']['shopMoney']['currencyCode']
    output_node['name'] = node['node']['name']
    output_node['fulfillment_status'] = node['node']['displayFulfillmentStatus']
    output_node['cursor'] = node['cursor']
    if node['node']['customer']:
        output_node['customer_name'] = node['node']['customer']['displayName']
    else:
        output_node['customer_name'] = None

    return output_node

def getOrdersList(data):
    output_list = []
    edges = data['data']['orders']['edges']

    for node in edges:
        output_list.append(parseOrderNode(node))

    return output_list

def getOrders(query, output, min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None):
    query_data = getQuery(query, min_processed_at, max_processed_at, fulfillment_status, cursor)
    data = getJSONData(query_data)

    if "errors" in data:
        return data

    page_info = data['data']['orders']['pageInfo']

    orders_list = getOrdersList(data)
    output += orders_list

    if page_info['hasNextPage']:
        getOrders(query,
                output, 
                min_processed_at=min_processed_at, 
                max_processed_at=max_processed_at, 
                fulfillment_status=fulfillment_status, 
                cursor=orders_list[-1]['cursor'] 
                )

    return output

def Orders(min_processed_at=None, max_processed_at=None, fulfillment_status=None):
    """
    Returns a list of dictonary items where each item is an Order listing with required fields
    Orders( min_processed_at, max_processed_at, fulfillment_status )
    min_processed_at ( Get all orders after this date, here the value must be a valid python Datetime() instance )
    max_processed_at ( Get all orders before this date, here the value must be a valid python Datetime() instance )
    fulfillment_status ( can have following values ['shipped','partial','unshipped','any'] passed as strings)
    """
    global QUERY
    output = getOrders( QUERY, [], min_processed_at=min_processed_at, max_processed_at=max_processed_at, fulfillment_status=fulfillment_status)
    
    return output 
