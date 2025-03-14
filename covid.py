import csv
import re
import math

def fixAge(dataRows):
    for row in dataRows:
        age = row[1].strip()  # Remove leading/trailing spaces
        match = re.match(r'^(\d+)-(\d+)$', age)  # Match age ranges

        if match:
            lower, upper = map(int, match.groups())  # Extract numbers
            avg_age = round((lower + upper) / 2)  # Use standard rounding
            row[1] = str(avg_age)  # Replace with rounded average

def fixDate(dataRows):
    for row in dataRows:
        for i in [8, 9, 10]:  # Assuming date columns are at indices 8, 9, 10
            date = row[i].strip()
            if date:
                day, month, year = date.split('.')
                new_date = f"{month}.{day}.{year}"
                row[i] = new_date

def fixLongLat(dataRows):
    province_latitudes = {}
    province_longitudes = {}
    
    province_counts_latitude = {}
    province_counts_longitude = {}

    # First loop to accumulate latitude and longitude totals per province
    for row in dataRows:
        province = row[4].strip()
        latitude = row[6].strip()
        longitude = row[7].strip()

        # Try converting latitude
        try:
            lat = float(latitude) if latitude and latitude.lower() != 'nan' else None
        except ValueError:
            lat = None

        # Try converting longitude
        try:
            lon = float(longitude) if longitude and longitude.lower() != 'nan' else None
        except ValueError:
            lon = None

        # Initialize province keys if not already present
        if province not in province_latitudes:
            province_latitudes[province] = 0
            province_counts_latitude[province] = 0
        
        if province not in province_longitudes:
            province_longitudes[province] = 0
            province_counts_longitude[province] = 0

        # Accumulate valid latitudes
        if lat is not None:
            province_latitudes[province] += lat
            province_counts_latitude[province] += 1

        # Accumulate valid longitudes
        if lon is not None:
            province_longitudes[province] += lon
            province_counts_longitude[province] += 1

    # print(dict(province_latitudes))
    # print(dict(province_counts_latitude))
    # print(dict(province_longitudes))
    # print(dict(province_counts_longitude))

    # Calculate average latitudes and longitudes per province
    province_avg_lat = {}
    province_avg_lon = {}

    for province in province_latitudes:
        if province_counts_latitude[province] > 0:  # Avoid division by zero
            province_avg_lat[province] = round(province_latitudes[province] / province_counts_latitude[province], 2)
        else:
            province_avg_lat[province] = 'NaN'  # If no valid latitudes, assign NaN

        if province_counts_longitude[province] > 0:  # Avoid division by zero
            province_avg_lon[province] = round(province_longitudes[province] / province_counts_longitude[province], 2)
        else:
            province_avg_lon[province] = 'NaN'  # If no valid longitudes, assign NaN
    
    print(dict(province_avg_lat))
    print(dict(province_avg_lon))


    
    # Second loop to replace missing latitudes/longitudes in dataRows
    for row in dataRows:
        province = row[4].strip()

        if row[6].strip().lower() == 'nan' or row[6].strip() == "":
            row[6] = str(province_avg_lat.get(province, 'NaN'))  # Replace with average latitude

        if row[7].strip().lower() == 'nan' or row[7].strip() == "":
            row[7] = str(province_avg_lon.get(province, 'NaN'))  # Replace with average longitude


def fixCity(dataRows):
    provinceCityCounts = {}

    for row in dataRows:
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
        
    for row in dataRows:
        city = row[3].strip()
        province = row[4].strip()

        if city.lower() == 'nan' or city == "" or city is None:
            row[3] = provinceMostCommon.get(province, 'NaN')

def fixSymptom(dataRows):
    provinceSymptom = {}

    for row in dataRows:
        province = row[4].strip()
        symptom = row[11].strip()

        if symptom.lower() == 'nan' or symptom == "":
            continue

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
    
    for row in dataRows:
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
            dataRows = rows[1:]  # Exclude the header row
            fixAge(dataRows)
            fixDate(dataRows)
            fixLongLat(dataRows)  
            fixCity(dataRows)
            fixSymptom(dataRows)

            # Write the modified rows to the output file after all functions have run
            for row in dataRows:
                writer.writerow(row)

if __name__ == '__main__':
    main()
