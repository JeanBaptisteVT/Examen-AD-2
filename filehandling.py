"""
FILE HANDLING SAMENVATTING VOOR DIT PROJECT
-------------------------------------------

Focus: patronen die terugkomen in de oefeningen:
- tekstbestanden lezen (regel per regel)
- CSV-bestanden lezen/schrijven
- bestanden met secties en commentaar (bv. [PLAYERS]/[PASSES])
- woorden tellen in een tekst
- veilig werken met 'with open(...) as f'
"""


# ---------------------------------------------------------
# 1. BESTAND OPENEN MET 'with open(...) as f'
# ---------------------------------------------------------

# SLEUTELIDEE:
# - 'with' opent een bestand en sluit het automatisch, zelfs bij fouten.
# - file_path is een string, bv. "data/tasks.csv" of "input.txt".

def voorbeeld_lezen(file_path):
    # 'r' = read (alleen lezen), standaard
    with open(file_path, 'r', encoding='utf-8') as f:
        inhoud = f.read()      # leest hele bestand in één string
    return inhoud


# ---------------------------------------------------------
# 2. REGEL PER REGEL LEZEN
#    (belangrijk voor grote bestanden en de oefeningen)
# ---------------------------------------------------------

def lees_regel_per_regel(file_path):
    regels = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:                    # itereren over bestand = regel per regel
            line = line.strip()           # verwijdert \n en spaties aan begin/einde
            if line == "":                # lege regels overslaan
                continue
            regels.append(line)
    return regels


# ---------------------------------------------------------
# 3. STRIP EN SPLIT: BASIS VOOR PARSEN VAN LIJNEN
# ---------------------------------------------------------

def parse_player_line(line):
    """
    Voor lijnen zoals:
    'Eden Hazard;10'
    - strip(): 'Eden Hazard;10' (zonder \n)
    - split(';'): ['Eden Hazard', '10']
    """
    line = line.strip()
    naam, nummer_str = line.split(";")
    nummer = int(nummer_str)
    return naam, nummer


def parse_pass_line(line):
    """
    Voor lijnen zoals:
    'Eden Hazard -> Romelu Lukaku : 2'
    Stappen:
    1) strip()
    2) splitsen op '->'
    3) rechts nog eens splitsen op ':'
    4) strip op elk deel om spaties weg te doen
    """
    line = line.strip()
    # linker en rechter deel: "Eden Hazard " en " Romelu Lukaku : 2"
    sender_part, rest = line.split("->")
    sender_name = sender_part.strip()

    # " Romelu Lukaku : 2" -> ["Romelu Lukaku ", " 2"]
    receiver_part, count_part = rest.split(":")
    receiver_name = receiver_part.strip()
    count = int(count_part.strip())

    return sender_name, receiver_name, count


# ---------------------------------------------------------
# 4. BESTANDEN MET SECTIES: [PLAYERS] / [PASSES]
# ---------------------------------------------------------

def lees_pass_graph(file_path):
    """
    Formaat:
    [PLAYERS]
    naam;nummer
    ...
    [PASSES]
    sender -> receiver : aantal

    Extra regels:
    - Lege regels negeren
    - Commentaarregels (# ...) negeren
    """

    players = {}       # {naam: nummer}
    passes = {}        # {(sender, receiver): count}

    with open(file_path, 'r', encoding='utf-8') as f:
        mode = None    # None, "PLAYERS", of "PASSES"

        for raw_line in f:
            line = raw_line.strip()

            # lege of commentaarregel
            if line == "" or line.startswith("#"):
                continue

            # sectie wisselen
            if line == "[PLAYERS]":
                mode = "PLAYERS"
                continue
            if line == "[PASSES]":
                mode = "PASSES"
                continue

            # inhoud verwerken afhankelijk van sectie
            if mode == "PLAYERS":
                naam, nummer = parse_player_line(line)
                players[naam] = nummer

            elif mode == "PASSES":
                sender, receiver, count = parse_pass_line(line)
                key = (sender, receiver)
                # dubbele passes optellen
                passes[key] = passes.get(key, 0) + count

            else:
                # ongeldige input: we zitten niet in een sectie
                raise ValueError("Ongeldige input: lijn buiten sectie: " + line)

    return players, passes


