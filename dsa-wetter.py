import random

class Day:
    def __init__(self, no, step1_result, step2_result, step3_result, step4_result) -> None:
        self.no = int(no)
        
        self.clouds = step1_result[1]
        self.wind = step2_result[1]
        self.day_temperature = str(step3_result[0])+"°C"
        self.night_temperature = str(step3_result[1])+"°C"

        self.step1_index = step1_result[0]
        self.step2_index = step2_result[0]
        self.step3_index = step3_result[0]
        self.step4_index = step4_result[0]
    
    def __str__(self) -> str:
        return f"""Tag {self.no}
{self.clouds}, {self.wind}
Temperatur: {self.day_temperature} bis {self.night_temperature}
"""
    def md(self) -> str:
        return f"- Tag {self.no}: {self.clouds}, {self.wind}, {self.day_temperature} - {self.night_temperature}\n"
    def csv(self) -> str:
        return f"Tag {self.no}, {self.clouds}, {self.wind}, {self.day_temperature}, {self.night_temperature}\n"

def log(*args):
    if options.verbose: print(*args)

def output_days(arg):
    if not isinstance(arg, list):
        arg = [arg]
    if options.format is not None and options.format.lower() == "csv":
        arg = [x.csv() for x in arg]
    if options.format is not None and options.format.lower() == "md":
        arg = [x.md() for x in arg]
    write(arg)

def write(lines):
    if options.filename is None:
        for l in lines:
            print(l)
        return
    
    log("Opening file:",options.filename)
    with open(options.filename, "w", encoding="utf-8") as outfile:
        outfile.writelines(lines)

def parse_arguments():
    from optparse import OptionParser
    parser = OptionParser()
    #Schritt 0
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Spuck enorm viel Holz aus.") #verbos für Debug
    parser.add_option("-f", "--format", dest="format", default=None, help="Ausgabeformat: Freitext, md oder csv. Standard ist Freitext.")
    parser.add_option("-o", "--output", dest="filename", default=None, help="Der Speicherort für die Ausgabe. Standard ist stdout.")
    parser.add_option("-x", "--seed", dest="seed", default=None, help="Setze den Seed manuell.")
    #Schritt 1
    parser.add_option("-d", "--desert", dest="is_desert", action="store_true", default=False, help="Die Gruppe befindet sich in der Wüste.") #in Wüste
    #Schritt 2
    parser.add_option("-s", "--season", dest="season", default="s", help="Die Jahreszeit - der Anfangsbuchstabe ist ausreichend. Standard ist Sommer.") #Jahreszeit
    parser.add_option("-w", "--windy", dest="is_windy", action="store_true", default=False, help="Es ist besonders windig.") #besonders windig
    #Schritt 3
    parser.add_option("-r", "--region", dest="region", default="zentrales mittelreich", help="Die Region wie angegeben auf S. 157 WdE. Standard ist Zentrales Mittelreich.") #Region
    #Schritt 6
    parser.add_option("-n", "--days", dest="days", default=1, help="Die Menge an Tagen, die generiert werden soll. Standard ist 1.") #Anzahl Tage
    global options, args
    options, args = parser.parse_args()

def step1():
    results = [
        # (Index, Bezeichnung, Temperaturmod tags)
        (0, "völlig wolkenlos", 10),
        (1, "einzelne Wolken", 5),
        (2, "bewölkt mit Wolkenlücken", 0),
        (3, "geschlossene Wolkendecke", -5)
    ]
    dice = random.randint(1,20)
    if options.is_desert:
        if 1 <= dice <= 16: return results[0]
        if 17 <= dice <= 18: return results[1]
        if dice == 19: return results[2]
        if dice == 20: return results[3]
    else:
        if 1 <= dice <= 4: return results[0]
        if 5 <= dice <= 10: return results[1]
        if 11 <= dice <= 16: return results[2]
        if 17 <= dice <= 20: return results[3]
    raise ValueError("Step 1: Dice result was",dice)

def step2():
    results = [
        #(Index, Bezeichnung, Temperaturmod)
        (0, "windstill", 4),
        (1, "leichter Wind", 2),
        (2, "sanfte Brise", 0),
        (3, "frische Brise", 0),
        (4, "steife Brise", -2),
        (5, "starker Wind", -4),
        (6, "Sturm", -6)
    ]
    dice = random.randint(1,20)
    if options.is_windy: dice += 1
    if options.season.lower()[0] == 'h':
        if 1 <= dice <= 3: return results[0]
        if 4 <= dice <= 5: return results[1]
        if 6 <= dice <= 7: return results[2]
        if 8 <= dice <= 10: return results[3]
        if 11 <= dice <= 14: return results[4]
        if 15 <= dice <= 18: return results[5]
        if 19 <= dice: return results[6]
    else:
        if 1 <= dice <= 4: return results[0]
        if 5 <= dice <= 7: return results[1]
        if 8 <= dice <= 10: return results[2]
        if 11 <= dice <= 13: return results[3]
        if 14 <= dice <= 16: return results[4]
        if 17 <= dice <= 19: return results[5]
        if 20 <= dice: return results[6]
    raise ValueError("Step 2: Dice result was",dice)

def step3(step1_tempmod: int, step2_tempmod: int):
    temp_by_region = {
        "ewiges eis": (-20,-30,-40),
        "höhen des ehernen schwerts": (-10,-20,-30),
        "hoher norden": (0,-10,-20),
        "tundra und taiga": (5,0,-5),
        "bornland, thorwal": (10,3,-5),
        "streitende königreiche bis weiden": (10,5,0),
        "zentrales mittelreich": (15,10,5),
        "nördliches horasreich, almada, aranien": (20,15,10),
        "höhen des raschtulswalls": (5,0,-10),
        "südliches horasreich, reich der ersten sonne": (25,20,15),
        "khom": (40,35,30),
        "echsensümpfe, meridiana": (30,25,20),
        "altoum, gewürzinseln, südmeer": (35,30,25)
    }
    if options.season.lower()[0] == 's': index = 0
    if options.season.lower()[0] in ('f','h'): index = 1
    if options.season.lower()[0] == 'w': index = 2
    day_temp = temp_by_region[options.region.lower()][index] + step1_tempmod + step2_tempmod
    night_temp = day_temp-(random.randint(1,20)+5)
    return (day_temp, night_temp)

