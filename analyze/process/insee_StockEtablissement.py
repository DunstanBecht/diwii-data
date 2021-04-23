def process(data):
    if len(data)!=48:
        print("Correction: data of length "+str(len(data)))
        old_data, data = data, []
        open=False
        for value in old_data:
            if isinstance(value, str) and len(value)>0 and open:
                data[-1] = data[-1]+value
                if value[-1]=='"':
                    open = False
            else:
                data.append(value)
                if isinstance(value, str) and len(value)>0 and value[0]=='"':
                    open = True
    for i in [6, 10, 12, 26]: # INT
        try:
            int(data[i])
        except:
            data[i] = None
    for i in [4, 8, 39]: # DATE
        if data[i]=='':
            data[i]=None
    return data
