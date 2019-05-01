class Tiles:
    #properties
    def __init__(self,name):
        #changeables
        self.owned = False
        self.canbeowned = False
        self.hasprice = False
        self.haspieces = False
        self.islocation = False
        self.name = name
        self.playerson = []
        self.sellprice = None
    def isOwned(self):
        return self.owned
    def isCanbeOwned(self):
        return self.canbeowned
    def isHasPrice(self):
        return self.hasprice
    def isHasPieces(self):
        return self.haspieces
    def __str__(self):
        return self.name

    #methods
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        toadd=[player1]
        possible=[player2, player3, player4]
        for x in possible:
            if x is not None:
                toadd.append(x)
        for y in toadd:
            self.playerson.append(y)
        return

    def Leave(self, player1, player2=None, player3=None, player4=None):
        toremove = [player1]
        possible = [player2, player3, player4]
        for x in possible:
            if x is not None:
                toremove.append(x)
        for y in toremove:
            self.playerson.remove(y)
        if self.playerson == None:
            self.haspieces = False
        return
    def getSellPrice(self):
        return self.sellprice
    #def xPos(self, playername):


