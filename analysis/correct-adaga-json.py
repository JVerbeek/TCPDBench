import json
import ast 
import os
import glob
import pathlib

for dataset in os.listdir("abed_results"):
    file = glob.glob(f"abed_results/{dataset}/default*/*.json")
    for filename in file:
        fp = pathlib.Path(filename)
        found = -1
        ill_formatted = False
        with open(fp) as f:   # open JSON as textfile
            lines = f.readlines()
            if "adaga" in filename: 
                json_dict = json.loads("".join(lines))
                if type(json_dict["result"]["cplocations"][0]) == list:
                    json_dict["result"]["cplocations"] = [seg[0] for seg in json_dict["result"]["cplocations"]]
                    with open(fp, "w") as f: 
                        json.dump(json_dict, f)
                        continue
        for i, line in enumerate(lines):
            if "{" in line and found < 0:
                found = i
                break
            if line.startswith("PARTITIONING CREATED:"):
                ill_formatted = True

        if False == ill_formatted or found < 0:
            continue
        else:
            print(ill_formatted, found)
            lines = lines[i:]
            json_content = str("".join([line.strip() for line in lines]))
            json_content = json_content.replace("null", "\"None\"")
            json_content = json_content.replace("false", "False")
            json_content = json_content.replace("true", "True")
            json_dict = ast.literal_eval(json_content)
            
            with open(fp, "w") as f: 
                json.dump(json_dict, f)

    