import re
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


import json

with open('data.json', 'r') as f:
    data = json.load(f)

# crime category dicts
excise = data.get("Excise", {})
gambling = data.get("Gambling", {})
cow_related = data.get("Cow_related", {})
drug_related_illegal_items = data.get("Drug_related_illegal_items", {})
offence_related_to_religion = data.get("Offence_related_to_Religion", {})
offence_related_to_currency_note = data.get("Offence_related_to_currency_note", {})
offence_against_state = data.get("Offence_against_state", {})
digital_offences = data.get("Digital_offences", {})
property_offences = data.get("Property_offences", {})
body_related_crime = data.get("Body_related_crime", {})
natural_disaster = data.get("Natural_disaster", {})
offence_related_to_election = data.get("Offence_related_to_election", {})
law_and_order = data.get("Law_and_order", {})
computer = data.get("Computer", {})
other = data.get("Other", {})

# Merge all into one flat dict
all_crime_types = {}
all_crime_types.update(excise)
all_crime_types.update(gambling)
all_crime_types.update(cow_related)
all_crime_types.update(drug_related_illegal_items)
all_crime_types.update(offence_related_to_religion)
all_crime_types.update(offence_related_to_currency_note)
all_crime_types.update(offence_against_state)
all_crime_types.update(digital_offences)
all_crime_types.update(property_offences)
all_crime_types.update(body_related_crime)
all_crime_types.update(other)
all_crime_types.update(natural_disaster)
all_crime_types.update(offence_related_to_election)
all_crime_types.update(law_and_order)
all_crime_types.update(computer)

# other dicts / lists
chhattisgarh_districts = data.get("chhattisgarh_districts", [])
ambikapur_police_stations = data.get("ambikapur_police_stations", [])
weapons_keywords = data.get("weapons_keywords", [])
score_match = data.get("score_match", [])
occasion = data.get("occasion", {})
accused_patterns = data.get("accused_patterns", [])
complainant_pattern = data.get("complainant_pattern", [])

#Police crimes
police_crime_types_input = data.get("police_crime_types_input", [])
police_crime_examples = data.get("police_crime_examples", [])
additional_police_crimes = data.get("additional_police_crimes", [])
summarized_police_crimes = data.get("summarized_police_crimes", [])
alternative_police_crimes = data.get("alternative_police_crimes", [])

# Combine all lists and remove duplicates
crimes_by_police = list(set(
    police_crime_types_input +
    police_crime_examples +
    additional_police_crimes +
    summarized_police_crimes +
    alternative_police_crimes
))

# Optional: Sort the list alphabetically
crimes_by_police.sort()
# print(crimes_by_police)


import re
import stanza


# nlp = stanza.Pipeline('hi', processors='tokenize,ner',download_method=None)

import stanza
stanza.download('hi', dir='./stanza_models')
nlp = stanza.Pipeline('hi', processors='tokenize,ner', dir='./stanza_models')


def extract_date(text):
    # Convert Hindi digits to Western numerals
    hindi_to_num = str.maketrans("०१२३४५६७८९", "0123456789")
    text = text.translate(hindi_to_num)

    # Match common date formats: dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy, dd/mm/yy etc.
    match = re.search(r'\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b', text)
    return match.group() if match else "N/A"

def extract_district(text):
    for district in chhattisgarh_districts:
        if district in text:
            return district
    return "N/A"
    
def extract_police_station(text):
    # for ps in ambikapur_police_stations:
    #     if ps in text:
    #         return ps
    # return "N/A"    
    
    # Try both 'थाना' and 'चौकी'
    match = re.search(r'(थाना|चौकी)\s+([^\n।:,]*)', text)
    return f'{match.group(1)} {match.group(2).strip()}' if match else "N/A"

def extract_fir_number(text):
    match = re.search(r'(अपराध क्रमांक|FIR|एफआईआर)\s*[:\-]?\s*([0-9\/\-]+)', text)
    return match.group(2) if match else "N/A"

def extract_complainant(text):
    patterns = [
    fr"{word}\s*[:-]?\s*([\w\u0900-\u097F\s]+)"
    for word in complainant_pattern
    ]  
    out=[]
    for pattern in patterns:
        all_matches = []
        match1 = re.findall(pattern, text)
        all_matches.extend([m.strip() for m in match1])
        # print("Match found:", all_matches,len(all_matches))
        for match in all_matches:
            matched_text = match.strip()
            words = re.findall(r'[\w\u0900-\u097F]+', matched_text)
            limited_words = words[:10]      # 10 words after that 
            name = ' '.join(limited_words)
            doc = nlp(name)
                # for ent in doc.ents:
                #     print(f"Text: {ent.text}, Type: {ent.type}")
            persons = [ent.text for ent in doc.ents if ent.type == 'NEP']
            if persons:
                out.extend(persons)
    if out:
        return ', '.join(out)
    else :
        return "N/A"

