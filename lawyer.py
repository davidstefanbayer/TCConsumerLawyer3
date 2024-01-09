from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from fuzzywuzzy import fuzz 

class Lawyer:
    def __init__(self, name, budget, location, expertise):
        self.name = name
        self.budget = budget
        self.location = location
        self.expertise = expertise

    def __repr__(self):
        return f"Lawyer(Name: {self.name}, Hourly Fee: {self.budget}, Location: {self.location}, Expertise: {self.expertise})"

# Property Lawyers
lawyer_1 = Lawyer("Pfordte Bosbach Rechtsanwälte", 250, "Oskar-Schlemmer-Straße 3, 80807 München", "property")
lawyer_2 = Lawyer("DMS Rechtsanwälte Duchon, Meißner, Schütrumpf", 300, "Finkenstr. 5, 80333 München", "property")
lawyer_9 = Lawyer("Berger & Stein Rechtsanwälte", 275, "Leopoldstraße 244, 80807 München", "property")
lawyer_10 = Lawyer("Kanzlei Schwarz & Partner", 320, "Maximilianstraße 35, 80539 München", "property")

# Tax Lawyers
lawyer_3 = Lawyer("Rose & Partner", 200, "Fürstenfelder Straße 5, 80331 München", "tax")
lawyer_4 = Lawyer("McDermott Will & Emery Rechtsanwälte ", 350, "Nymphenburger Str. 3, 80335 München", "tax")
lawyer_11 = Lawyer("Bauer & Müller Steuerkanzlei", 210, "Sonnenstraße 19, 80331 München", "tax")
lawyer_12 = Lawyer("Kanzlei Weiss & Lang", 330, "Theresienstraße 1, 80333 München", "tax")

# Family Lawyers
lawyer_5 = Lawyer("Garlipp & Kollegen Rechtsanwälte", 150, "Nymphenburger Str. 185, 80634 München", "divorce")
lawyer_6 = Lawyer("Vera Templer & Parnter", 275, "Sebastiansplatz 8, 80331 München", "divorce")
lawyer_13 = Lawyer("Kanzlei Fischer & Sohn", 165, "Ludwigstraße 8, 80539 München", "divorce")
lawyer_14 = Lawyer("Müller & Wagner Familienrecht", 280, "Schellingstraße 109, 80798 München", "divorce")

# Environmental Lawyers
lawyer_7 = Lawyer("Graf von Wesphalen & Partner", 225, "Nymphenburger Straße 64, 80335 München", "environmental")
lawyer_8 = Lawyer("Environmental Lawyer Name 2", 300, "Elisenstraße 3, 80335 München", "environmental")
lawyer_15 = Lawyer("Kanzlei Grün & Partner", 240, "Lindwurmstraße 10, 80337 München", "environmental")
lawyer_16 = Lawyer("Baum & Wald Umweltrecht", 315, "Brienner Straße 55, 80333 München", "environmental")



#  geolocator
geolocator = Nominatim(user_agent="TUMConsumerLawyerTC")

class LawyerMatcher:
    def __init__(self, lawyers):
        self.lawyers = lawyers

    def get_coordinates(self, address):
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude) if location else None

    def find_matching_lawyers(self, max_fee, user_location, expertise_needed):
        user_coordinates = self.get_coordinates(user_location)
        matching_lawyers = []

        for lawyer in self.lawyers:
            if lawyer.expertise == expertise_needed and lawyer.budget <= max_fee:
                lawyer_coordinates = self.get_coordinates(lawyer.location)
                if user_coordinates and lawyer_coordinates:
                    distance = geodesic(user_coordinates, lawyer_coordinates).km
                    distance = round(distance, 2)  #two decimal places
                    matching_lawyers.append((lawyer, distance))

        matching_lawyers.sort(key=lambda x: x[1])
        return matching_lawyers

def get_user_inputs():
    max_fee = float(input("Please enter your maximum budget (e.g., 300.0): "))
    user_location = input("Please enter your address (e.g., 'Maximilianstraße 34, 80539 München'): ")
    user_problem = input("Please describe your problem in up to 2000 words: ") 
    expertise_needed = input("Please confirm the area of expertise (based on your input:'property'): ")
    return max_fee, user_location, expertise_needed

max_hourly_fee, user_location, expertise_needed = get_user_inputs()

matcher = LawyerMatcher([lawyer_1, lawyer_2, lawyer_3, lawyer_4, lawyer_5, lawyer_6, lawyer_7, lawyer_8])

print(f"Your address is: {user_location}")
user_coordinates = matcher.get_coordinates(user_location)
print()
print(f"Coordinates: {user_coordinates}")
print()
print(f"Law expertise needed: {expertise_needed}")
print()
print(f"Max hourly budget: {max_hourly_fee}")
print()


matching_lawyers = matcher.find_matching_lawyers(max_hourly_fee, user_location, expertise_needed)

if matching_lawyers:
    closest_lawyer, closest_distance = matching_lawyers[0]
    print(f"Your matching lawyer is {closest_lawyer.name} and is located at {closest_lawyer.location}, {closest_distance} km away.")

    documents = ["ID", "signed property deed", "copy of your rental agreement"]

    document_list = "\n".join([f"- {doc}" for doc in documents])

    print(f"It looks like you're having a legal dispute with your neighbor. Please prepare the following documents:\n{document_list}")
    print()
    print()
    print(f"Based on the information you provided, we estimate your fees to be: 249.00 EUR.")
    print()
    print(f"Furthermore, we estimate the case to be resolved by February 23rd 2024.")
else:
    print("No matching lawyers found based on your criteria.")
