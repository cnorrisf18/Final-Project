from tile import Tiles
class Locations(Tiles):

    #properties
    def __init__(self, code = None, name=None, rentprice = None, sellprice = None, mortgageprice = None, houseprice = None):
        super().__init__(name=name)
        #fixed
        self.canbeowned = True
        self.hasprice = True
        self.rentprice = rentprice
        self.code = code
        #rent price will be a list: [1 house, 2 houses, 3 houses, 4 houses, hotel]
        self.pairs = []
        self.sellprice = sellprice
        self.mortgageprice = mortgageprice
        self.houseprice = houseprice
        #changeables
        self.monopoly = False
        self.hashouses = False
        self.howmanyhouses = 0
        self.hashotel = False
        self.mortgaged = False
        self.owner = None
    def __str__(self):
        return self.code

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
    def isHasHouses(self):
        return self.hashouses
    def getHowManyHouses(self):
        return self.howmanyhouses
    def isHasHotel(self):
        return self.hashotel
    def getOwner(self):
        return self.owner
    def getPieces(self):
        return self.playerson
    def getHousePrice(self):
        return self.houseprice
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
    def BuyHouses(self, numhouses):
        if self.hashotel == True:
            print("You can't buy houses on a property with a hotel.")
            return
        if self.mortgaged == True:
            print("Can't buy houses on a mortgaged property.")
            return
        if self.monopoly == False:
            print("Can only buy houses when you've got the monopoly.")
            return
        self.howmanyhouses = self.howmanyhouses + numhouses
        if self.howmanyhouses == 5:
            self.howmanyhouses = 0
            self.hashotel = True
        elif self.howmanyhouses > 5:
            print("Can't have more than a hotel.")
            return
    def SellHouses(self, numhouses):
        if self.hashotel == True:
            self.howmanyhouses = 5
            self.hashotel = False
        self.howmanyhouses = self.howmanyhouses-numhouses
        if numhouses > 5:
            print("Can't sell more than 5 houses.")
            return
        if self.howmanyhouses < 0:
            print("Can't have less than 0 houses.")
            return
    def ChargeRent(self):
        if self.hashotel == True:
            return self.rentprice[5]
        if self.monopoly == True and self.howmanyhouses==0:
            return self.rentprice[self.howmanyhouses] * 2
        return self.rentprice[self.howmanyhouses]
    def AddPairs(self, in1, in2 = None, in3 = None):
        optional=[in1, in2, in3]
        for n in optional:
            if n !=None:
                self.pairs.append(n)
        return self.pairs