def extract_accused(text):  
    patterns = [
    fr"{word}\s*[:-]?\s*([\w\u0900-\u097F\s]+)"
    for word in accused_patterns
    ]  
    out = []
    for pattern in patterns:
            all_matches = []
            match1 = re.findall(pattern, text)
            all_matches.extend([m.strip() for m in match1])
            # print("match : "    , all_matches,len(all_matches))
            for match in all_matches:
                # print(match,text.index(match))
                matched_text = text[text.index(match):text.index(match)+150] 
                matched_text = matched_text.split("।")[0].strip()
                # print("matched_text : ", matched_text)
                matched_text = re.split(r'पिता|पुत्र|पति|Father|Son|Husband', matched_text)[0].strip()
                # Extract words (Hindi, Latin letters, digits)
                words = re.findall(r'[\w\u0900-\u097F]+', matched_text)
                # print("words : ", words)
                # limited_words =   words[:20]
                # print("limited_words : ", limited_words)
                name = ' '.join(words)
                doc = nlp(name)
                # for ent in doc.ents:
                #     print(f"Text: {ent.text}, Type: {ent.type}")
                persons = [ent.text for ent in doc.ents if ent.type == 'NEP']
                if persons:
                    out.extend(persons)
    if out:
        return ', '.join(out)
    else :
        return "N/A"
   
def extract_weapons(text):
    weapons_keyword = weapons_keywords
    found = [word for word in weapons_keyword if word in text]
    return ', '.join(found) if found else "N/A"

def extract_crime_type(text):
    for crime in all_crime_types:
        if crime in text:
            return crime
    return "N/A" 

def extract_score(text):
    score=0
    accused = extract_accused(text)
    score += len(accused.split(', ')) if accused != "N/A" else 0
    
    for i in score_match:
        if i in text:
            score += 1
    
    for i in occasion.keys():
        if i in text:
            score += occasion[i]
               
    word_to_number = {
            "शून्य": 0, "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पांच": 5,
            "छह": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10, "ग्यारह": 11,
            "बारह": 12, "तेरह": 13, "चौदह": 14, "पंद्रह": 15, "सोलह": 16,
            "सत्रह": 17, "अठारह": 18, "उन्नीस": 19, "बीस": 20
        }

    def convert_hindi_numerals(s):
        return s.translate(str.maketrans('०१२३४५६७८९', '0123456789'))

    def extract_number_from_words(w):
        return word_to_number.get(w.strip(), 0)

    crime = extract_crime_type(text)
    if crime in all_crime_types:
        score += all_crime_types[crime]
      
        crime_lst = (
                list(property_offences.keys()) + 
                list(digital_offences.keys()) + 
                list(offence_related_to_currency_note.keys()) +  
                list(gambling.keys())
            )
        if crime in crime_lst:
            # लाख
            lakh = re.search(r'([\d०१२३४५६७८९]+|[अ-ह]+)\s*लाख', text)
            if lakh:
                lakh_word = lakh.group(1)
                if lakh_word.isdigit() or all(ch in '०१२३४५६७८९' for ch in lakh_word):
                    lakh_value = convert_hindi_numerals(lakh_word)
                else:
                    lakh_value = extract_number_from_words(lakh_word)
                # print(int(lakh_value))
                score += int(lakh_value) * 2
            # करोड़
            crore = re.search(r'([\d०१२३४५६७८९]+|[अ-ह]+)\s*करोड़', text)
            if crore:
                crore_word = crore.group(1)
                if crore_word.isdigit() or all(ch in '०१२३४५६७८९' for ch in crore_word):
                    crore_value = convert_hindi_numerals(crore_word)
                else:
                    crore_value = extract_number_from_words(crore_word)
                # print(int(crore_value))
                score += int(crore_value) * 10

    return score

def extract_crime_category(text):
    # Check for crimes by police first
    for police_crime_keyword in crimes_by_police:
        if police_crime_keyword in text:
            return "Crime by Police"

    # If no police crime keyword found, check for general crime types
    for public_crime_keyword in all_crime_types:
        if public_crime_keyword in text:
            return "Crime by Public"

    # If no relevant keyword is found
    return "Other"
    
def extract_summary_string(text):
    heading = f"🗞️ {extract_district(text)},  {extract_police_station(text)}___{extract_date(text)}___प्राथमिकी संख्या {extract_fir_number(text)}"
    summary = (
        f"{extract_accused(text)} को {extract_crime_type(text)} के मामले में आरोपी बनाया गया है। "
        f"इस प्रकरण में शिकायतकर्ता का नाम {extract_complainant(text)} है। "
    ) 
    return heading,summary