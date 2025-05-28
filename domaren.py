
from pypdf import PdfReader
from openai import OpenAI
import re

client = OpenAI()

def get_relevant_text(text_total, topic):
        print("Extracting relevant text from the document using gpt-4o...")
        text_relevant = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {
                "role": "system",
                "content": f"You will be provided with a document written in Swedish. Your task is to extract all text relating to the topic of {topic} as well as the economic and legal viability of {topic}. Return nothing but the relevant text."
            },
            {
                "role": "user",
                "content": text_total
            }
            ],
            temperature=0.2,
            max_tokens=16000,
            top_p=1
            )
        return text_relevant.choices[0].message.content


#function that extracts relevant text from a local txt file
def get_relevant_text_local(file_name):
     print("Extracting relevant text from local document...")
     with open(file_name, "r",encoding="utf-8") as text_file:
        text_relevant = text_file.read()
        return text_relevant
     

topic = "capacity mechanisms, referring specifically to new niche technologies and or markets that have a balancing effect on the grid."

def get_concretization_score(text_relevant, topic): # Define the topic, if this is vague then the model may adapt your topic to the text. For example a text regarding nuclear power can be given high scores for "capacity mechanisms".

    #check if the string length exceeds the maximum allowed length 1048576.
    if len(text_relevant) > 1048576:
        print("Error: The text length exceeds the maximum allowed length 1048576.")
        return "Error: The text length is too great."

    score_format = {
  "type": "json_schema",
  "json_schema": {
    "name": "concretization_score_format",
    "schema": {
      "type": "object",
      "properties": {
        "scores": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "legal viability": { "type": "integer" },
              "economic viability": { "type": "integer" },
              "technical/scientific/expert viability": { "type": "integer" },
              "the road forward": { "type": "integer" },
              "good examples": { "type": "integer" }
            },
            "required": [
              "legal viability",
              "economic viability",
              "technical/scientific/expert viability",
              "the road forward",
              "good examples"
            ],
            "additionalProperties": False
          }
        }
      },
      "required": ["scores"],
      "additionalProperties": False
    },
    "strict": True
  }
}
    print("Deciding on the concretization score...")
    try:
      concretization_score = client.chat.completions.create(
          model="o1",
          messages=[
          {
              "role": "system",
              "content": f"You will be provided with a report document written in Swedish that all in some way regard the topic of {topic}. We now invent the concept of concretization scores in the context of governance and policy. The concretization score of a text represents how concretely the text is advocating for a certain policy, topic or solution. The concretization score will have five dimensions, economic viability, legal viability, technical/scientific/expert viability, the road forward and good examples. Economic viability is scored based on if the text mentions economic factors that favor the topic. Legal viability is scored based on if the text mentions legal factors that favor the topic. Technical/scientific/expert viability is scored based on if the text mentions technical, scientific or expert opinions that favor the topic. The road forward is scored based on if the text mentions steps that can be taken to implement the topic. Good examples is scored based on if the text mentions examples of other times the topic has been implemented. Please provide the 5D concretization scores between 0 and 100 indicating the concretization of {topic} It is important that you do not evaluate any other topic than {topic}. "
          },
          {
              "role": "user",
              "content": text_relevant
          }
          ],
          max_completion_tokens=2500,  
          response_format=score_format
          )
    except:
        concretization_score = client.chat.completions.create(
          model="o1",
          messages=[
          {
              "role": "system",
              "content": f"You will be provided with a report document written in Swedish that all in some way regard the topic of {topic}. We now invent the concept of concretization scores in the context of governance and policy. The concretization score of a text represents how concretely the text is advocating for a certain policy, topic or solution. The concretization score will have five dimensions, economic viability, legal viability, technical/scientific/expert viability, the road forward and good examples. Economic viability is scored based on if the text mentions economic factors that favor the topic. Legal viability is scored based on if the text mentions legal factors that favor the topic. Technical/scientific/expert viability is scored based on if the text mentions technical, scientific or expert opinions that favor the topic. The road forward is scored based on if the text mentions steps that can be taken to implement the topic. Good examples is scored based on if the text mentions examples of other times the topic has been implemented. Please provide the 5D concretization scores between 0 and 100 indicating the concretization of {topic} It is important that you do not evaluate any other topic than {topic}. "
          },
          {
              "role": "user",
              "content": text_relevant[2000:-2000] #cut the text to fit the model
          }
          ],
          max_completion_tokens=2500,  
          response_format=score_format
          )
    return concretization_score.choices[0].message.content

#function that returns text contents of pdf as a string
def read_pdf_to_string(filename):
    print("Reading pdf file...")
    pdf_reader = PdfReader(filename)
    #check if the pdf is not in the folder
    if pdf_reader is None:
        print("Error: The pdf file is not in the folder.")
        return None
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() 
    # Fix broken words (words split across lines)
    text = re.sub(r"(\S+)\s*-\s*\n\s*(\S+)", r"\1\2", text)

    # # Replace newline characters that are not immideatly after a period and a space with a space
    # text = re.sub(r'(?<!\.\s)\n', ' ', text)

    # # Normalize spaces (replace multiple spaces with a single space)
    # text = re.sub(r"\s+", " ", text).strip()

    return text

#function that returns text contents of txt as a string
def read_txt_to_string(file_name):
    print("Reading txt file...")
    with open(file_name, "r") as text_file:
        text = text_file.read()
        return text

#function that gets implementation score of a input document
import os
def get_implementation_score(text):
     #create a dictionary of all documents in the folder C:\Users\simon\OneDrive\Dokument\AAKurserChalmers\Kandidatarbete\OpenAI\DomarenV2\Inputs)
     #loop through all documents in the folder
     score_dict = {}
     for file in os.listdir("Inputs"):
        if file.endswith(".pdf"):
            score_dict[file] = 0

     #check the output text if it contains content of the input documents in the dictionary
     #if the output text contains content of the input document, increase the score of the input document by 1
     #loop through all output documents
     for file in os.listdir("Outputs"):
        print("processing output document: ", file)
        file_text = read_pdf_to_string("Outputs/" + file)
        print("file text: ", file_text)
        for key in score_dict:
            title = key.split(";")[0]
            print(title)
            #check if the any of the output text contains content of the input document
            if title in file_text:
                score_dict[key] += 1
            
     return score_dict

#define a function that takes a string and saves the string as a txt file
def save_string_as_txt_file(string, file_name, folder_name):
    #check if the folder exists, if not create it
    if not os.path.exists(folder_name):
        print(f"Folder {folder_name} does not exist, creating it...")
        os.makedirs(folder_name)
    #save the string as a txt file in the folder
    with open(os.path.join(folder_name, file_name), "w") as text_file:
        print(f"Saving {file_name} in {folder_name}...")
        text_file.write(string)

