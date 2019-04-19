import turtle
import random
from tile import Tiles
from tax import Tax
from chest import Chest
from locations import Locations
from railroad import Railroads
from utilities import Utilities

class Player(turtle.Turtle):
    def __init__(self, name, color, shape, number2, number4, number3=None):
        super().__init__()
        #fixed
        self.name=name
        self.color(color)
        self.shape(shape)
        self.number2=number2
        self.number4=number4
        self.number3=number3
        self.x=None
        self.y=None
        self.speed(1)
        #changeables
        self.bank=1500
        self.spaceon=Go
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
                global playerlist
                playerlist=playerlist-self
                done = True
                return
            else:
                print("Invalid input, try again")
    def isBankrupt(self):
        return self.bankrupt
    def getBank(self):
        self.bank=int(self.bank)
        return self.bank
    def buyProperty(self, property):
        origbankname = self.bank
        sellprice=property.getSellPrice()
        self.bank = self.bank - sellprice
        if self.bank <= 0:
            print("You don't have enough money to buy this!")
            self.bank=origbankname
            return self.bank
        else:
            property.Buy(self)
            self.owned.append(property)
            print("{}, you have successfully bought {}. You have ${} left in the bank.".format(self.name, property,
                                                                                               self.getBank()))
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
        print("{}, you have been taxed for {}. Your remaining balance is {}.".format(self.name, tax.ChargeTax(),
                                                                                     self.bank))
        if self.bank <= 0:
            self.goBankrupt()
        return self.bank
    def payRent(self, property):
        self.bank = self.bank - property.ChargeRent()
        oplayer=property.owner
        oplayer.bank = oplayer.bank + property.ChargeRent()
        if self.bank <= 0:
            self.goBankrupt()
        print("{}, you have paid ${} to {} for rent on {}. You have {} left in the bank.".format(self.name,
              property.ChargeRent(),oplayer.name, property, self.getBank()))
        print("{}, you now have {} in the bank.".format(oplayer.name, oplayer.getBank()))
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
    def setGo(self):
        global tile_list
        self.x=tile_list[Go][self.number4][0]
        self.y=tile_list[Go][self.number4][1]
        self.setpos(x=self.x, y=self.y)
        return
    def moveTo(self, property):
        global tile_list
        global tile_list_x_top
        global tile_list_y_left
        global tile_list_y_right
        global tile_list_x_bot
        if property in tile_list_x_bot:
            if self.number3 == None:
                self.x=tile_list_x_bot[property][self.number2]
            else:
                self.x = tile_list_x_bot[property][self.number3]
            self.y=tile_list_x_bot['y'][self.number2]
        elif property in tile_list_x_top:
            if self.number3 == None:
                self.x = tile_list_x_top[property][self.number2]
            else:
                self.x = tile_list_x_top[property][self.number3]
            self.y = tile_list_x_top['y'][self.number2]
        elif property in tile_list_y_left:
            if self.number3 == None:
                self.y = tile_list_y_left[property][self.number2]
            else:
                self.y = tile_list_y_left[property][self.number3]
            self.x=tile_list_y_left['x'][self.number2]
        elif property in tile_list_y_right:
            if self.number3 == None:
                self.y = tile_list_y_right[property][self.number2]
            else:
                self.y = tile_list_y_right[property][self.number3]
            self.x=tile_list_y_right['x'][self.number2]
        else:
            self.x=tile_list[property][self.number4][0]
            self.y=tile_list[property][self.number4][1]
        self.setpos(x=self.x, y=self.y)
        oldspace=self.spaceon
        oldspace.Leave(self)
        self.spaceon=property
        property.Land(self)
        return
    def rollDice(self):
        global tl
        done = False
        while not done:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            dicesum = dice1 + dice2
            print("{}, you rolled a {} and a {}.".format(self.name, dice1, dice2))
            on = self.spaceon
            oldpos = tl.index(on)
            newpos = oldpos + dicesum
            if newpos > len(tl):
                print("{} passed Go.".format(self.name))
                self.collectGo()
            newpos = newpos % len(tl)
            nowon = tl[newpos]
            self.moveTo(nowon)
            self.spaceon = nowon
            land = self.spaceon
            if land.canbeowned == True:
                buyProperty(self, land)
            elif land.canbeowned == False:
                unownedProperty(self, land)
            if dice1 == dice2:
                print("{}, you rolled doubles! Now you get to roll again!".format(self.name))
            else:
                done = True
        return
