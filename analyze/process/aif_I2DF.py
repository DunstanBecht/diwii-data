def process(data):
    if not isinstance(data[1], str):
        data[1] = str(data[1])
    if len(data[1])==1:
        data[1] = "0"+data[1]
    return data
