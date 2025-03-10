import csv
import re
import math

def fixAge(data_rows):
    for row in data_rows:
        age = row[1].strip()  # Get the age column value and remove spaces
        if re.match(r'^\d+-\d+$', age):  # Check if it's an age range
            lower, upper = map(int, age.split('-'))
            age = (upper + lower) / 2
            age = math.ceil(age)
            row[1] = str(age)

def fixDate(data_rows):
    for row in data_rows:
        for i in [8, 9, 10]:  # Assuming date columns are at indices 8, 9, 10
            date = row[i].strip()
            if date:
                day, month, year = date.split('.')
                new_date = f"{month}.{day}.{year}"
                row[i] = new_date

def fixLongLat(data_rows):
    province_latitudes = {}
    province_longitudes = {}
    province_counts = {}

    # First loop to accumulate latitude and longitude totals per province
    for row in data_rows:
        province = row[4].strip()
        latitude = row[6].strip()
        longitude = row[7].strip()

        try:
            if latitude.lower() != 'nan' and latitude != "":
                latitude = float(latitude)  # Convert to float if not 'nan'
            else:
                latitude = None  # Mark invalid latitudes as None
        except ValueError:
            latitude = None  # If not a valid number, set to None

        try:
            if longitude.lower() != 'nan' and longitude != "":
                longitude = float(longitude)  # Convert to float if not 'nan'
            else:
                longitude = None  # Mark invalid longitudes as None
        except ValueError:
            longitude = None  # If not a valid number, set to None

        # Initialize dictionaries for provinces if not already added
        if province not in province_latitudes:
            province_latitudes[province] = 0
            province_longitudes[province] = 0
            province_counts[province] = 0

        # Add valid latitude and longitude to province totals
        if latitude is not None:
            province_latitudes[province] += latitude
        if longitude is not None:
            province_longitudes[province] += longitude
        province_counts[province] += 1  # Increment the count for this province

    # Calculate the averages for each province
    for province in province_latitudes:
        # Calculate the average
        province_latitudes[province] /= province_counts[province]
        province_longitudes[province] /= province_counts[province]

        # Round the averages to 2 decimal places
        province_latitudes[province] = round(province_latitudes[province], 2)
        province_longitudes[province] = round(province_longitudes[province], 2)

    # Second loop to update the rows with the calculated average latitudes/longitudes
    for row in data_rows:
        province = row[4].strip()
        latitude = row[6].strip()
        longitude = row[7].strip()

        if latitude.lower() == 'nan' or latitude == "" or latitude is None:
            row[6] = str(province_latitudes.get(province, 'NaN'))  # Replace with average latitude

        if longitude.lower() == 'nan' or longitude == "" or longitude is None:
            row[7] = str(province_longitudes.get(province, 'NaN'))  # Replace with average longitude

def fixCity(data_rows):
    provinceCityCounts = {}

    for row in data_rows:
        city = row[3].strip()
        province = row[4].strip()

        if city.lower() == 'nan' or city == "":
            continue

        if province not in provinceCityCounts:
            provinceCityCounts[province] = {}

        if city not in provinceCityCounts[province]:
            provinceCityCounts[province][city] = 0
        
        provinceCityCounts[province][city] += 1  # Increment the count for this province
    
    provinceMostCommon = {}

    for province, cityCounts in provinceCityCounts.items():
        # Sort cities first by count (descending), then by name (alphabetically)
        most_common_city = sorted(cityCounts.items(), key=lambda x: (-x[1], x[0]))[0][0]
        provinceMostCommon[province] = most_common_city
        
    for row in data_rows:
        city = row[3].strip()
        province = row[4].strip()

        if city.lower() == 'nan' or city == "" or city is None:
            row[3] = provinceMostCommon.get(province, 'NaN')

def fixSymptom(data_rows):
    provinceSymptom = {}

    for row in data_rows:
        province = row[4].strip()
        symptom = row[11].strip()

        if symptom.lower() == 'nan' or symptom == "":
            continue

        symptom = symptom.replace('; ', ';').replace(';', ';')
        symptomList = symptom.split(';')

        for symptom in symptomList:
            symptom = symptom.strip()

            if province not in provinceSymptom:
                provinceSymptom[province] = {}
            
            if symptom not in provinceSymptom[province]:
                provinceSymptom[province][symptom] = 0
        
            provinceSymptom[province][symptom] += 1  # Increment the count for this province

    provinceMostCommon = {}

    for province, symptomCounts in provinceSymptom.items():
        # Sort symptoms first by count (descending), then by name (alphabetically)
        most_common_symptom = sorted(symptomCounts.items(), key=lambda x: (-x[1], x[0]))[0][0]
        provinceMostCommon[province] = most_common_symptom
    
    for row in data_rows:
        province = row[4].strip()
        symptom = row[11].strip()

        if symptom.lower() == 'nan' or symptom == "" or symptom is None:
            row[11] = provinceMostCommon.get(province, 'NaN')

def main():
    with open('covidTrain.csv') as csvfile:
        reader = csv.reader(csvfile)
        
        # Read all rows into a list, including the header
        rows = list(reader)
        header = rows[0]  # The first row is the header

        with open('covidResult.csv', 'w', newline='') as csvout:
            writer = csv.writer(csvout)

            # Write the header row to the output file
            writer.writerow(header)

            # Process all rows
            data_rows = rows[1:]  # Exclude the header row
            fixAge(data_rows)
            fixDate(data_rows)
            fixLongLat(data_rows)  
            fixCity(data_rows)
            fixSymptom(data_rows)

            # Write the modified rows to the output file after all functions have run
            for row in data_rows:
                writer.writerow(row)

if __name__ == '__main__':
    main()
