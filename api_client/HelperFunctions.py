def getQuery(query, min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None):
    temp_query_var = query 
    data = query_string = query_wrapper = params = cursor_wrapper = ""
    if min_processed_at or max_processed_at or fulfillment_status:
        query_wrapper+= "query: \"{}\""

    if cursor:
        cursor_wrapper = ", after:"+cursor
        temp_query_var = temp_query_var.replace("{cursor}",cursor_wrapper)
    else:
        temp_query_var = temp_query_var.replace("{cursor}","")

    if min_processed_at:
        params += "processed_at:>"+min_processed_at.strftime("%Y-%m-%dT%H-%M-%SZ")+" "

    if max_processed_at:
        params += "processed_at:<"+max_processed_at.strftime("%Y-%m-%dT%H-%M-%SZ")+" "

    if fulfillment_status:
        params += "fulfillment_status:"+fulfillment_status

    if params != "":
        query_string = query_wrapper.format(params)

    if query_string != "":
        query_string = ", "+query_string
        temp_query_var = temp_query_var.replace("{query}",query_string)
    else:
        temp_query_var = temp_query_var.replace("{query}","")

    return temp_query_var.encode('utf-8')
