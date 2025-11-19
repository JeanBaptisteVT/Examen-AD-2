# PriorityQue Datastructuur

import heapq


class PriorityQueue:
    def __init__(self):
        self.content = []

    def add(self, item):
        heapq.heappush(self.content, item)

    def peek(self):
        return self.content[0]

    def poll(self):  # element met hoogste prioriteit uit de wachtrij halen
        return heapq.heappop(self.content) if len(self.content) > 0 else None

    def is_empty(self):
        return len(self.content) == 0

    def __str__(self):
        return str(heapq.nsmallest(len(self.content), self.content))


def simuleer_parking(aantaParkeerplaatsen: int, blokTijd: int, klanten: list):
    Time = 0
    pq = PriorityQueue()

    # Initialiseer de parkeerplaatsen
    Parkeerplaatsen = [0] * aantaParkeerplaatsen

    # Voeg alle klanten toe aan de wachtrij
    for klant in klanten:
        pq.add(klant)

    while not pq.is_empty():
        # Update tijd naar de eerstvolgende klant als nodig
        Time = max(Time, pq.peek()[0])

        # Zoek een beschikbare parkeerplaats
        parkeerplaats_gevonden = False
        for i in range(aantaParkeerplaatsen):
            if Parkeerplaatsen[i] <= Time:  # Parkeerplaats vrij
                Parkeerplaatsen[i] = Time + pq.peek()[1]  # Parkeer de klant
                pq.poll()  # Verwijder klant uit wachtrij
                parkeerplaats_gevonden = True
                break

        # Als er geen parkeerplaats beschikbaar is, verwerk de klant later
        if not parkeerplaats_gevonden:
            klant = pq.poll()
            pq.add((klant[0] + blokTijd, klant[1]))  # Verwerk klant later

    # Zoek de maximale eindtijd
    return max(Parkeerplaatsen)