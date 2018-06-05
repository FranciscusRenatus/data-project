import json
import DataExtract as ext
data = json.loads("""{
  "odata.metadata":"http://opendata.cbs.nl/ODataApi/OData/81975NED/$metadata","value":[
    {
      "name":"TableInfos","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/TableInfos"
    },{
      "name":"UntypedDataSet","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/UntypedDataSet"
    },{
      "name":"TypedDataSet","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet"
    },{
      "name":"DataProperties","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/DataProperties"
    },{
      "name":"CategoryGroups","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/CategoryGroups"
    },{
      "name":"Afzet","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/Afzet"
    },{
      "name":"BedrijfstakkenBranchesSBI2008","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008"
    },{
      "name":"Perioden","url":"http://opendata.cbs.nl/ODataApi/OData/81975NED/Perioden"
    }
  ]
}""")

for n in range(4,8):
    url = data["value"][n]["url"]
    count = ext.requestData(url + "/$count")
    f = open(data["value"][n]["name"] + ".txt","w+")
    top = 1000
    skip = 0
    for i in range(count):
        requesteddata = ext.requestData(url + "?$top=" + str(top) + "&$skip=" + str(skip))
        skip += 1000
        for item in requesteddata["value"]:
            f.write("\n")
            for key in item:
                if key != "Description":
                    f.write(str(key))
                    f.write(": ")
                    f.write(str(item[key]))
                    f.write("\n\n")
    f.close()