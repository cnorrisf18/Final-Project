import turtle
import random

def getPos(x, y):
    print("(",x , y,")")
    return
def drawBoard(comchest, chance, player, comp1, comp2, comp3, board):
    #set background image
    board.setup(700, 700, None, None)
    board.bgpic("board.gif")
    #draw community chest and chance
    comchest.color("darkblue")
    comchest.penup()
    comchest.begin_fill()
    comchest.setpos(-227, 133)
    comchest.pendown()
    comchest.setpos(-157, 62)
    comchest.setpos(-56, 159)
    comchest.setpos(-128, 229)
    comchest.setpos(-227, 133)
    comchest.end_fill()
    chance.color("lightgreen")
    chance.penup()
    chance.begin_fill()
    chance.setpos(128, -231)
    chance.pendown()
    chance.setpos(229, -135)
    chance.setpos(155, -64)
    chance.setpos(57, -164)
    chance.setpos(128, -231)
    chance.end_fill()
    #set up players
    player.penup()
    player.setpos(267, -272)
    player.pendown()
    comp1.penup()
    comp1.setpos(322, -270)
    comp1.pendown()
    comp2.penup()
    comp2.setpos(268, -313)
    comp2.pendown()
    comp3.penup()
    comp3.setpos(326, -320)
    comp3.pendown()
    #coord testing (will be removed eventually)
    #board.onscreenclick(getPos)
    #board.mainloop()
class Player(turtle.Turtle):
    def __init__(self, name, color, shape):
        super().__init__()
        #fixed
        self.name=name
        self.color(color)
        self.shape(shape)
        #changeables
        self.bank=1500
        self.spaceon=None
        self.injail=False
        self.owned=[]
        self.bankrupt=False

    def __str__(self):
        return self.name
    def addBank(self, amount):
        self.bank=self.bank+amount
        return self.bank
    def subBank(self, amount):
        self.bank=self.bank-amount
        return self.bank
    def goBankrupt(self):
        global classes
        done = False
        while not done:
            sell = input(
                "{}, you're about to go bankrupt! Currently, you've got {} in the bank. Would you like to sell houses "
                "or mortgage property to avoid this? Enter S for sell houses, M for mortgage property, or N for no."
                    .format(self.name, self.bank))
            if sell == 'S' or sell == 's':
                propstr = input("What property would you like to sell houses from?")
                propstr = propstr.lower()
                propstr = propstr.replace(" ", "")
                property = classes[propstr]
                numhouses = input("How many houses would you like to sell from {}?".format(property))
                self.bank = self.sellHouses(property, numhouses)
                if self.bank >= 0:
                    done = True
                    return self.bank
            elif sell == 'M' or sell == 'm':
                propstr = input("What property would you like to mortgage?")
                propstr = propstr.lower()
                propstr = propstr.replace(" ", "")
                property = classes[propstr]
                self.bank = self.mortgageProperty(property)
                if self.bank >= 0:
                    done = True
                    return self.bank
            elif sell == 'N' or sell == 'n':
                print("{}, you have gone bankrupt!".format(self.name))
                for prop in self.owned:
                    prop.Sell()
                self.bank=0
                self.owned=[]
                self.bankrupt=True
                done = True
                return
            else:
                print("Invalid input, try again")
    def isBankrupt(self):
        return self.bankrupt
    def getBank(self):
        return self.bank
    def buyProperty(self, property):
        origbankname = self.bank
        self.bank = self.bank - property.sellprice
        if self.bank <= 0:
            print("You don't have enough money to buy this!")
            return origbankname
        else:
            property.Buy(self)
            self.owned = self.owned + property
            print("{}, you have successfully bought {}. You have ${} left in the bank.".format(self.name, property,
                                                                                               self.bank))
            return self.bank
    def buyHouses(self, property, numbought):
        origbankname = self.bank
        self.bank=self.bank - (property.houseprice * numbought)
        if property.monopoly == False:
            print("Houses can only be bought on a monopoly.")
            return origbankname
        elif property.owner != self:
            print("You're not the owner of this property!")
            return origbankname
        elif self.bank <= 0:
            print("You don't have enough money to buy this!")
            return origbankname
        else:
            property.BuyHouses(numbought)
            print("{}, you have successfully bought {} houses on {}. You now have {} houses there. "
                  "You have ${} left in the bank."
                  .format(self.name, numbought, property, property.howmanyhouses, self.bank))
            return self.bank
    def getTaxed(self, tax):
        self.bank=self.bank - tax.ChargeTax()
        if self.bank <= 0:
            self.goBankrupt()
        return self.bank
    def payRent(self, property):
        self.bank = self.bank - property.ChargeRent()
        oplayer=property.owner
        oplayer.bank = oplayer.bank + property.ChargeRent()
        if self.bank <= 0:
            self.goBankrupt()
        return self.bank, oplayer.bank
    def collectGo(self):
        self.bank = self.bank + 200
        return self.bank
    def mortgageProperty(self, property):
        if property.owner != self:
            print("{}, you don't own this property, so you can't mortgage it!".format(self.name))
            return self.bank
        mamount = property.Mortgage()
        self.bank = self.bank + mamount
        return self.bank
    def sellHouses(self, property, numhouses):
        if property.owner != self:
            print("Can't sell houses on properties that aren't yours!")
            return self.bank
        elif property.monopoly == False:
            print("Can't sell houses on something that's not a monopoly!")
            return self.bank
        samount = property.SellHouses(numhouses)
        self.bank = self.bank + samount
        print("{}, you sold {} houses, which added ${} to your bank account.".format(self.name, numhouses, samount))
        return self.bank
