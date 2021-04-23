def process(data):
    for i in [9]: # INT
        try:
            data[i] = int(data[i].replace('-', ''))
        except:
            data[i] = None
    return data