def step4(step1_result):
    results = [
        (0, "kein Niederschlag"),
        (True, "Niederschlag")
    ]
    dice = random.randint(1,20)
    if step1_result[0] == 1 and dice <= 1: return results[1]
    if step1_result[0] == 2 and dice <= 4: return results[1]
    if step1_result[0] == 3 and dice <= 10: return results[1]
    return results[0]

def step4_0(step2_result, temperature, step4_result):
    results = [
        (1,"Nieselregen"),
        (2,"ergiebiger Regen"),
        (3,"Wolkenbruch")
    ]
    results_snow = [
        (1,"Ein paar Flocken"),
        (2,"ergiebiger Schneefall"),
        (3,"Dauerschnee/Hagel")
    ]
    dice = random.randint(1,20)
    if step2_result[0] == 0:
        if 1 <= dice <= 12: return results[0] if temperature > 0 else results_snow[0]
        if 13 <= dice <= 19: return results[1] if temperature > 0 else results_snow[1]
        if 20 <= dice: return results[2] if temperature > 0 else results_snow[2]
    if step2_result[0] == 1:
        if 1 <= dice <= 9: return results[0] if temperature > 0 else results_snow[0]
        if 10 <= dice <= 18: return results[1] if temperature > 0 else results_snow[1]
        if 19 <= dice: return results[2] if temperature > 0 else results_snow[2]
    if step2_result[0] == 2:
        if 1 <= dice <= 7: return results[0] if temperature > 0 else results_snow[0]
        if 8 <= dice <= 17: return results[1] if temperature > 0 else results_snow[1]
        if 18 <= dice: return results[2] if temperature > 0 else results_snow[2]
    if step2_result[0] == 3:
        if 1 <= dice <= 5: return results[0] if temperature > 0 else results_snow[0]
        if 6 <= dice <= 16: return results[1] if temperature > 0 else results_snow[1]
        if 17 <= dice: return results[2] if temperature > 0 else results_snow[2]
    if step2_result[0] == 4:
        if 1 <= dice <= 3: return results[0] if temperature > 0 else results_snow[0]
        if 4 <= dice <= 15: return results[1] if temperature > 0 else results_snow[1]
        if 16 <= dice: return results[2] if temperature > 0 else results_snow[2]
    if step2_result[0] == 5:
        if 1 <= dice <= 2: return results[0] if temperature > 0 else results_snow[0]
        if 3 <= dice <= 13: return results[1] if temperature > 0 else results_snow[1]
        if 14 <= dice: return results[2] if temperature > 0 else results_snow[2]
    if step2_result[0] == 6:
        if dice <= 1: return results[0] if temperature > 0 else results_snow[0]
        if 2 <= dice <= 10: return results[1] if temperature > 0 else results_snow[1]
        if 11 <= dice: return results[2] if temperature > 0 else results_snow[2]
    raise ValueError("Step 4_0: Dice result was",dice)

def step6():
    dice = random.randint(1,20)
    rtn = 0
    if options.season[0].lower() in ('s','w'):
        if dice in (13,18,19,20): rtn |= 0b1000 #Wolken
        if dice in (10,14,15,17,19,20): rtn |= 0b0100 #Windstärke
        if dice in (11,14,16,17,18,20): rtn |= 0b0010 #Temperatur
        if dice in (12,13,15,16,17,18,19,20): rtn |= 0b0001 #Niederschlag
    elif options.season[0].lower() in ('f','h'):
        if dice in (8,9,17,18,19,20): rtn |= 0b1000 #Wolken
        if dice in (5,10,11,12,13,16,18,19,20): rtn |= 0b0100 #Windstärke
        if dice in (6,10,11,14,15,16,17,19,20): rtn |= 0b0010 #Temperatur
        if dice in (7,8,9,12,13,14,15,16,17,18,19,20): rtn |= 0b0001 #Niederschlag
    else:
        raise ValueError(f"Schritt 6: Jahreszeit war {options.season}")
    return rtn

if __name__=='__main__':
    parse_arguments()
    log("Options: ", options)
    random.seed(options.seed)

    step6_flags = 0b1111 #1000=Wolken/Schritt1, 0100=Wind/Schritt2, 0010=Temperatur/Schritt3, 0001=Niederschlag/Schritt4
    days = []
    for i in range(int(options.days)):
        if step6_flags&0b1000:
            step1_result = step1()
            log("Schritt 1:",step1_result)
            step6_flags &= 0b0111

        if step6_flags&0b0100:
            step2_result = step2()
            log("Schritt 2:",step2_result)
            step6_flags &= 0b1011

        if step6_flags&0b0010:
            step3_result = step3(step1_result[2], step2_result[2])
            log("Schritt 3:",step3_result,"°C")
            step6_flags &= 0b1101

        if step6_flags&0b0001:
            step4_result = step4(step1_result)
            if step4_result[0]: step4_result = step4_0(step2_result, step3_result[0], step4_result)
            log("Schritt 4:",step4_result)
            step6_flags &= 0b1110
        
        days.append( Day(1+i, step1_result, step2_result, step3_result, step4_result) )
        step6_flags = step6()
        log("Schritt 6:",step6_flags)
    
    output_days(days)
