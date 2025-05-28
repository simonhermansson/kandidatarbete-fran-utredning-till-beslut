# the purpose of this script is to create a batch jsonl file for the SOU texts
# this script will take a direcory of SOU-texts and input them into the jsonl structure
# the jsonl structure is as follows: 
# {"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "o1", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": SOU1}]}}
# {"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "o1", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": SOU2}]}}

import os
folder_path ="DomarenV2/Domaren/test_inputs"  # Path to the folder with .txt files

def make_batch_jsonl(folder_path, prompt, topic, betygs_matris, output_path="DomarenV2/Domaren/batch.jsonl"):
    file_paths = []
    file_names = []
    betygs_matris = betygs_matris.replace("\n", " ")  # Remove newlines for JSON compatibility
    prompt = prompt.replace("\n", " ")  # Remove newlines for JSON compatibility
    topic = topic.replace("\n", " ")  # Remove newlines for JSON compatibility

    # Get all .txt files and save both paths and filenames
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                file_paths.append(file_path)
                file_names.append(filename)  # Save the filename here

    # Create a batch jsonl file
    with open(output_path, "w", encoding="utf-8") as jsonl_file:
        for path, filename in zip(file_paths, file_names):
            with open(path, 'r', encoding="utf-8") as f:
                filename = filename.replace('.txt', '')  # Remove the .txt extension for the custom_id
                text = f.read().replace("\n", " ").replace('"', "'") # Remove newlines and replace " with ' for JSON compatibility
                jsonl_file.write(f'{{"custom_id": "{filename}", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "o1", "messages": [{{"role": "system", "content": "{prompt}"}}, {{"role": "user", "content": "{text}"}}]}}}}\n')
            print(f"Processed {filename}")


betygs_matris = """
[0-33.3 (Bristfälligt) | 33.3-66.6 (Acceptabelt) | 66.6-100 (Genomarbetat)]
**Juridisk genomförbarhet**  
0-33.3: Saknar eller har endast vaga hänvisningar till lagstiftning. Ingen analys av rättsliga hinder eller möjligheter.  
33.3-66.6: Refererar till befintlig lagstiftning men utan djupare diskussion om dess tillämpning i sammanhanget.  
3: Har tydlig juridisk förankring, med analys av hur förslaget passar in i nuvarande rättssystem. Anknyter direkt till relevanta paragrafer, förordningar eller rättspraxis.  

**Ekonomisk genomförbarhet**  
0-33.3: Inga eller mycket generella ekonomiska resonemang. Hänvisar endast till övergripande nyttor.  
33.3-66.6: Beskriver ekonomisk påverkan men utan tydliga beräkningar eller konkreta exempel.  
66.6-100: Ger detaljerade ekonomiska analyser med specifika beräkningar och exempel för olika aktörer.  

**Faktamässigt underlag**  
0-33.3: Saknar eller har endast ytliga referenser till forskning. Resonemang baseras huvudsakligen på antaganden eller allmänna påståenden.  
33.3-66.6: Hänvisar till forskning men utan diskussion om metodik eller aktuellt forskningsläge.  
66.6-100: Bygger på etablerad forskning, redogör för forskningsläge och identifierar kunskapsluckor.  

**Goda exempel**  
0-33.3: Hänvisar vagt till andra länder eller sektorer utan detaljerade jämförelser.  
33.3-66.6: Nämner relevanta exempel men utan analys av hur de kan tillämpas i den aktuella kontexten.  
66.6-100: Ger specifika, jämförbara exempel med analys.  

**Vägen framåt**  
0-33.3: Saknar tydliga mål, tidsramar eller konkreta åtgärder. Ofta hänvisning till fler utredningar.  
33.3-66.6: Har vissa mål och delmål, men de är inte mätbara eller konkret beskrivna.  
66.6-100: Presenterar en tydlig handlingsplan med specifika, mätbara och tidssatta mål samt delmål.  
"""
topic = "'Elnätens och elmarknadernas balansering, flexibilitet, kapacitetsmekanismer samt dess framtida utveckling inom dessa aspekter'"  # Example topic

