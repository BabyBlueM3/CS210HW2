import csv
import re
from collections import defaultdict, Counter
import math

def firePercent(dataRows):
    totalCount = 0
    countValid = 0

    for row in dataRows:
        level = row[2].strip()
        type = row[4].strip()
        
        if type.lower() != 'fire':
            continue

        try:
            level = float(level)
        except ValueError:
            continue
        
        totalCount += 1
        
        if level >= 40:
            countValid += 1
          
    result = (countValid / totalCount) * 100

    if result - math.floor(result) >= 0.5:
        result = math.ceil(result)
    else:
        result = math.floor(result)

    return result

def fixType(dataRows):

    commonWeakness = defaultdict(list)
    commonCount = {}

    for row in dataRows:

        type = row[4].strip()
        weakness = row[5].strip()        

        if type.lower() == 'nan':
            continue

        commonWeakness[weakness].append(type)

        for weakness, type in commonWeakness.items():
            typeCounter = Counter(type)
            commonType = typeCounter.most_common(1)[0]
            commonCount[weakness] = commonType
    
    for row in dataRows:
        type = row[4].strip()
        weakness = row[5].strip()

        if type.lower() == 'nan' or type == "" or type is None:
                if weakness in commonCount:
                    row[4] = commonCount.get(weakness, 'unknown')[0]


def fixAtkDefHp(dataRows):

    def calculate_averages(level_threshold, greater_than=True):
        atkTotal = 0
        defTotal = 0 
        hpTotal = 0
        countAtk = 0
        countDef = 0
        countHp = 0
        for row in dataRows:
            try:
                level = float(row[2].strip())
            except ValueError:
                continue

            if (level > level_threshold if greater_than else level <= level_threshold):

                atk = row[6].strip()
                defense = row[7].strip()
                hp = row[8].strip()
                
                if atk.lower() != 'nan' and atk != "":            
                    atkTotal += float(atk)
                    countAtk += 1
                if defense.lower() != 'nan' and defense != "":            
                    defTotal += float(defense)
                    countDef += 1
                if hp.lower() != 'nan' and hp != "":            
                    hpTotal += float(hp)
                    #print(hp)
                    countHp += 1        

        
        return round(atkTotal / countAtk, 1), round(defTotal / countDef, 1), round(hpTotal / countHp, 1)

    # Calculate averages for levels > 40 and <= 40
    atkAvgHigh, defAvgHigh, hpAvgHigh = calculate_averages(40, greater_than=True)
    atkAvgLow, defAvgLow, hpAvgLow = calculate_averages(40, greater_than=False)



    # Fill missing values based on level category
    for row in dataRows:
        try:
            level = float(row[2].strip())
        except ValueError:
            continue

        atk = row[6].strip()
        defense = row[7].strip()
        hp = row[8].strip()

        if level > 40:
            if atk.lower() == 'nan' or atk == "": 
                row[6] = atkAvgHigh
            if defense.lower() == 'nan' or defense == "": 
                row[7] = defAvgHigh
            if hp.lower() == 'nan' or hp == "": 
                row[8] = hpAvgHigh
        else:
            if atk.lower() == 'nan' or atk == "": 
                row[6] = atkAvgLow
            if defense.lower() == 'nan' or defense == "": 
                row[7] = defAvgLow
            if hp.lower() == 'nan' or hp == "": 
                row[8] = hpAvgLow

def typeToPerson(dataRows):
    typeDict = defaultdict(list)

    for row in dataRows:
        personality = row[3].strip()
        type = row[4].strip()

        typeDict[type].append(personality)
    
    sortedDict = sorted(typeDict.keys())

    typeDict = {key: typeDict[key] for key in sortedDict}


    for type, personality in typeDict.items():
        typeDict[type] = tuple(sorted(typeDict[type]))



    return (typeDict)

def avgHP(dataRows):

    HPsum = 0
    count = 0

    for row in dataRows:
        
        hp = row[8]
        stage = row[9].strip()

        try:
            hp = float(hp) 
            stage = float(stage)  
        except ValueError:
            continue  

        if stage == 3.0:
            HPsum += hp
            count += 1
    HPsum = HPsum / count
    result = HPsum


    if result - math.floor(result) >= 0.5:
        result = math.ceil(result)
    else:
        result = math.floor(result)
    return result




def main():
    input_file = 'pokemonTrain.csv'
    output_txt = 'pokemon1.txt'
    output_txt2 = 'pokemon4.txt'
    output_txt3 = 'pokemon5.txt'
    output_csv = 'pokemonResult.csv'  # Result file with all rows

    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Read all rows, including the header
        rows = list(reader)
        if not rows:
            print("Error: The input CSV file is empty.")
            return

        header = rows[0]  
        dataRows = rows[1:]  # Exclude the header row

        # Apply data processing functions
        firePercentage = firePercent(dataRows)  
        fixType(dataRows)      
        fixAtkDefHp(dataRows)
        averageHP = avgHP(dataRows)

        # Write processed data to both output CSV files
        for output_file in [output_csv]:
            with open(output_file, 'w', newline='') as csvout:
                writer = csv.writer(csvout)
                writer.writerow(header)  
                writer.writerows(dataRows)

        # Generate the Pokemon type to personality mapping and write to output_txt2
        sortedTypeDict = typeToPerson(dataRows)         

        with open(output_txt2, 'w') as txtout:
            txtout.write("Pokemon type to personality mapping:\n\n")

            for poke_type, personalities in sortedTypeDict.items():
                # Write each type and its sorted personalities to the text file
                txtout.write(f"    {poke_type}: {', '.join(personalities)}\n")

        with open(output_txt, 'w') as txtout:
            txtout.write(f"Percentage of fire type Pokemons at or above level 40 = {firePercentage}\n")

        with open(output_txt3, 'w') as txtout:
            txtout.write(f"Average hit point for Pokemons of stage 3.0 = {averageHP}\n")


main()

