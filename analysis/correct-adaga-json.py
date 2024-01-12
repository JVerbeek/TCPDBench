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
            print(fp)
        for i, line in enumerate(lines):
            if "{" in line and found < 0:
                found = i
                break
            if line.startswith("PARTITIONING CREATED:"):
                ill_formatted = True
                b = ast.literal_eval(line.strip().split(": ")[1])
                b = [t[1] for t in b]
                break

        if not ill_formatted and found < 0:
            continue
        else:
            lines = lines[i:]

        json_content = str("".join([line.strip() for line in lines]))
        json_content = json_content.replace("null", "\"None\"")
        json_content = json_content.replace("false", "False")
        json_content = json_content.replace("true", "True")
        print(json_content, found)
        json_dict = ast.literal_eval(json_content)

        if "adaga" in file:
            json_dict["result"]["cplocations"] = b
    
        with open(fp, "w") as f: 
            json.dump(json_dict, f)


    