class Chance(Tiles):
    # properties
    startchancelist = {"Advance to Go":'Go', "Advance to Illinois Ave":'Illinois Avenue',
                       "Advance to St. Charles Place":'St. Charles Place',
                       "Advance to a random Utility":1, "Advance to a random Railroad":2, "Bank pays you $50":3,
                       "Get out of Jail Free":4, "Go back 3 Spaces":5, "Go to Jail":'Jail',
                       "House Repairs:House-25, Hotel-100":6,
                       "Poor Tax:$15":6, "Go to Reading Railroad":'Reading RailRoad', "Go to Boardwalk":'Boardwalk',
                       "Elected Chairman of the Board: Pay each player $50":7,
                       "Building loan matures, collect $150":8,
                       "Won crossword competition, collect $100":9}
    chancelist = {"Advance to Go":'Go', "Advance to Illinois Ave":'Illinois Avenue',
                       "Advance to St. Charles Place":'St. Charles Place',
                       "Advance to a random Utility":1, "Advance to a random Railroad":2, "Bank pays you $50":3,
                       "Get out of Jail Free":4, "Go back 3 Spaces":5, "Go to Jail":'Jail',
                       "House Repairs:House-25, Hotel-100":6,
                       "Poor Tax:$15":6, "Go to Reading Railroad":'Reading RailRoad', "Go to Boardwalk":'Boardwalk',
                       "Elected Chairman of the Board: Pay each player $50":7,
                       "Building loan matures, collect $150":8,
                       "Won crossword competition, collect $100":9}

    def __init__(self, name=None, numcards=None):
        super().__init__(name=name)
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

    # methods
    def DrawCard(self, player):
        global chancelist
        global startchancelist
        global utilities
        global railroads
        global classes
        self.numcards = self.numcards - 1
        if self.numcards == 0:
            self.numcards = self.startingcards
            chancelist = startchancelist
        drawn = random.choice(chancelist)
        print("{}, you drew {}.".format(player.name, drawn))
        del chancelist[drawn]
        if drawn == 'Advance to Go':
            go = classes[chancelist[drawn]]
            player.moveTo(go)
            player.collectGo()
        elif drawn =='Advance to Illinois Avenue' or drawn == "Advance to St. Charles Place" or drawn == "Go to Reading Railroad" or drawn == "Go to Boardwalk":
            prop=classes[chancelist[drawn]]
            player.moveTo(prop)
            buyProperty(player, prop)
        elif drawn == 'Advance to a random Utility':
            utility=random.choice(utilities)




def getPos(x, y):
    print("(",x , y,")")
    return
def drawBoard(comchest, chance, player, comp1, comp2, comp3, board):
    global tile_list
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
    player.speed(0)
    player.setGo()
    player.speed(1)
    comp1.penup()
    comp1.speed(0)
    comp1.setGo()
    comp1.speed(1)
    comp2.penup()
    comp2.speed(0)
    comp2.setGo()
    comp2.speed(1)
    comp3.penup()
    comp3.speed(0)
    comp3.setGo()
    comp3.speed(1)
    #coord testing (will be removed eventually)
    #board.onscreenclick(getPos)
    #board.mainloop()
def givebankamount(playerlist):
    for n in playerlist:
        print("{}, your bank balance is {}.".format(n, n.getBank()))
