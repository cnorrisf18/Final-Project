from tile import Tiles
class Railroads(Tiles):
    #properties
    def __init__(self, name=None, rentprice = None, sellprice = None, mortgageprice = None):
        super().__init__(name=name)
        self.canbeowned = True
        self.hasprice = True
        self.rentprice = rentprice
        self.pairs = None
        self.sellprice = sellprice
        self.mortgageprice = mortgageprice
        self.name=name
        # changeables
        self.monopoly = False
        self.mortgaged = False
        self.owner = None
        self.playerson = None
    def __str__(self):
        return self.name
    def isOwned(self):
        return self.owned
    def isCanbeOwned(self):
        return self.canbeowned
    def isHasPrice(self):
        return self.hasprice
    def isHasPieces(self):
        return self.haspieces
    def getRentPrice(self):
        return self.rentprice
    def getPairs(self):
        return self.pairs
    def getMortgagePrice(self):
        return self.mortgageprice
    def isMonopoly(self):
        return self.monopoly
    def getOwner(self):
        return self.owner
    def getPieces(self):
        return self.playerson
    # methods
    def Buy(self, player1):
        self.owned = True
        self.owner = player1
        return self.sellprice
    def Sell(self):
        self.owned = False
        self.owner = None
        return self.sellprice
    def Mortgage(self):
        self.mortgaged = True
        return self.mortgageprice
    def BecomeMonopoly(self):
        self.monopoly = True
    def LooseMonopoly(self):
        self.monopoly = False
    def ChargeRent(self, numowned):
        return self.rentprice[numowned - 1]
    def AddPairs(self, in1, in2=None, in3=None):
        self.pairs = [in1, in2, in3]
        return self.pairs