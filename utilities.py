from tile import Tiles
class Utilities(Tiles):
    #properties
    def __init__(self, name = None,rentprice = None, sellprice = None, mortgageprice = None):
        super().__init__(name=name)
        #fixed
        self.canbeowned = True
        self.hasprice = True
        self.rentprice = 40
        self.pairs = []
        self.sellprice = sellprice
        self.mortgageprice = mortgageprice
        self.islocation = False
        #changeables
        self.monopoly = False
        self.mortgaged = False
        self.owner = None
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
    def getSellPrice(self):
        return self.sellprice
    def getMortgagePrice(self):
        return self.mortgageprice
    def isMonopoly(self):
        return self.monopoly
    def getOwner(self):
        return self.owner
    def getPieces(self):
        return self.playerson
    #methods
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
    def ChargeRent(self):
        if self.monopoly is True:
            return 80
        else:
            return 40
    def AddPairs(self, in1, in2=None, in3=None):
        optional = [in1, in2, in3]
        for n in optional:
            if n != None:
                self.pairs.append(n)
        return self.pairs

