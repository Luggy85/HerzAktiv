import json
import time

# Opening JSON file
file = open("data/person_db.json")

# Loading the JSON File in a dictionary
person_data = json.load(file)


def load_person_data():
    """Funktion zum Laden der Personendaten aus einer JSON-Datei."""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data


def get_person_list(person_data):
    """Funktion zum Extrahieren der Personennamen aus den Personendaten."""
    # person_data = load_person_data()
    person_list = []
    for person in person_data:
        person_list.append(person['firstname'] +' '+ person['lastname'])
    return person_list

def find_person_data_by_name(suchstring):
    """Funktion zum Finden von Personendaten anhand des Namens."""
    if suchstring == 'None':
        return {}
    
    # Teilt einen String und speichert die Ergebnisse in einer Liste
    two_names = suchstring.split(" ")
    vorname = two_names[0]
    nachname = two_names[1]

    person_data = load_person_data()


    # Nun können wir vergleichen bis wir einen Treffer finden
    for entry in person_data:
        #print(entry)
        if (entry["firstname"] == vorname and entry["lastname"] == nachname):
            print()

            return entry
    else:
        return {}

# Finde das Alter anhand des Geburtsjahres
def find_age(suchstring):
    current_year = time.localtime().tm_year
    birth_year = find_person_data_by_name(suchstring)['date_of_birth']
    age = current_year - birth_year
    return age
        

if __name__ == "__main__":
    person_dict = load_person_data()
    person_names = get_person_list(person_dict)
    found_person_data = find_person_data_by_name("Yunus Schmirander")
    person_age = find_age("Yunus Schmirander")
    print(person_names)
    print(found_person_data)
    print(person_age)
    
