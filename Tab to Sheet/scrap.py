def getAllKeys(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from getAllKeys(value)
        if type(value) is list:
            for x in value:
                if type(x) is dict:
                    yield (key, x)
                    yield from getAllKeys(x)
                else:
                    yield (key, x)      
        else:
            yield (key, value)

x = {'index': 61, 'voices': [{'beats': [{'type': 4, 'rest': True, 'notes': [{'rest': True}], 'duration': [1, 1]}]}], 'rest': True}
#x = { 'voices' : {'beats': [{'type': 4, 'rest': True, 'notes': [{'rest': True}], 'duration': [1, 1]}]} }

#print(x['beats'][0]['notes'])
#for key, value in getAllKeys(x):
    #print(key,":",value)
#y = getAllKeys(x)

print ( list("asdf") )