class Tiles:
    #properties
    def __init__(self,name):
        #changeables
        self.owned = False
        self.canbeowned = False
        self.hasprice = False
        self.haspieces = False
        self.name =name
    def isOwned(self):
        return self.owned
    def isCanbeOwned(self):
        return self.canbeowned
    def isHasPrice(self):
        return self.hasprice
    def isHasPieces(self):
        return self.haspieces
    def __str__(self):
        print(self.name)

    #methods
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        self.playerson = player1, player2, player3, player4

    def Leave(self, player1, player2=None, player3=None, player4=None):
        self.playerson = self.playerson - player1, player2, player3, player4
        if self.playerson == None:
            self.haspieces = False
class Locations(Tiles):

    #properties
    def __init__(self, name=None, rentprice = None, sellprice = None, mortgageprice = None, houseprice = None):
        super().__init__(name=name)
        #fixed
        self.canbeowned = True
        self.hasprice = True
        self.rentprice = rentprice
        #rent price will be a list: [1 house, 2 houses, 3 houses, 4 houses, hotel]
        self.pairs = None
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
    def getSellPrice(self):
        return self.sellprice
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
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        self.playerson = player1, player2, player3, player4

    def Leave(self, player1, player2=None, player3=None, player4=None):
        self.playerson = self.playerson - player1, player2, player3, player4
        if self.playerson == None:
            self.haspieces = False
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
            raise RuntimeError("You can't buy houses on a property with a hotel.")
        if self.mortgaged == True:
            raise RuntimeError("Can't buy houses on a mortgaged property.")
        if self.monopoly == False:
            raise RuntimeError("Can only buy houses when you've got the monopoly.")
        self.howmanyhouses = self.howmanyhouses + numhouses
        if self.howmanyhouses == 5:
            self.howmanyhouses = 0
            self.hashotel = True
        elif self.howmanyhouses > 5:
            raise RuntimeError("Can't have more than a hotel.")
    def SellHouses(self, numhouses):
        if self.hashotel == True:
            self.howmanyhouses = 5
            self.hashotel = False
        self.howmanyhouses = self.howmanyhouses-numhouses
        if numhouses > 5:
            raise RuntimeError("Can't sell more than 5 houses.")
        if self.howmanyhouses < 0:
            raise RuntimeError("Can't have less than 0 houses.")
    def ChargeRent(self):
        if self.hashotel == True:
            return self.rentprice[5]
        return self.rentprice[self.howmanyhouses]
    def AddPairs(self, in1, in2 = None, in3 = None):
        self.pairs = [in1, in2, in3]
        return self.pairs
