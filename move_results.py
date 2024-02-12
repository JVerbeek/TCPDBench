import os
import json
import shutil

for i, file in enumerate(os.listdir("stagedir/0")):
    print(file)
    with open("stagedir/0/"+file, "r") as f:
        content = json.load(f)
        dest = content["dataset"]
        shutil.move("stagedir/0/"+file, f"abed_results/{dest}/{file}")
print(f"Done, moved {i} files")
