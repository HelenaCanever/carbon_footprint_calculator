 
import json

with open('report_template.json') as json_file:
    report = json.load(json_file)

for i in report["transportation"]:
    if report["transportation"][i]["emissions"]!=0:
        print(report["transportation"][i]["fr_name"])
        print(report["transportation"][i]["monthly"])
        if report["transportation"][i]["monthly"]:
            print("Trips:")
            print(str(report["transportation"][i]["trips"])+ " per month")
            print("Distance:")
            print(str(report["transportation"][i]["kms"]*report["transportation"][i]["trips"])+ " kilometers per month")
            print(str(report["transportation"][i]["kms"]*report["transportation"][i]["trips"]*report["duration"])+ " kilometers in total")

        else:
            print("Trips:")
            print(str(report["transportation"][i]["trips"])+ " in total" )
            print("Distance:")
            print(str(report["transportation"][i]["kms"]*report["transportation"][i]["trips"])+ " kilometers in total")



            
            
        