class Utilities(Tiles):
    #properties
    def __init__(self, name = None,rentprice = None, sellprice = None, mortgageprice = None):
        super().__init__(name=name)
        #fixed
        self.canbeowned = True
        self.hasprice = True
        self.rentprice = rentprice
        self.pairs = None
        self.sellprice = sellprice
        self.mortgageprice = mortgageprice
        #changeables
        self.monopoly = False
        self.mortgaged = False
        self.owner = None
        self.playerson = None
    def __str__(self):
        print(self.name)
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
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        self.playerson = player1, player2, player3, player4

    def Leave(self, player1, player2=None, player3=None, player4=None):
        self.playerson = self.playerson - player1, player2, player3, player4
        if self.playerson == None:
            self.haspieces = False
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
        print(self.name)
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
    # methods
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        self.playerson = player1, player2, player3, player4
    def Leave(self, player1, player2=None, player3=None, player4=None):
        self.playerson = self.playerson - player1, player2, player3, player4
        if self.playerson== None:
            self.haspieces = False
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
class ChanceChest(Tiles):
    #properties
    def __init__(self, name = None, numcards = None):
        super().__init__(name=name)
        self.startingcards = numcards
        self.numcards = numcards
        self.haspieces = False
        self.playerson = None
        self.carddescriptions=None
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
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        self.playerson = player1, player2, player3, player4

    def Leave(self, player1, player2=None, player3=None, player4=None):
        self.playerson = self.playerson - player1, player2, player3, player4
        if self.playerson == None:
            self.haspieces = False
    def DrawCard(self):
        self.numcards = self.numcards - 1
        if self.numcards == 0:
            self.numcards = self.startingcards
    def AddDescriptions(self, dictionary):
        self.carddescriptions=dictionary
        return self.carddescriptions
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
    def Land(self, player1, player2=None, player3=None, player4=None):
        self.haspieces = True
        self.playerson = player1, player2, player3, player4

    def Leave(self, player1, player2=None, player3=None, player4=None):
        self.playerson = self.playerson - player1, player2, player3, player4
        if self.playerson == None:
            self.haspieces = False
    def ChargeTax(self):
        return self.taxprice

#not sure where these go yet:

#Brown
MediterraneanAvenue=Locations(name = "Mediterranean Avenue", rentprice = [2, 10, 30, 90, 160, 250],  sellprice = 60,
                              mortgageprice = 30, houseprice = 50 )
BalticAvenue=Locations(name = "Baltic Avenue",rentprice=[4, 20, 60, 180, 320], sellprice=60, mortgageprice=30, houseprice=50)
MediterraneanAvenue.AddPairs(BalticAvenue)
BalticAvenue.AddPairs(MediterraneanAvenue)
brown=[MediterraneanAvenue, BalticAvenue]

#Light Blue
OrientalAvenue=Locations(name ="Oriental Avenue",rentprice=[6, 30, 90, 270, 400, 550], sellprice=100, mortgageprice=50, houseprice=50)
VermontAvenue=Locations(name = "Vermont Avenue",rentprice=[6, 30, 90, 270, 400, 550], sellprice=100, mortgageprice=50, houseprice=50)
ConnecticutAvenue=Locations(name="Connecticut Avenue",rentprice=[8, 40, 100, 300, 450, 600], sellprice=120, mortgageprice=60, houseprice=50)
OrientalAvenue.AddPairs(VermontAvenue, ConnecticutAvenue)
VermontAvenue.AddPairs(ConnecticutAvenue, OrientalAvenue)
ConnecticutAvenue.AddPairs(OrientalAvenue, VermontAvenue)
lightblue=[OrientalAvenue, VermontAvenue, ConnecticutAvenue]

#Pink
StCharlesPlace=Locations(name ="St. Charles Place",rentprice=[10,50,150,450,625,750], sellprice=140, mortgageprice=70, houseprice=100)
StatesAvenue=Locations(name="States Avenue",rentprice=[10,50,150,450,625,750], sellprice=140, mortgageprice=70, houseprice=100)
VirginiaAvenue=Locations(name="Virginia Avenue",rentprice=[12,60,180,500,700,900], sellprice=160, mortgageprice=80, houseprice=100)
StCharlesPlace.AddPairs(StatesAvenue, VirginiaAvenue)
StatesAvenue.AddPairs(StCharlesPlace, VirginiaAvenue)
VirginiaAvenue.AddPairs(StCharlesPlace, StatesAvenue)
pink=[StCharlesPlace, StatesAvenue, VirginiaAvenue]

#Orange
StJamesPlace=Locations(name="St. James Place",rentprice=[14,70,200,550,750,950], sellprice=180, mortgageprice=90, houseprice=100)
TennesseeAvenue=Locations(name="Tennessee Avenue",rentprice=[14,70,200,550,750,950], sellprice=180, mortgageprice=90, houseprice=100)
NewYorkAvenue=Locations(name="New York Avenue",rentprice=[16,80,220,600,800,1000], sellprice=200, mortgageprice=100, houseprice=100)
StJamesPlace.AddPairs(TennesseeAvenue, NewYorkAvenue)
TennesseeAvenue.AddPairs(StJamesPlace, NewYorkAvenue)
NewYorkAvenue.AddPairs(StJamesPlace,TennesseeAvenue)
orange=[StJamesPlace, TennesseeAvenue, NewYorkAvenue]

