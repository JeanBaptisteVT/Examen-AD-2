from Speler import Player
from Pass import Pass

#https://dodona.be/nl/activities/947898035/

class PassGraph:
    def __init__(self):
        # lijst met alle Player-objecten
        self.players = []          # list[Player]
        # 2. De ADJACENCY LIST (NABIJHEIDSLIJST). Dit is het hart van de graaf.
        # Key (str): Spelersnaam (de Zender).
        # Value (list[Pass]): Lijst van alle passes die DÉZE speler gegeven heeft.
        self.adj = {}

    # Voorbeeld in de graaf:
    # self.adj = {
    #     "Piet": [Pass(Piet, Jan, 5), Pass(Piet, Klaas, 1)],
    #     "Jan": [Pass(Jan, Piet, 2), Pass(Jan, Klaas, 4)],
    #     "Klaas": [Pass(Klaas, Jan, 1)],
    #     "Hans": [Pass(Hans, Piet, 5)]
    # }
    # ---------- 1) BASIS: spelers ----------

    def add_player(self, player):
        """Voegt speler toe als die nog niet bestaat."""

        # controleren of speler al bestaat (op basis van naam)
        for p in self.players:
            if p.name == player.name:
                return  # speler bestaat al → niets doen

        # nieuwe speler toevoegen
        self.players.append(player)

        # in adj een lege lijst maken voor deze zender
        # zodat we later passes kunnen toevoegen zonder fouten
        self.adj[player.name] = []

    def has_player(self, player_or_name):
        """Controleert of een speler (Player of naam) in de graaf zit."""

        # als argument een Player is → gebruik player.name
        if isinstance(player_or_name, Player):
            name = player_or_name.name
        else:
            name = player_or_name  # anders is het een string

        # alle spelers overlopen
        for p in self.players:
            if p.name == name:
                return True

        return False

    def get_player(self, name):
        """Zoek Player met deze naam, of None."""
        for p in self.players:
            if p.name == name:
                return p
        return None

    # -------------------------------------------------------
    # 2) PASS-OPERATIES
    # -------------------------------------------------------

    def add_pass(self, sender, receiver, times=1):#times = 1 betekent: als je geen aantal meegeeft, telt de pass gewoon één keer.

        """Voegt een pass toe of verhoogt het aantal als ze al bestaat."""
#times = 1 betekent: als je geen aantal meegeeft, telt de pass gewoon één keer.

        if times <= 0:
            raise ValueError("times must be positive")

        # beide spelers moeten bestaan
        if not (self.has_player(sender) and self.has_player(receiver)):
            raise ValueError("Both players must already be added to the graph")

        # lijst van  passes van de zender
        passes_from_sender = self.adj[sender.name]

        # kijk of pass sender -> receiver al bestaat (heeft die al een pas gegeven aan die andere speler? Dan gewoont teller verhogen)
        for p in passes_from_sender:
            if p.get_end() == receiver:  # Pass.get_end geeft Player
                p.nr_of_times += times  # teller verhogen
                return

        # nog geen pass gevonden → nieuwe maken
        new_pass = Pass(sender, receiver, times)
        passes_from_sender.append(new_pass)

    def get_pass(self, sender_name, receiver_name):
        """Zoekt pass van sender naar receiver. Geeft Pass of None."""

        # lijst van passes vanuit sender (of lege lijst als onbekend)
        passes = self.adj.get(sender_name, [])

        # zoeken naar de juiste pass
        for p in passes:
            if p.get_end().name == receiver_name:
                return p