def buyProperty(play, land):
    if land.owned == False:
        done = False
        while not done:
            buy = input("{}, would you like to buy {}? Enter Y for yes, N for no.".format(play.name, land.name))
            if buy == 'Y' or buy == 'y':
                play.buyProperty(land)
                land.Buy(play)
                done = True
            elif buy == 'N' or buy == 'n':
                print("{}, you did not buy {}.".format(play.name, land.name))
                done = True
            else:
                print("Invalid input, try again.")
    elif land.owned == True:
        play.payRent(land)
def unownedProperty(play, land):
    if land.name == 'Chance':
        0
    elif land.name == 'Community Chest':
        0
    elif land.name == 'Luxury Tax' or land.name == 'Income Tax':
        play.getTaxed(land)
    elif land.name == 'Jail':
        0
    elif land.name == 'Just Visiting':
        0
    elif land.name == 'Go To Jail':
        0
    elif land.name == 'Free Parking':
        print("{}, you landed on Free Parking! You get $100!".format(play.name))
        play.addBank(100)
    elif land.name == 'Go':
        print("{}, you landed on Go! You get $200!".format(play.name))
        play.collectGo()
def makePlayer(shape):
    global tile_list
    name = 'Chloe'
    # input("What is your name?")
    color = 'black'
    # input("What color would you like to be?")
    t = Player(name, shape=shape, color=color, number2=0, number4=0)
    t.name = name
    return t
def findWinner(playerlist):
    currentw=0
    for player in playerlist:
        if player.bank > currentw:
            currentw=player.bank
    return currentw
def playTurn(playerlist,bestplayer):
    done = False
    while not done:
        for play in playerlist:
            play.rollDice()
        if bestplayer.bankrupt == True:
            done = True
            return
        if playerlist == [bestplayer]:
            done = True
            return



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
railroads=[ReadingRailRoad, PennsylvaniaRailRoad, BORailRoad, ShortLineRailRoad]
#Chance/ComChest

Chance1=Chance(name='Chance',numcards=16)
Chance2=Chance(name='Chance', numcards=16)
Chance3=Chance(name='Chance', numcards=16)

CommunityChest1=Chest(name='Community Chest',numcards=17)
CommunityChest2=Chest(name='Community Chest',numcards=17)
CommunityChest3=Chest(name='Community Chest',numcards=17)


#Tax
LuxuryTax=Tax(name='Luxury Tax',taxprice=75)
IncomeTax=Tax(name='Income Tax',taxprice=200)

#Misc.
Jail=Tiles("Jail")
JustVisiting=Tiles("Just Visiting")
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

tile_list={MediterraneanAvenue:[210, 240], CommunityChest1:[155, 185], BalticAvenue:[95, 130], IncomeTax:[40, 70],
           ReadingRailRoad:[-20, 20], OrientalAvenue:[-70, -40], Chance1:[-130, -100], VermontAvenue:[-190, -150],
           ConnecticutAvenue:[-250, -210], JustVisiting:[[-338, -270], [-338, -302], [-338, -332], [-293, -332]],
           Jail:[[-312, -271], [-271, -271], [-312, -312], [-271, -312]],
           StCharlesPlace:[[-291, -210], [-291, -240], [-335, -211], [-335, -238]], ElectricCompany:[-155, -185],
           StatesAvenue:[-95, -126], VirginiaAvenue:[-38, -72],PennsylvaniaRailRoad:[21, -13], StJamesPlace:[73, 44],
           CommunityChest2:[140, 100], TennesseeAvenue:[190, 150], NewYorkAvenue:[250, 210], FreeParking:[344, 301],
           KentuckyAvenue:[-205, -245], Chance2:[-150, -190], IndianaAvenue:[-94, -130], IllinoisAvenue:[-35, -70],
           BORailRoad:[17, -17], AtlanticAvenue:[70, 30], VetnorAvenue:[136, 95], WaterWorks:[190, 150],
           MarvinGardens:[245, 204], GotoJail:[334, 295], PacificAvenue:[245, 212], NorthCarolinaAvenue:[185, 155],
           CommunityChest3:[97, 132],PennsylvaniaAvenue:[30, 77], ShortLineRailRoad:[-20, 15], Chance3:[-76, -36],
           ParkPlace:[-130, -95], LuxuryTax:[-185, -155], Boardwalk:[-244, -208],
           Go:[[271, -293], [322, -293], [268, -320], [326, -320]]}

