import json

data = r"""{
   "type":"output",
   "name":"exported.csv",
   "target":"HDFS",
   "input":[
      {
         "type":"filter",
         "condition":"gender = \"m\"",
         "input":[
            {
               "type":"join",
               "input":[
                  {
                     "column":"employee_id",
                     "input":[
                        {
                           "type":"source",
                           "id":"ABCDE"
                        }
                     ]
                  },
                  {
                     "column":"id",
                     "input":[
                        {
                           "type":"source",
                           "id":"def"
                        }
                     ]
                  }
               ]
            }
         ]
      }
   ]
}"""



def process_input(data):
    """ input will be a json, return a datamart"""
    if "type" in data.keys() and data['type'] == 'join':
        df1 = process_input(data['input'][0]['input'][0])
        df2 = process_input(data['input'][1]['input'][0])
        print (df1)
        print (df2)
        return "join 2 tables with coloums:  " + data['input'][0]['column'] + '   and   ' + data['input'][1]['column']


    if "type" in data.keys() and data['type'] == 'filter':
        df1 = process_input(data['input'][0])
        print (df1)
        return "filter applied: " + data['condition']

    if "type" in data.keys() and data['type'] == 'source':
        return 'data source:' + data['id']

    # if "type" in data.keys() and data['type'] == 'source':
    #     print (data['type'] + ': ' + data['id'])
    #     return
    # elif "type" in data.keys():
    #     print("operation:" + data['type'])

    print (process_input(data['input'][0]))



data = json.loads(data)
process_input(data)



