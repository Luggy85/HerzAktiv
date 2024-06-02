import json
import time

class Person:

    @staticmethod
    def load_person_data():
        """Funktion zum Laden der Personendaten aus einer JSON-Datei."""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """Funktion zum Extrahieren der Personennamen aus den Personendaten."""
        person_list = []
        for person in person_data:
            person_list.append(person['firstname'] +' '+ person['lastname'])
        return person_list
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """Funktion zum Finden von Personendaten anhand des Namens."""
        if suchstring == 'None':
            return {}
        
        # Teilt einen String und speichert die Ergebnisse in einer Liste
        two_names = suchstring.split(" ")
        vorname = two_names[0]
        nachname = two_names[1]

        person_data = Person.load_person_data()


        # Nun können wir vergleichen bis wir einen Treffer finden
        for entry in person_data:
            #print(entry)
            if (entry["firstname"] == vorname and entry["lastname"] == nachname):
                print()

                return entry
        else:
            return {}

    def find_age(self):
        # Finde das Alter anhand des Geburtsjahres
        current_year = time.localtime().tm_year
        birth_year = self.date_of_birth
        age = current_year - birth_year
        return age
        
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict['date_of_birth']
        self.firstname = person_dict['firstname']
        self.lastname = person_dict['lastname']
        self.picture_path = person_dict['picture_path']
        self.id = person_dict['id']

if __name__ == "__main__":
    person_dict = Person.load_person_data()
    person_names = Person.get_person_list(person_dict)
    found_person_data = Person.find_person_data_by_name("Yunus Schmirander")
    
    person1 = Person(Person.find_person_data_by_name("Yunus Schmirander"))
    print(person1.date_of_birth)
    print(person1.find_age())

    print(person_names)
    print(found_person_data)
    
    
