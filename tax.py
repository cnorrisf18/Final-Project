from tile import Tiles

class Tax(Tiles):
    #properties
    def __init__(self, name =None, taxprice = None):
        super().__init__(name=name)
        self.taxprice = taxprice
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
    def getTaxprice(self):
        return self.taxprice
    #methods
    def ChargeTax(self):
        return self.taxprice