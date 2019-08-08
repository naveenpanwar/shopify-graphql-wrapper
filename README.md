## Dependencies
1. Python 3
2. **Python Decouple** ( python-decouple ), you can install it with `pip install python-decouple`

## Getting Started
1. Install the Dependency(s) as mentioned in the list
2. Clone the repository `git clone git@github.com:naveenpanwar/shopify-graphql-wrapper.git`
3. Create a **Private App** in your Shopify store and give it permissions to read Orders and other required fileds.
4. Copy the **Password** field.
5. Create a `.env` or `.ini` in the project root and enter the values of `SHOP_ADDRESS=<your_shop_subdomain> ACCESS_TOKEN=<copied_password>` here is a link to a [python-decouple guide](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html).
6. `cd` into root of cloned directory.
7. You can use it like so.
```python
>>> from api_client.Orders import Orders
>>> orders = Orders()
>>> orders
```

## Function Specifications
`Orders( min_processed_at, max_processed_at, fulfillment_status )`

Returns a list of dictonary items where each item is an Order listing with required fields
min_processed_at ( Get all orders after this date, here the value must be a valid python Datetime() instance )
max_processed_at ( Get all orders before this date, here the value must be a valid python Datetime() instance )
fulfillment_status ( can have following values ['shipped','partial','unshipped','any'] passed as strings)
```python
>>> from api_client.Orders import Orders
>>> orders = Orders()
>>> orders
```
    
`PaymentDetails( order_id ) where order_id is the unique_id of an order`
Returns a list of dictonary items where each item is a PaymentDetail from an order with required fields
```python
>>> from api_client.PaymentDetails import PaymentDetails
>>> payment_details = PaymentDetails(<some_order_id>)
>>> payment_details 
```
    
`LineItems( order_id ) where order_id is the unique_id of an order`
Returns a list of dictonary items where each item is an LineItem from an order with required fields
```python
>>> from api_client.LineItems import LineItems
>>> items = LineItems(<some_order_id>)
>>> items 
```
