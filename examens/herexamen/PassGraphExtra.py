def players_list(self):
    """Geef een kopie van de spelerslijst."""
    result = []
    for p in self.players:
        result.append(p)
    return result


def passes(self):
    """Geef alle passes in de graaf."""
    all_passes = []
    for sender_name in self.adj:
        for p in self.adj[sender_name]:
            all_passes.append(p)
    return all_passes


class PassGraph:
    def __init__(self, path=None):
        self.players = []
        self.adj = {}

        if path is not None:
            self._load_from_txt(path)

    def _load_from_txt(self, path):
        try:
            f = open(path, "r", encoding="utf-8")
        except OSError:
            raise ValueError("Bestand kan niet geopend worden")

        section = None   # geen sectie tot we [PLAYERS] of [PASSES] lezen

        for line in f:
            line = line.strip()

            # lege regel → overslaan
            if line == "":
                continue

            # comment → overslaan
            if line.startswith("#"):
                continue

            # secties herkennen
            if line == "[PLAYERS]":
                section = "PLAYERS"
                continue
            if line == "[PASSES]":
                section = "PASSES"
                continue

            # onbekende sectie
            if line.startswith("[") and line.endswith("]"):
                f.close()
                raise ValueError("Onbekende sectie: " + line)

            if section is None:
                f.close()
                raise ValueError("Regel buiten sectie: " + line)

            # ---------------------------
            # PLAYERS inlezen
            # ---------------------------
            if section == "PLAYERS":
                if ";" not in line:
                    f.close()
                    raise ValueError("Ongeldige spelersregel: " + line)

                parts = line.split(";", 1)
                name = parts[0].strip()
                number_str = parts[1].strip()

                try:
                    number = int(number_str)
                except ValueError:
                    f.close()
                    raise ValueError("Ongeldig rugnummer: " + number_str)

                player = Player(name, number)
                self.add_player(player)

            # ---------------------------
            # PASSES inlezen
            # ---------------------------
            elif section == "PASSES":

                if ":" not in line:
                    f.close()
                    raise ValueError("Ongeldige passregel: " + line)

                left, nr_str = line.split(":", 1)
                nr_str = nr_str.strip()

                try:
                    nr = int(nr_str)
                except ValueError:
                    f.close()
                    raise ValueError("Foute nummerwaarde: " + nr_str)

                if nr <= 0:
                    f.close()
                    raise ValueError("Pass-aantal moet positief zijn")

                # links van de :
                if "->" not in left:
                    f.close()
                    raise ValueError("Ongeldige passregel: " + line)

                sender_part, receiver_part = left.split("->", 1)
                sender_name = sender_part.strip()
                receiver_name = receiver_part.strip()

                sender = self.get_player(sender_name)
                receiver = self.get_player(receiver_name)

                if sender is None or receiver is None:
                    f.close()
                    raise ValueError("Pass verwijst naar onbekende speler")

                self.add_pass(sender, receiver, nr)

        f.close()

    def save_to_txt(self, path):
        f = open(path, "w", encoding="utf-8")

        # spelers
        f.write("[PLAYERS]\n")
        for p in self.players:
            f.write(p.name + ";" + str(p.number) + "\n")

        # passes
        f.write("[PASSES]\n")
        for sender_name in self.adj:
            for p in self.adj[sender_name]:
                sender = p.get_start().name
                receiver = p.get_end().name
                nr = p.get_weight()
                f.write(sender + " -> " + receiver + " : " + str(nr) + "\n")

        f.close()