tl=[Go, MediterraneanAvenue, CommunityChest1, BalticAvenue, IncomeTax, ReadingRailRoad, OrientalAvenue,
                  Chance1, VermontAvenue, ConnecticutAvenue, JustVisiting, StCharlesPlace, ElectricCompany, StatesAvenue,
                  VirginiaAvenue, PennsylvaniaRailRoad, StJamesPlace, CommunityChest2, TennesseeAvenue, NewYorkAvenue,
                  FreeParking, KentuckyAvenue, Chance2, IndianaAvenue, IllinoisAvenue, BORailRoad, AtlanticAvenue,
                  VetnorAvenue, WaterWorks, MarvinGardens, GotoJail, PacificAvenue, NorthCarolinaAvenue,
                  CommunityChest3, PennsylvaniaAvenue, ShortLineRailRoad, Chance3, ParkPlace, LuxuryTax, Boardwalk]

tile_list_x_bot={'y':[-293, -320],MediterraneanAvenue:[210, 240], CommunityChest1:[155, 185], BalticAvenue:[95, 130],
           IncomeTax:[40, 70],ReadingRailRoad:[-20, 20], OrientalAvenue:[-70, -40], Chance1:[-130, -100],
           VermontAvenue:[-190, -150],ConnecticutAvenue:[-250, -210]}

tile_list_x_top={'y':[301, 334],KentuckyAvenue:[-205, -245], Chance2:[-150, -190], IndianaAvenue:[-94, -130],
           IllinoisAvenue:[-35, -70],BORailRoad:[17, -17], AtlanticAvenue:[70, 30], VetnorAvenue:[136, 95],
           WaterWorks:[190, 150], MarvinGardens:[245, 204], GotoJail:[334, 295]}

tile_list_y_left={'x':[-291, -335], ElectricCompany:[-155, -185],StatesAvenue:[-95, -126], VirginiaAvenue:[-38, -72],
           PennsylvaniaRailRoad:[21, -13], StJamesPlace:[73, 44],CommunityChest2:[140, 100], TennesseeAvenue:[190, 150],
           NewYorkAvenue:[250, 210], FreeParking:[344, 301]}

tile_list_y_right={'x':[295, 334], PacificAvenue:[245, 212], NorthCarolinaAvenue:[185, 155],
           CommunityChest3:[97, 132],PennsylvaniaAvenue:[30, 77], ShortLineRailRoad:[-20, 15], Chance3:[-76, -36],
           ParkPlace:[-130, -95], LuxuryTax:[-185, -155], Boardwalk:[-244, -208]}



def mainGame():
    print("Welcome to Monopoly! Today you will be playing against 3 computer characters. Enjoy!")
    print("You are the turtle-shaped character.")
    player=makePlayer('turtle')
    Comp1 = Player('Comp1', shape='circle', color='blue', number2=0, number3=1, number4=1)
    Comp2 = Player('Comp2', shape='square', color='red', number2=1, number4=2)
    Comp3 = Player('Comp3', shape='arrow', color='yellow', number2=1, number3=0, number4=3)
    playerlist=[player, Comp1, Comp2, Comp3]
    comchest = turtle.Turtle()
    chance = turtle.Turtle()
    board=turtle.Screen()
    Go.playerson=playerlist
    print("Gotcha. Good choice! Now we'll set up the board...")
    drawBoard(comchest, chance, player, Comp1, Comp2, Comp3, board)
    print("Let's start playing! Have fun!")
    givebankamount(playerlist)
    playTurn(playerlist, player)
    winner=findWinner(playerlist)
    print("Congrats {}, you have won the game!".format(winner))
    print("These were the ending bank balances:{}".format(givebankamount(playerlist)))
    board.mainloop()





mainGame()