prompt = f'''
    Du kommer att få ett rapportdokument på svenska som på något sätt behandlar ämnet {topic}.
    Vi introducerar nu begreppet konkretiseringspoäng i kontexten av styrning och policy.
    Konkretiseringspoäng för en text representerar hur konkret texten förespråkar en viss policy, ett ämne eller en lösning
    Konkretiseringspoängen består av fem parametar: juridisk genomförbarhet, ekonomisk genomförbarhet, faktamässigt underlag, vägen framåt samt goda exempel.
    Ekonomisk genomförbarhet bedöms utifrån hur väl texten nämner ekonomiska faktorer som gynnar ämnet.
    Juridisk genomförbarhet bedöms utifrån hur väl texten nämner juridiska faktorer som gynnar ämnet.
    Teknisk/vetenskaplig/expertmässig genomförbarhet bedöms utifrån hur väl texten nämner tekniska, vetenskapliga eller expertutlåtanden som gynnar ämnet.
    Vägen framåt bedöms utifrån hur väl texten nämner steg som kan tas för att implementera ämnet.
    Goda exempel bedöms utifrån hur väl texten nämner exempel på tidigare tillfällen då ämnet har implementerats.

    Dokumentet nedan ska bedömas utifrån de 5 parametrarna: juridik, ekonomi, faktamässigt underlag, goda exempel och vägen framåt.
    För varje parameter görs följande: 
    Hitta först textstycken som berör {topic} och den gällande parametern, 
    betygsätt sedan dessa textstycken för enligt följande instruktioner:
    Betygsskalan är 0-100 och tilldelas efter hur väl texten uppfyller kriterierna i {betygs_matris}. 
    För att räkna ut parameterns betyg skall du beräkna genomsnittet av betygen för de olika textstyckena för den parametern.
    De fem konkretiseringspoängen mellan 0 och 100 ska alltså visa hur konkret ämnet {topic} behandlas i texten.

    Returnera endast ett JSON-objekt med snittbetygen för varje parameter. Svara ENDAST med ett giltigt JSON-objekt enligt följande struktur:
    ['juridisk genomförbarhet': '0-100', 'ekonomisk genomförbarhet': '0-100', 'faktamässigt underlag': '0-100', 'goda exempel': '0-100', 'vägen framåt': '0-100']
    Om du av någon anledning inte kan ge något betyg, vänligen ange 'error' som betyg för den parametern. Du ska enbart svara med JSON-objektet, inget annat.
    '''


folder_path = "DomarenV2/Domaren/relevanta_SOUer_errors1"
# make_batch_jsonl(folder_path, prompt, topic, betygs_matris, "DomarenV2/Domaren/relevant_SOU_batch_errors1.jsonl")

#now we need to upload the jsonl file as a request
from openai import OpenAI
client = OpenAI()


# batch_input_file = client.files.create(
#     file=open("DomarenV2/Domaren/relevant_SOU_batch_errors1.jsonl", "rb"),
#     purpose="batch"
# )
# print("batch uppladdad")

# batch_input_file_id = batch_input_file.id
# print("id:",batch_input_file_id)
# client.batches.create(
#     input_file_id=batch_input_file_id,
#     endpoint="/v1/chat/completions",
#     completion_window="24h",
#     metadata={
#         "description": "Batch 'errors1' för relevanta SOUer, skickas in kl tisdag 15 april kl 14.41"
#     }
# )
# print("batch inskickad")
# bl = client.batches.list(limit=1)
# print("batch list:",bl)
# batch_status = client.batches.retrieve(batch_input_file_id)
# print("batch_status:",batch_status)


# print("output_file_id:",output_file_id)
file_response = client.files.content("file-MbCgA5b7AdJ74L17s6Xrb9") #batch errors1
# print(file_response.text)
with open("DomarenV2/Domaren/resultat_batch_errors1.txt", "w", encoding="utf-8") as f:
    f.write(file_response.text)

# error_file_id='file-Di1KT5BQN35pBJZepEXbzo'
# error_file_response = client.files.content(error_file_id)
# with open("DomarenV2/Domaren/errors_batch_errors1.txt", "w", encoding="utf-8") as f:
#     f.write(error_file_response.text)
# print(error_file_response.text)