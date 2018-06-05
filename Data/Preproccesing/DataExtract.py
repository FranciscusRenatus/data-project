import urllib.request, json 

def requestData(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        return data

print(requestData("http://opendata.cbs.nl/ODataApi/OData/81975NED/UntypedDataSet"))