#p = Pass(Hazard, Lukaku, 3)
# p.get_end()       → Player-object: Lukaku
# p.get_end().name  → "Romelu Lukaku"
        return None

    def neighbors(self, sender_name):
        """Retouneert lijst van uitgaande passes van deze zender."""
        return self.adj.get(sender_name, [])
        # self.adj.get(sender_name, []):
        # - probeer de value (lijst van passes) op te halen voor key sender_name
        # - bestaat de key NIET → return de default: []
        #
        # Zonder die [] zou een onbekende sender_name leiden tot:
        # self.adj[sender_name]  → KeyError (programma crasht) (maar als die bestaat, geen probleem)
        # -------------------------------------------------------
        # 3) ANALYSEFUNCTIES
        # -------------------------------------------------------

    def total_weight(self, subset=None):
        # Als er geen subset is → neem alle spelers
        if subset is None:
            subset = []
            for p in self.players:
                subset.append(p.name)

        total = 0

        # Loop door elke zender
        for sender_name in self.adj:
            # Als zender niet in subset zit → overslaan
            if sender_name not in subset:
                continue

            # Loop door alle passes van deze zender
            for p in self.adj[sender_name]:
                receiver_name = p.get_end().name

                # Enkel tellen als ontvanger ook in subset zit
                if receiver_name in subset:
                    total += p.get_weight()

        return total

    def pass_intensity(self, subset=None):
        """
        intensiteit = totaal aantal passes binnen subset
                      ------------------------------------
                      maximaal aantal mogelijke passes (n*(n-1))
        """

        # subset leeg → neem iedereen
        if subset is None:
            subset = []
            for p in self.players:
                subset.append(p.name)

        n = len(subset)

        # minder dan 2 spelers → intensiteit = 0
        if n < 2:
            return 0.0

        numerator = self.total_weight(subset)  # echte passes
        denominator = n * (n - 1)  # mogelijke gerichte passes

        return numerator / denominator

    def top_pairs(self, k=5):
        """Retourneer top k passes met grootste nr_of_times."""

        all_passes = []

        for sender_name in self.adj:
            for p in self.adj[sender_name]:
                all_passes.append(p)

        for i in range(len(all_passes)):
            for j in range(len(all_passes) - 1):
                if all_passes[j].get_weight() < all_passes[j + 1].get_weight():
                    temp = all_passes[j]
                    all_passes[j] = all_passes[j + 1]
                    all_passes[j + 1] = temp

        # Neem de eerste k elementen
        result = []
        for i in range(min(k, len(all_passes))):
            result.append(all_passes[i])

        return result

    def distribution_from(self, sender_name):
        # Haal alle passes van de zender op
        pass_list = self.adj.get(sender_name, [])

        # Maak lijst (receiver_name, count)
        dist = []
        for p in pass_list:
            receiver = p.get_end().name
            count = p.get_weight()
            dist.append((receiver, count))

        # Sorteer op count (groot naar klein) zonder lambda
        for i in range(len(dist)):
            for j in range(len(dist) - 1):
                if dist[j][1] < dist[j + 1][1]:
                    temp = dist[j]
                    dist[j] = dist[j + 1]
                    dist[j + 1] = temp

        return dist


# Testscenario voor PassGraph

# 1. PassGraph object aanmaken
g = PassGraph()

# 2. Vier spelers aanmaken
p1 = Player("Eden Hazard", 10)
p2 = Player("Moussa Dembele", 19)
p3 = Player("Jan Vertonghen", 5)
p4 = Player("Romelu Lukaku", 9)

# 3. Spelers toevoegen aan de graaf
g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)

# 4. Zes passen toevoegen
g.add_pass(p1, p2, 3)   # Hazard → Dembele (3)
g.add_pass(p2, p1, 1)   # Dembele → Hazard (1)
g.add_pass(p1, p3, 2)   # Hazard → Vertonghen (2)
g.add_pass(p3, p4, 4)   # Vertonghen → Lukaku (4)
g.add_pass(p4, p1, 1)   # Lukaku → Hazard (1)
g.add_pass(p1, p2, 2)   # Hazard → Dembele opnieuw (2) → totaal 5

# 5. Analyse methodes testen

print("Total weight (alle spelers):")
print(g.total_weight())  # som van alle passes

print("\nPass intensity (alle spelers):")
print(g.pass_intensity())  # intensiteit over hele team

print("\nTop 3 pairs:")
for p in g.top_pairs(3):
    print(p, p.get_weight())

print("\nDistribution from Eden Hazard:")
print(g.distribution_from("Eden Hazard"))