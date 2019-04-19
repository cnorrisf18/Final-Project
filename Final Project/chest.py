from tile import Tiles
class Chest(Tiles):
    #properties

    chestdict = {"Advance to Go": 1, "Bank Error:Collect $200": 2, "Doctor's Fees:Pay $50": 3,
                 "Sale of Stock:Collect $50": 4,
                 "Get out of Jail Free": 5, "Go to Jail": 6, "Grand Opera Night:Collect $50 from each player": 7,
                 "Holiday Fund Matures:Collect $100": 8, "Income Tax Refund:Collect $20": 9,
                 "Bday! Collect $10 from each player": 10, "Life insurance matures:Collect $100": 11,
                 "Hospital Fees:Pay $50": 12,
                 "School Fees:Pay $50": 13, "Consultancy Fee:Collect $25": 14,
                 "Street Repairs:Pay $40/house, $115/hotel": 15,
                 "Second price in beauty contest:Collect $10": 16, "Inherit $100": 17}


    def __init__(self, name = None, numcards = None):
        super().__init__(name=name)
        chanceCards =  {}
        self.startingcards = numcards
        self.numcards = numcards
        self.haspieces = False
        self.playerson = None
    def __str__(self):
        print(self.name)
    def isCanbeOwned(self):
        return self.canbeowned
    def isHasPrice(self):
        return self.hasprice
    def isHasPieces(self):
        return self.haspieces
    def getPieces(self):
        return self.playerson
    #methods
    def DrawCard(self):
        self.numcards = self.numcards - 1
        if self.numcards == 0:
            self.numcards = self.startingcards
