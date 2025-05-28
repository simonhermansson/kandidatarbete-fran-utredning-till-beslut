
import os

import json


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
    Vänligen ange de fem konkretiseringspoängen (5D) mellan 0 och 100 som visar hur konkret ämnet {topic} behandlas i texten.
    Det är viktigt att du inte utvärderar något annat ämne än {topic}.

    Dokumentet nedan ska bedömas utifrån de 5 parametrarna: juridik, ekonomi, faktamässigt underlag, goda exempel och vägen framåt.
    För varje parameter görs följande: 
    Hitta först relevanta textstycken som berör parametern, 
    betygsätt sedan de relevanta textstyckena enligt följande instruktioner:
    Betygsskalan är 0-100 och tilldelas efter hur väl texten uppfyller kriterierna i {betygs_matris}. 
    För att räkna ut vad parameterns betyg blir tar du genomsnittet av betygen för de olika textstyckena.
    Returnera endast ett JSON-objekt med snittbetygen för varje parameter. Svara ENDAST med ett giltigt JSON-objekt enligt följande struktur:
    ['juridisk genomförbarhet': '0-100', 'ekonomisk genomförbarhet': '0-100', 'faktamässigt underlag': '0-100', 'goda exempel': '0-100', 'vägen framåt': '0-100']
    '''

import tiktoken
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("o1")
    tokens = encoding.encode(text)
    return len(tokens)

def control_length(path):
    filename = os.path.basename(path)
    # print(f"Processing file: {path}")
    with open(path, 'r', encoding='utf-8') as file:
        sou_file_text = file.read()
        text = prompt + sou_file_text
        
        tokens = count_tokens(text) # Count the tokens in the text using tiktoken
        filename_short = filename.replace('.txt', '')  # Remove the .txt extension for the custom_id
        print((filename_short,tokens))
        if tokens > 195000:
            print(f"FILE {filename} HAS {tokens} TOKENS, which exceeds the limit of 195000.")
            # int_ratio = int(tokens // 190000)
            # #the text should be split into int_ratio+1 files to reduce tokens to 195000 or less
            # split_text = sou_file_text.split()
            # split_length = len(split_text) // (int_ratio + 1)
            # for i in range(int_ratio + 1):
            #     start = i * split_length
            #     end = (i + 1) * split_length if i < int_ratio else len(split_text)
            #     new_text = ' '.join(split_text[start:end])
            #     with open(f"DomarenV2/Domaren/relevanta_SOUer/{filename_short}_split{i}.txt", 'w', encoding='utf-8') as new_file:
            #         new_file.write(new_text)
            file.close()
            # #the old file should be moved to a new folder called large_files
            # os.makedirs("DomarenV2/Domaren/large_files", exist_ok=True)
            # os.rename(path, f"DomarenV2/Domaren/large_files/{filename}")
                
folder = "DomarenV2/Domaren/relevanta_SOUer" 
for filename in os.listdir(folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder, filename)
        control_length(file_path)