#Red
KentuckyAvenue=Locations(name="Kentucky Avenue",rentprice= [18,90,250,700,875,1050], sellprice=220, mortgageprice=110, houseprice=150)
IndianaAvenue=Locations(name="Indiana Avenue",rentprice= [18,90,250,700,875,1050], sellprice=220, mortgageprice=110, houseprice=150)
IllinoisAvenue=Locations(name="Illinois Avenue",rentprice=[20,100,300,750,925], sellprice=240, mortgageprice=120, houseprice=150)
KentuckyAvenue.AddPairs(IndianaAvenue, IllinoisAvenue)
IndianaAvenue.AddPairs(KentuckyAvenue, IllinoisAvenue)
IllinoisAvenue.AddPairs(KentuckyAvenue, IndianaAvenue)
red=[KentuckyAvenue, IndianaAvenue, IllinoisAvenue]

#Yellow
AtlanticAvenue=Locations(name='Atlantic Avenue',rentprice=[22,110,330,800,975,1150], sellprice=260, mortgageprice=130, houseprice=150)
VetnorAvenue=Locations(name='Vetnor Avenue',rentprice=[22,110,330,800,975,1150], sellprice=260, mortgageprice=130, houseprice=150)
MarvinGardens=Locations(name='Marvin Gardens',rentprice=[24,120,360,850,1025,1200], sellprice=280, mortgageprice=140, houseprice=150)
AtlanticAvenue.AddPairs(VetnorAvenue, MarvinGardens)
VetnorAvenue.AddPairs(AtlanticAvenue, MarvinGardens)
MarvinGardens.AddPairs(AtlanticAvenue, VetnorAvenue)
yellow=[AtlanticAvenue, VetnorAvenue, MarvinGardens]

#Green
PacificAvenue=Locations(name='Pacific Avenue',rentprice=[26,130,390,900,1100,1275], sellprice=300, mortgageprice=150, houseprice=200)
NorthCarolinaAvenue=Locations(name='North Carolina Avenue',rentprice=[26,130,390,900,1100,1275], sellprice=300, mortgageprice=150, houseprice=200)
PennsylvaniaAvenue=Locations(name='Pennsylvania Avenue',rentprice=[28,150,450,1000,1200,1400], sellprice=320, mortgageprice=160, houseprice=200)
PacificAvenue.AddPairs(NorthCarolinaAvenue, PennsylvaniaAvenue)
NorthCarolinaAvenue.AddPairs(PacificAvenue, PennsylvaniaAvenue)
PennsylvaniaAvenue.AddPairs(PacificAvenue, NorthCarolinaAvenue)
green=[PacificAvenue, NorthCarolinaAvenue, PennsylvaniaAvenue]

#DarkBlue
ParkPlace=Locations(name='Park Place',rentprice=[35,175,500,1100,1300,1500], sellprice=350, mortgageprice=175, houseprice=200)
Boardwalk=Locations(name='Boardwalk',rentprice=[50,200,600,1400,1700,2000], sellprice=400, mortgageprice=200, houseprice=200)
ParkPlace.AddPairs(Boardwalk)
Boardwalk.AddPairs(ParkPlace)
darkblue=[ParkPlace, Boardwalk]

#Utilities
ElectricCompany=Utilities(name='Electric Company',sellprice=150, mortgageprice=75, rentprice=[4,10])
WaterWorks=Utilities(name='Water Works',sellprice=150, mortgageprice=75, rentprice=[4,10])
ElectricCompany.AddPairs(WaterWorks)
WaterWorks.AddPairs(ElectricCompany)
utilities=[ElectricCompany, WaterWorks]

#Railroads
ReadingRailRoad=Railroads(name='Reading Railroad',rentprice=[25,50,100,200], sellprice=200, mortgageprice=100)
PennsylvaniaRailRoad=Railroads(name='Pennsylvania Railroad',rentprice=[25,50,100,200], sellprice=200, mortgageprice=100)
BORailRoad=Railroads(name='B&O Railroad',rentprice=[25,50,100,200], sellprice=200, mortgageprice=100)
ShortLineRailRoad=Railroads(name='Short Line Railroad',rentprice=[25,50,100,200], sellprice=200, mortgageprice=100)

#Chance/ComChest

