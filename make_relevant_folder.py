# #load the file implementation_scores
# with open("SOU_hanteringsprogram/relevanta_souer.csv") as f:
#     lines = f.readlines()
# #remove the first line
# #extract the first column as a list
# SOU_filenames = []
# for line in lines[1:]:
#     #split the line by comma and extract the first column
#     SOU_filenames.append(line.split(";")[0])
# print(SOU_filenames)
# #all these files should be copied into a new folder called "relevanta_SOUer"

import json
#the filenames will be extraced from errors_batch3.txt
#that look like {"id": "batch_req_67fe330d8b5481908f01ae063d9b8e2e", "custom_id": "sou_2003_115", "response": {"status_code": 429, "request_id": "97d81ac7354608175784538d9d367611", "body": {"error": {"message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.", "type": "insufficient_quota", "param": null, "code": "insufficient_quota"}}}, "error": null}

SOU_filenames = []
with open("DomarenV2/Domaren/errors_batch3.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        #extract the filename from the line
        filename = json.loads(line).get("custom_id")
        SOU_filenames.append(filename+".txt")

print(SOU_filenames)
import os
#make the folder
def make_relevant_folder(SOU_filenames):
    os.makedirs("DomarenV2/Domaren/relevanta_SOUer_errors1", exist_ok=True)
    for filename in SOU_filenames:
        #read the file
        with open(f"DomarenV2/Domaren/relevanta_SOUer/{filename}", "r", encoding="utf-8") as f:
            text = f.read()
        #write the file to the new folder
        with open(f"DomarenV2/Domaren/relevanta_SOUer_errors1/{filename}", "w", encoding="utf-8") as f:
            f.write(text)
    
make_relevant_folder(SOU_filenames)