# ---------------------------------------------------------
# 5. CSV-BESTAND LEZEN (EIGEN SIMPELE PARSER)
#    bv. voor takenlijst, voorraad, ...
# ---------------------------------------------------------

def lees_tasks_van_csv(file_path):
    """
    Verwacht bv. een CSV met header:
    task_name,duration,priority

    Doel: lijst van dicts teruggeven:
    [{"task_name": ..., "duration": ..., "priority": ...}, ...]
    """
    tasks = []

    with open(file_path, 'r', encoding='utf-8') as f:
        # eerste lijn = header overslaan
        header = f.readline()

        for line in f:
            line = line.strip()
            if line == "":
                continue

            parts = line.split(",")      # splitsen op komma
            if len(parts) != 3:
                raise ValueError(f"Ongeldige CSV-lijn: {line}")

            task_name = parts[0].strip()
            duration = int(parts[1].strip())
            priority = int(parts[2].strip())

            tasks.append({
                "task_name": task_name,
                "duration": duration,
                "priority": priority
            })

    return tasks


# ---------------------------------------------------------
# 6. CSV-BESTAND SCHRIJVEN
#    (bv. lijst van tasks terug wegschrijven)
# ---------------------------------------------------------

def schrijf_tasks_naar_csv(file_path, tasks):
    """
    tasks is een lijst van dicts zoals hierboven.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        # header
        f.write("task_name,duration,priority\n")

        for task in tasks:
            line = f"{task['task_name']},{task['duration']},{task['priority']}\n"
            f.write(line)


# ---------------------------------------------------------
# 7. WOORDEN SPLITSEN EN TELLEN IN EEN TEKSTBESTAND
#    (oefening woorden_splitsen / woorden_tellen)
# ---------------------------------------------------------

def is_letter(ch):
    # eenvoudige check: alfabetische letter
    return ch.isalpha()


def woorden_splitsen(file_path):
    """
    Definitie woord: zo lang mogelijke reeks letters.
    Alles wat geen letter is, is scheidingsteken.
    """
    woorden = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.lower()   # hoofdletters negeren
            huidig_woord = []

            for ch in line:
                if is_letter(ch):
                    huidig_woord.append(ch)
                else:
                    if huidig_woord:
                        woord = "".join(huidig_woord)
                        woorden.append(woord)
                        huidig_woord = []

            # laatste woord aan het einde van de regel niet vergeten
            if huidig_woord:
                woord = "".join(huidig_woord)
                woorden.append(woord)

    return woorden


def woorden_tellen(file_path):
    """
    Gebruikt woorden_splitsen en telt frequenties in een dict.
    """
    woorden = woorden_splitsen(file_path)
    freq = {}

    for w in woorden:
        freq[w] = freq.get(w, 0) + 1

    return freq


# ---------------------------------------------------------
# 8. FOUTAFHANDELING BIJ FILE HANDLING (BASIS)
# ---------------------------------------------------------

def veilig_lezen(file_path):
    """
    Typische patroon:
    - probeer te openen
    - als bestand niet bestaat → duidelijke foutmelding
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Bestand niet gevonden: {file_path}")


# ---------------------------------------------------------
# 9. OVERZICHT: BELANGRIJKE PATRONEN UIT DIT BESTAND
# ---------------------------------------------------------

def samenvatting():
    """
    Kernpatronen:
    - with open(path, mode, encoding='utf-8') as f:
    - for line in f:   # regel per regel lezen
    - line.strip() om \n en spaties weg te doen
    - line.startswith('#') om commentaar te herkennen
    - split(...) om onderdelen van een lijn te parsen
    - int(...), float(...) om strings naar getallen om te zetten
    - dict en lijst gebruiken om ingelezen data in geheugen te steken
    - bij schrijven: f.write("tekst\n") in een lus
    """
    pass
