# https://dodona.be/nl/activities/962940240/

class Player:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __eq__(self, other):
        if (isinstance(other, Player) and self.name == other.name):
            return True
        else:
            return False


    def __lt__(self, other):
        if isinstance(other, Player):
            if self.number < other.number:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __str__(self):
        return f"{self.name} ({self.number})"

def main():
    # Testscenario voor Player

    p1 = Player("Eden Hazard", 10)
    p2 = Player("Moussa Dembele", 19)
    p3 = Player("Jan Vertonghen", 5)

    # spelers in lijst
    players = [p1, p2, p3]

    # Print één object
    print(p1)

    # Test eq methode
    print(p1 == Player("Eden Hazard", 99))  # True (naam gelijk, nummer genegeerd)
    print(p1 == p2)  # False

    # Test lt via sorted()
    sorted_players = sorted(players)

    # Print gesorteerde lijst
    for player in sorted_players:
        print(player)

main()