Chance=ChanceChest(name='Chance',numcards=16)
chancedict={"Advance to Go":1, "Advance to Illinois Ave":2, "Advance to St. Charles Place":3,
            "Advance to nearest Utility":4, "Advance to nearest Railroad":5, "Bank pays you $50":6,
            "Get out of Jail Free":7,"Go back 3 Spaces":8, "Go to Jail":9, "House Repairs:House-25, Hotel-100":10,
            "Poor Tax:$15":11,"Go to Reading Railroad":12, "Go to Boardwalk":13,
            "Elected Chairman of the Board: Pay each player $50":14,"Building loan matures, collect $150":15,
            "Won crossword competition, collect $100":16}
Chance.AddDescriptions(chancedict)
CommunityChest=ChanceChest(name='Community Chest',numcards=17)
chestdict={"Advance to Go":1, "Bank Error:Collect $200":2, "Doctor's Fees:Pay $50":3, "Sale of Stock:Collect $50":4,
           "Get out of Jail Free":5, "Go to Jail":6, "Grand Opera Night:Collect $50 from each player":7,
           "Holiday Fund Matures:Collect $100":8, "Income Tax Refund:Collect $20":9,
           "Bday! Collect $10 from each player":10,"Life insurance matures:Collect $100":11, "Hospital Fees:Pay $50":12,
           "School Fees:Pay $50":13,"Consultancy Fee:Collect $25":14, "Street Repairs:Pay $40/house, $115/hotel":15,
           "Second price in beauty contest:Collect $10":16, "Inherit $100":17}
CommunityChest.AddDescriptions(chestdict)

#Tax
LuxuryTax=Tax(name='Luxury Tax',taxprice=75)
IncomeTax=Tax(name='Income Tax',taxprice=200)

#Misc.
Jail=Tiles("Jail")
GotoJail=Tiles("Go To Jail")
FreeParking=Tiles("Free Parking")
Go=Tiles("Go")

classes={"mediterraneanavenue":MediterraneanAvenue, 'balticavenue':BalticAvenue, 'orientalavenue':OrientalAvenue,
         'vermontavenue':VermontAvenue, 'connecticutavenue':ConnecticutAvenue,'stcharlesplace':StCharlesPlace,
         'statesavenue':StatesAvenue, 'virginiaavenue':VirginiaAvenue,'stjamesplace':StJamesPlace,'tennesseeavenue'
         :TennesseeAvenue, 'newyorkavenue':NewYorkAvenue,'kentuckyavenue':KentuckyAvenue,'indianaavenue':IndianaAvenue,
         'illinoisavenue':IllinoisAvenue,'atlanticavenue':AtlanticAvenue,'vetnoravenue':VetnorAvenue,'marvingardens':
         MarvinGardens,'pacificavenue':PacificAvenue,'northcarolinaavenue':NorthCarolinaAvenue,'pennsylvaniaavenue':
         PennsylvaniaAvenue,'parkplace':ParkPlace,'boardwalk':Boardwalk,'electriccompany'
         :ElectricCompany,'waterworks':WaterWorks,'readingrailroad':ReadingRailRoad,'pennsylvaniarailroad'
         :PennsylvaniaRailRoad,'b&orailroad':BORailRoad,'shortlinerailroad':ShortLineRailRoad}

def givebankamount(name1, name2=None, name3=None, name4=None):
        print("{}, your bank balance is {}.".format(name1, name1.getBank()))
        print("{}, your bank balance is {}.".format(name2, name2.getBank()))
        print("{}, your bank balance is {}.".format(name3, name3.getBank()))
        print("{}, your bank balance is {}.".format(name4, name4.getBank()))

def makePlayer(shape):
    name=input("What is your name?")
    color=input("What color would you like to be?")
    t=Player(name, shape =shape, color =color)
    t.name=name
    return t

def mainGame():
    print("Welcome to Monopoly! Today you will be playing against 3 computer characters. Enjoy!")
    print("You are the turtle-shaped character.")
    player=makePlayer('turtle')
    Comp1=Player('Comp1',shape='circle',color='blue')
    Comp2=Player('Comp2',shape='square',color='red')
    Comp3=Player('Comp3',shape='arrow',color='yellow')
    comchest = turtle.Turtle()
    chance = turtle.Turtle()
    board=turtle.Screen()
    print("Gotcha. Good choice! Now we'll set up the board...")
    drawBoard(comchest, chance, player, Comp1, Comp2, Comp3, board)
    givebankamount(player, Comp1, Comp2, Comp3)
    board.mainloop()



mainGame()