import turtle
import random
from tile import Tiles
from tax import Tax
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
        self.otherplayers=[]
        self.x=None
        self.y=None
        self.speed(1)
        #changeables
        self.bank=1500
        self.spaceon=Go
        self.injail=False
        self.turnsinjail = 0
        self.owned=[]
        self.monopolies=[]
        self.hasmonopoly=False
        self.houses=0
        self.hotels=0
        self.bankrupt=False
        self.hasfreejail=False

    def __str__(self):
        return self.name
    def addPlayers(self, player1, player2=None, player3=None):
        posslist=[player1, player2, player3]
        reallist=[]
        for p in posslist:
            if p is not None:
                reallist.append(p)
        self.otherplayers=reallist
        return reallist
    def addBank(self, amount):
        self.bank=self.bank+amount
        return self.bank
    def subBank(self, amount):
        self.bank=self.bank-amount
        if self.bank <= 0:
            self.goBankrupt()
        return self.bank
    def goBankrupt(self):
        print("GO BANKRUPT IS BEING CALLED")
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
        self.bank=int(self.bank)
        return self.bank
    def getOwned(self):
        thislist=[]
        for owned in self.owned:
            thislist.append(owned.name)
        return thislist
    def buyProperty(self, property):
        global owned_dict
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
            self.stampowned(property)
            print("{}, you have successfully bought {}. You have ${} left in the bank.".format(self.name, property,
                                                                                               self.getBank()))
            return self.bank
    def stampowned(self,property):
        nowon = self.spaceon
        stampplace = owned_dict[property][0]
        self.speed(0)
        self.setpos(stampplace)
        self.stamp()
        self.moveTo(nowon)
        self.speed(1)
        return
    def buyHouses(self, property, numbought):
        if type(numbought) != int:
            print("Number of houses bought is not an integer!")
            return
        origbankname = self.bank
        self.bank=self.bank - (property.houseprice * numbought)
        if property.monopoly == False:
            print("Houses can only be bought on a monopoly.")
            self.bank=origbankname
            return self.bank
        elif property.owner != self:
            print("You're not the owner of this property!")
            self.bank=origbankname
            return self.bank
        elif self.bank <= 0:
            print("You don't have enough money to buy this!")
            self.bank=origbankname
            return self.bank
        else:
            if property.BuyHouses(numbought) == None:
                return
            if property.hashotel is True:
                print("{}, you have successfully bought {} houses on {}. You now have a hotel there."
                      "You have ${} left in the bank."
                      .format(self.name, numbought, property, self.bank))
            else:
                print("{}, you have successfully bought {} houses on {}. You now have {} houses there. "
                  "You have ${} left in the bank."
                  .format(self.name, numbought, property, property.howmanyhouses, self.bank))
            if property.hashotel is True:
                self.houses = self.houses + numbought - 1
                self.hotels = self.hotels + 1
            else:
                self.houses=self.houses + numbought
            return self.bank
    def getTaxed(self, tax):
        self.bank=self.bank - tax.ChargeTax()
        print("{}, you have been taxed for {}. Your remaining balance is {}.".format(self.name, tax.ChargeTax(),
                                                                                     self.bank))
        if self.bank <= 0:
            self.goBankrupt()
        return self.bank
    def payRent(self, property):
        if property.owner is self:
            return
        if isinstance(property, Railroads):
            numowned = 0
            owner=property.owner
            for prop in owner.owned:
                if isinstance(prop, Railroads):
                    numowned=numowned + 1
            print('numowned =', numowned)
            rent=property.ChargeRent(numowned)
            print('rent = ', rent)
        else:
            rent=property.ChargeRent()
        self.bank = self.bank - rent
        oplayer=property.owner
        oplayer.bank = oplayer.bank + rent
        if self.bank <= 0:
            self.goBankrupt()
        print("{}, you have paid ${} to {} for rent on {}. You have {} left in the bank.".format(self.name,
              rent,oplayer.name, property, self.getBank()))
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
        if property.howmanyhouses + numhouses == 5:
            self.hotels = self.hotels - 1
        self.houses = self.houses - numhouses
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
        donend = False
        while not donend:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            jailcount = 0
            dicesum = dice1 + dice2
            print("{}, you rolled a {} and a {}.".format(self.name, dice1, dice2))
            on = self.spaceon
            oldpos=0
            if self.injail is False:
                oldpos = tl.index(on)
            elif self.injail is True:
                oldpos = 10
            newpos = oldpos + dicesum
            if newpos > len(tl):
                print("{} passed Go.".format(self.name))
                self.collectGo()
            newpos = newpos % len(tl)
            nowon = tl[newpos]
            if self.injail is True:
                if dice1 == dice2:
                    print("{}, you've rolled doubles and now get to get out of jail!".format(self.name))
                    self.injail=False
                    self.turnsinjail=0
                    self.moveTo(nowon)
                    if nowon.canbeowned is True:
                        buyProperty(self,nowon)
                    elif nowon.canbeowned is False:
                        unownedProperty(self, nowon)
                    donend = True
                    return 'out of jail'
                return 'still in jail'
            self.moveTo(nowon)
            land = self.spaceon
            if land.canbeowned == True:
                buyProperty(self, land)
            elif land.canbeowned == False:
                unownedProperty(self, land)
            if dice1 == dice2:
                print("{}, you rolled doubles! Now you get to roll again!".format(self.name))
                jailcount = jailcount + 1
                if jailcount == 3:
                    print("{}, you've rolled doubles three times, and now you're going to jail!".format(self.name))
                    donend = True
                    return 'wenttojail'
            else:
                donend = True
        return 'safe'

class Chance(Tiles):
    def __init__(self, name=None, numcards=None):
        super().__init__(name=name)
        self.startingcards = numcards
        self.numcards = numcards
        self.haspieces = False
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
        global tl
        self.numcards = self.numcards - 1
        if self.numcards == 0:
            self.numcards = self.startingcards
            chancelist = startchancelist
        drawn = random.choice(list(chancelist.keys()))
        print("{}, you drew {}.".format(player.name, drawn))
        if drawn == "Advance to Go":
            name=chancelist[drawn]
            for t in tl:
                if t.name == name:
                    go = t
                    player.moveTo(go)

            player.collectGo()
        elif drawn =="Advance to Illinois Avenue" or drawn == "Advance to St. Charles Place" or\
                drawn == "Go to Reading Railroad" or drawn == "Go to Boardwalk":
            name=chancelist[drawn]
            for t in tl:
                if t.name == name:
                    prop = t
                    player.moveTo(prop)
                    buyProperty(player, prop)
        elif drawn == "Advance to a random Utility":
            utility=random.choice(utilities)
            player.moveTo(utility)
            buyProperty(player, utility)
        elif drawn == "Advance to a random Railroad":
            railroad=random.choice(railroads)
            player.moveTo(railroad)
            buyProperty(player, railroad)
        elif drawn == "Bank pays you $50":
            player.addBank(50)
        elif drawn == "Get out of Jail Free":
            player.hasfreejail=True
        elif drawn == "Go back 3 Spaces":
            nowon=player.spaceon
            place=tl.index(nowon)
            newplace=place-3
            nownowon=tl[newplace]
            player.moveTo(nownowon)
        elif drawn == "Go to Jail":
            goToJail(player)
        elif drawn == "House Repairs:House-25, Hotel-100":
            house = player.houses * 25
            hotel = player.hotels * 100
            total = house + hotel
            print("{}, you have to pay {} for house repairs.".format(player.name, total))
            player.subBank(total)
            print("{}, you have {} left in the bank.".format(player.name, player.bank))
        elif drawn == "Poor Tax:$15":
            player.subBank(15)
        elif drawn == "Elected Chairman of the Board: Pay each player $50":
            total = 0
            for comp in player.otherplayers:
                comp.addBank(50)
                total = total + 50
            player.subBank(total)
        elif drawn == "Building loan matures, collect $150":
            player.addBank(150)
        elif drawn == "Won crossword competition, collect $100":
            player.addBank(100)
        del chancelist[drawn]
        return
class Chest(Tiles):
    def __init__(self, name=None, numcards=None):
        super().__init__(name=name)
        self.startingcards = numcards
        self.numcards = numcards
        self.haspieces = False
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
        global chestdict
        global startchestdict
        global utilities
        global railroads
        global tl
        self.numcards = self.numcards - 1
        if self.numcards == 0:
            self.numcards = self.startingcards
            chestdict = startchestdict
        drawn = random.choice(list(chestdict.keys()))
        print("{}, you drew {}.".format(player.name, drawn))
        del chestdict[drawn]
        if drawn == "Advance to Go":
            name=chancelist[drawn]
            for t in tl:
                if t.name == name:
                    go=t
                    player.moveTo(go)
                    player.collectGo()
        elif drawn == "Bank Error:Collect $200":
            player.addBank(200)
        elif drawn == "Doctor's Fees:Pay $50" or drawn == "Hospital Fees:Pay $50" or drawn == "School Fees:Pay $50":
            player.subBank(50)
        elif drawn == "Sale of Stock:Collect $50":
            player.addBank(50)
        elif drawn == "Get out of Jail Free":
            player.hasfreejail=True
        elif drawn == "Go to Jail":
            goToJail(player)
        elif drawn == "Grand Opera Night:Collect $50 from each player":
            total = 0
            for comp in player.otherplayers:
                comp.subBank(50)
                total = total + 50
            player.addBank(total)
        elif drawn == "Holiday Fund Matures:Collect $100":
            player.addBank(100)
        elif drawn == "Income Tax Refund:Collect $20":
            player.addBank(20)
        elif drawn == "Bday! Collect $10 from each player":
            total = 0
            for comp in player.otherplayers:
                comp.subBank(10)
                total = total + 10
            player.addBank(10)
        elif drawn == "Life insurance matures:Collect $100":
            player.addBank(100)
        elif drawn == "Consultancy Fee:Collect $25":
            player.addBank(25)
        elif drawn == "Street Repairs:Pay $40/house, $115/hotel":
            house = player.houses * 40
            hotel = player.hotels * 115
            total = house + hotel
            print("{}, you have to pay {} for house repairs.".format(player.name, total))
            player.subBank(total)
            print("{}, you have {} left in the bank.".format(player.name, player.bank))
        elif drawn == "Second price in beauty contest:Collect $10":
            player.addBank(10)
            print("You look so beautiful!")
        elif drawn == "Inherit $100":
            player.addBank(100)
        return

class Locations(Tiles):

    #properties
    def __init__(self, name=None, rentprice = None, sellprice = None, mortgageprice = None, houseprice = None):
        super().__init__(name=name)
        #fixed
        self.canbeowned = True
        self.hasprice = True
        self.rentprice = rentprice
        self.islocation = True
        self.h1=turtle.Turtle()
        self.h2=turtle.Turtle()
        self.h3=turtle.Turtle()
        self.h4=turtle.Turtle()
        self.hot=turtle.Turtle()
        self.houselist=[self.h1, self.h2, self.h3, self.h4]
        for h in self.houselist:
            h.color('lightgreen')
            h.turtlesize(.5, .5, .5)
            h.shape('square')
            h.speed(0)
            h.penup()
        self.hot.color('firebrick')
        self.hot.turtlesize(.5, 1, .5)
        self.hot.shape('square')
        self.hot.penup()
        self.hot.speed(0)
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
    def setHouses(self):
        global owned_dict
        pos = 1
        for h in self.houselist:
            h.ht()
            h.setpos(owned_dict[self][pos])
            pos = pos+1
        self.hot.ht()
        self.hot.setpos(owned_dict[self][2])
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
        print ("number of houses:",self.howmanyhouses)
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
        copylist=self.houselist[:self.howmanyhouses]
        for h in copylist:
            h.st()
        if self.howmanyhouses == 5:
            for h in self.houselist:
                h.ht()
            self.howmanyhouses = 0
            self.hashotel = True
            self.hot.st()
        elif self.howmanyhouses > 5:
            print("Can't have more than a hotel.")
            print (self.howmanyhouses)
            return
        return 'not none'
    def SellHouses(self, numhouses):
        orig = self.howmanyhouses
        if self.hashotel == True:
            self.howmanyhouses = 5
            self.hashotel = False
            self.hot.ht()
        self.howmanyhouses = self.howmanyhouses-numhouses
        if numhouses > 5:
            print("Can't sell more than 5 houses.")
            self.howmanyhouses = orig
            return 0
        if self.howmanyhouses < 0:
            print("Can't have less than 0 houses.")
            self.howmanyhouses = orig
            return 0
        amount = numhouses * self.houseprice
        copylist = self.houselist[:self.howmanyhouses]
        for h in copylist:
            h.ht()
        return amount
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

def trade(play, playerlist):
    global tl
    copy=playerlist.copy()
    copy.remove(play)
    copystr=[]
    for c in copy:
        copystr.append(c.name)
    done = False
    while not done:
        trade=input("{}, would you like to trade with someone? Enter Y or N.".format(play.name))
        if trade == 'Y' or trade == 'y':
            who=input("Who would you like to trade with? Pick one: {}.".format(copystr))
            if who not in copystr:
                print("Invalid input.")
                continue
            for other in copy:
                if who == other.name:
                    otherprop=other.getOwned()
                    buy = input("What property of theirs would you like to trade for? {}".format(otherprop))
                    if buy not in otherprop:
                        print("Invalid input.")
                        continue
                    for prop in tl:
                        if prop.name==buy:
                            buy=prop
                    monprop=input("Would you like to offer money or a property for this trade?")
                    if monprop == 'Money' or monprop == 'money':
                        sell=input("How much money would you like to offer?")
                        try:
                            sell = int(sell)
                        except ValueError:
                            print("Invalid input; not an integer.")
                            continue
                        if play.bank-sell <=0:
                            print("You don't have enough money to offer this amount.")
                            continue
                    elif monprop == 'Property' or monprop == 'property':
                        powned=play.getOwned()
                        sell = input("What property of yours would you like to trade for {}? You own {}"
                                     .format(buy, powned))
                        if sell not in powned:
                            print("Invalid input.")
                            continue
                        for prop in tl:
                            if prop.name==sell:
                                sell=prop
                    else:
                        print("Invalid input.")
                        continue
                    print("{}, you'd like to trade with {}. You're offering {} for {}."
                          .format(play.name, other.name, sell, buy))
                    confirm=input("{}, would you like to participate in this trade? Enter Y or N.".format(other.name))
                    if confirm == 'Y' or confirm == 'y':
                        print("Trade complete! {} traded with {} for {}.".format(play.name, other.name, buy))
                        if type(sell) == int:
                            play.subBank(sell)
                            other.addBank(sell)
                            buy.Sell()
                            buy.Buy(play)
                            play.owned.append(buy)
                            other.owned.remove(buy)
                        elif sell in tl:
                            buy.Sell()
                            buy.Buy(play)
                            sell.Sell()
                            sell.Buy(other)
                            play.owned.append(buy)
                            play.owned.remove(sell)
                            other.owned.remove(buy)
                            other.owned.append(sell)
                            other.stampowned(sell)
                        play.stampowned(buy)
                        if buy.monopoly is True:
                            buy.monopoly = False
                            for n in buy.pairs:
                                n.monopoly = False

                        truelist = []
                        for n in range(0, len(buy.pairs)):
                            if buy.pairs[n] in play.owned:
                                truelist.append('t')
                            else:
                                truelist.append('f')
                        if 'f' not in truelist:
                            print(
                                "{}, you now have a monopoly on the section you just bought. You may now build houses on "
                                "those properties.".format(play.name))
                            play.hasmonopoly=True
                            buy.monopoly = True
                            monolist = [buy.name]
                            for mono in buy.pairs:
                                mono.monopoly = True
                                monolist.append(mono.name)
                            play.monopolies.append(monolist)

                        continue
                    elif confirm == 'N' or confirm == 'n':
                        print("The trade was not completed.")
                        continue
                    else:
                        print("Invalid input.")
                        continue
        elif trade == 'N' or trade == 'n':
            print("Decided not to trade.")
            done=True
        else:
            print("Invalid input.")
            continue
    return
def monoQuestions(play):
    global tl
    if play.hasmonopoly==True:
        done = False
        while not done:
            buyhouses = input("{}, would you like to buy houses on a monopoly? Enter Y or N.".format(play.name))
            if buyhouses == 'Y' or buyhouses == 'y':
                where=input('Where would you like to buy houses? Here are your options: {}'.format(play.monopolies))
                testlist=[]
                for n in play.monopolies:
                    if where in n:
                        testlist.append('t')
                if 't' not in testlist:
                    print("Invalid input.")
                    continue
                for prop in tl:
                    if prop.name == where:
                        where = prop
                num=input("How many houses would you like to buy?")
                try:
                    num = int(num)
                except ValueError:
                    print("Invalid input; not an integer")
                    continue
                try:
                    play.buyHouses(property=where, numbought=num)
                except AttributeError:
                    print("You can't buy houses on this property!")
                    continue
                fini=input("Are you finished buying houses? Enter Y if finished.")
                if fini == 'Y' or fini == 'y':
                    done = True
            elif buyhouses == 'N' or buyhouses == 'n':
                print("Decided not to buy houses.")
                done=True
            else:
                print("Invalid input.")

        end = False
        while not end:
            sellhouses = input("{}, would you like to sell houses on a monopoly? Enter Y or N.".format(play.name))
            if sellhouses == 'Y' or sellhouses == 'y':
                where = input('Where would you like to sell houses? Here are your options: {}'.format(play.monopolies))
                if where not in play.monopolies:
                    print("Invalid input.")
                    continue
                for prop in tl:
                    if prop.name == where:
                        where = prop
                num = input("How many houses would you like to sell?")
                try:
                    num = int(num)
                except ValueError:
                    print("Invalid input; not an integer")
                    continue
                try:
                    play.sellHouses(property=where, numhouses=num)
                except AttributeError:
                    print("You can't sell houses on this property!")
                    continue
                fini = input("Are you finished selling houses? Enter Y if finished.")
                if fini == 'Y' or fini == 'y':
                    end = True
            elif sellhouses == 'N' or sellhouses == 'n':
                print("Decided not to sell houses.")
                end = True
            else:
                print("Invalid input.")
    return
def getPos(x, y):
    print("(",x , y,")")
    return
def drawBoard(comchest, chance, playerlist, board, property_list):
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
    for player in playerlist:
        player.penup()
        player.speed(0)
        player.setGo()
        player.speed(1)
    # set houses
    for p in property_list:
        if p.islocation is True:
            p.setHouses()
    return
    #coord testing (will be removed eventually)
    board.onscreenclick(getPos)
    board.mainloop()
def givebankamount(playerlist):
    for n in playerlist:
        bank=n.getBank()
        statement = ("{}, your bank balance is {}.".format(n, bank))
        return statement
def giveowned(playerlist):
    for p in playerlist:
        owned=p.getOwned()
        print("{} owns the following:{}".format(p.name, owned))
    return
def buyProperty(play, land):
    if land.owned == False:
        done = False
        while not done:
            buy = input("{}, would you like to buy {}? It costs {}. Enter Y for yes, N for no.".format(play.name, land.name, land.sellprice))
            if buy == 'Y' or buy == 'y':
                play.buyProperty(land)
                land.Buy(play)
                truelist=[]
                for n in range(0, len(land.pairs)):
                    if land.pairs[n] in play.owned:
                        truelist.append('t')
                    else:
                        truelist.append('f')
                if 'f' not in truelist:
                    print("{}, you now have a monopoly on the section you just bought. You may now build houses on "
                          "those properties.".format(play.name))
                    play.hasmonopoly=True
                    land.monopoly = True
                    monolist=[land.name]
                    for mono in land.pairs:
                        mono.monopoly = True
                        monolist.append(mono.name)
                    play.monopolies.append(monolist)
                done = True
                return
            elif buy == 'N' or buy == 'n':
                print("{}, you did not buy {}.".format(play.name, land.name))
                done = True
                return
            else:
                print("Invalid input, try again.")
    elif land.owned == True:
        play.payRent(land)
        return
def unownedProperty(play, land):
    if land.name == 'Chance':
        try:
            land.DrawCard(play)
        except:
            print("ERROR")
    elif land.name == 'Community Chest':
        try:
            land.DrawCard(play)
        except:
            print("ERROR")
    elif land.name == 'Luxury Tax' or land.name == 'Income Tax':
        play.getTaxed(land)
        return
    elif land.name == 'Just Visiting':
        pass
    elif land.name == 'Go To Jail':
        goToJail(play)
    elif land.name == 'Free Parking':
        print("{}, you landed on Free Parking! You get $100!".format(play.name))
        play.addBank(100)
    elif land.name == 'Go':
        global playerlist
        print("PLAYERLIST BEFORE LANDED:",playerlist)
        print("{}, you landed on Go! You get $200!".format(play.name))
        print("PLAYERLIST AFTER LANDED:", playerlist)
        play.collectGo()
        print("PLAYERLIST AFTER COLLECTGO:", playerlist)
    return
def makePlayer():
    players=int(input("Enter the # of players up to 4."))
    playerlist=[]
    done = False
    while not done:
        if players > 4 or players <= 0:
            print("Invalid input, try again")
        for p in range(1, players+1):
            name = input("What's your name?")
            color = input("What color would you like to be?")
            shape = input("What shape would you like to be? Pick from circle, turtle, square, or arrow.")
            if p == 1:
                n2 = 0
                n4 = 0
                n3=None
                a = Player(name=name, shape=shape, color=color, number2=n2, number4=n4, number3=n3)
                a.name = name
                playerlist.append(a)
                done=True
            else:
                a = None
            if p == 2:
                n2 = 0
                n3 = 1
                n4 = 1
                t = Player(name=name, shape=shape, color=color, number2=n2, number4=n4, number3=n3)
                t.name = name
                playerlist.append(t)
                done=True
            else:
                t = None
            if p == 3:
                n2=1
                n3=None
                n4=2
                b = Player(name=name, shape=shape, color=color, number2=n2, number4=n4, number3=n3)
                b.name = name
                playerlist.append(b)
                done=True
            else:
                b=None
            if p == 4:
                n2=1
                n3=0
                n4=3
                c = Player(name=name, shape=shape, color=color, number2=n2, number4=n4, number3=n3)
                c.name = name
                playerlist.append(c)
                done=True
            else:
                c=None
            if a is not None:
                a.addPlayers(player1=b, player2=c, player3=t)
            if b is not None:
                b.addPlayers(player1=a, player2=c, player3=t)
            if c is not None:
                c.addPlayers(player1=a, player2=b, player3=t)
            if t is not None:
                t.addPlayers(player1=a, player2=b, player3=c)
    return playerlist
def Pause():
    print("\n")
    wait=input("Press ENTER to continue.")
    print("\n")
    return
def findWinner(playerlist):
    currentw=0
    for player in playerlist:
        propsum=0
        for prop in player.owned:
            propsum = propsum + prop.sellprice
        totalsum=player.bank+propsum
        if totalsum > currentw:
            currentw=player.bank
    return currentw
def PlayTurn(playerlist):
    done = False
    origlist=[]
    for player in playerlist:
        origlist.append(player)
    while not done:
        for play in origlist:
            print("{}'s turn.".format(play.name))
            print("{}, you have {} in the bank.".format(play.name, play.bank))
            giveowned(origlist)
            trade(play, origlist)
            monoQuestions(play)
            dojail = play.rollDice()
            if dojail == 'wenttojail':
                goToJail(play)
                Pause()
                continue
            if play.injail is True:
                play.turnsinjail = play.turnsinjail + 1
                print("{}, you have spent {} turns in jail.".format(play.name, play.turnsinjail))
                if play.turnsinjail == 3:
                    print("{}, you have spent 3 turns in jail. You've been kicked out!")
                    play.moveTo(JustVisiting)
                    play.injail = False
                    play.turnsinjail = 0
                outOfJail(play)
            if play.bankrupt == True:
                print("REMOVING PLAYER FROM PLAYERLIST")
                playerlist.remove(play)
            Pause()
        if len(playerlist) == 1:
            print("FINISHING LOOP")
            done = True
    return
def goToJail(play):
    print("{}, you are now in jail.".format(play.name))
    play.moveTo(Jail)
    play.injail = True
    play.turnsinjail = 0
def outOfJail(play):
    free = play.hasfreejail
    outjail = False
    if free is True:
        done = False
        while not done:
            usefree = input("{}, would you like to use your Get Out of Jail Free card? Enter Y or N.".format(play.name))
            if usefree == 'Y' or usefree == 'y':
                print("You used your Get Out of Jail Free card.")
                play.hasfreejail = False
                outjail=True
                done = True
            elif usefree == 'N' or usefree == 'n':
                print("Decided not to use your Get Out of Jail Free card.")
                outjail=False
                done = True
            else:
                print("Invalid input.")
    cash = input("{}, would you like to pay $50 to get out of jail? Enter Y or N.".format(play.name))
    end = False
    while not end:
        if cash == 'Y' or cash == 'y':
            print("You paid $50 to get out of jail.")
            play.subBank(50)
            outjail=True
            end = True
        elif cash == 'N' or cash == 'n':
            print("Decided not to pay to get out of jail.")
            outjail=False
            end = True
        else:
            print("Invalid input.")
    if outjail is True:
        print("{}, you got out of jail.".format(play.name))
        play.injail=False
        play.turnsinjail=0
        play.moveTo(JustVisiting)
    return

#not sure where these go yet:
print("Loading...")
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
ReadingRailRoad.AddPairs(PennsylvaniaRailRoad, BORailRoad, ShortLineRailRoad)
PennsylvaniaRailRoad.AddPairs(ReadingRailRoad, BORailRoad, ShortLineRailRoad)
BORailRoad.AddPairs(ReadingRailRoad, PennsylvaniaRailRoad, ShortLineRailRoad)
ShortLineRailRoad.AddPairs(ReadingRailRoad, PennsylvaniaRailRoad, BORailRoad)
railroads=[ReadingRailRoad, PennsylvaniaRailRoad, BORailRoad, ShortLineRailRoad]
#Chance/ComChest

Chance1=Chance(name='Chance',numcards=16)
Chance2=Chance(name='Chance', numcards=16)
Chance3=Chance(name='Chance', numcards=16)

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

CommunityChest1=Chest(name='Community Chest', numcards=17)
CommunityChest2=Chest(name='Community Chest', numcards=17)
CommunityChest3=Chest(name='Community Chest',numcards=17)


startchestdict = {"Advance to Go": 'Go', "Bank Error:Collect $200": 2, "Doctor's Fees:Pay $50": 3,
                     "Sale of Stock:Collect $50": 4,
                     "Get out of Jail Free": 5, "Go to Jail": 'Jail', "Grand Opera Night:Collect $50 from each player": 7,
                     "Holiday Fund Matures:Collect $100": 8, "Income Tax Refund:Collect $20": 9,
                     "Bday! Collect $10 from each player": 10, "Life insurance matures:Collect $100": 11,
                     "Hospital Fees:Pay $50": 12,
                     "School Fees:Pay $50": 13, "Consultancy Fee:Collect $25": 14,
                     "Street Repairs:Pay $40/house, $115/hotel": 15,
                     "Second price in beauty contest:Collect $10": 16, "Inherit $100": 17}
chestdict = {"Advance to Go": 'Go', "Bank Error:Collect $200": 2, "Doctor's Fees:Pay $50": 3,
                     "Sale of Stock:Collect $50": 4,
                     "Get out of Jail Free": 5, "Go to Jail": 'Jail', "Grand Opera Night:Collect $50 from each player": 7,
                     "Holiday Fund Matures:Collect $100": 8, "Income Tax Refund:Collect $20": 9,
                     "Bday! Collect $10 from each player": 10, "Life insurance matures:Collect $100": 11,
                     "Hospital Fees:Pay $50": 12,
                     "School Fees:Pay $50": 13, "Consultancy Fee:Collect $25": 14,
                     "Street Repairs:Pay $40/house, $115/hotel": 15,
                     "Second price in beauty contest:Collect $10": 16, "Inherit $100": 17}

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

#first place is stamp spot, next 4 are houses, one can be hotel)
owned_dict={MediterraneanAvenue:[(225, -240), (244, -265), (229, -265), (217, -265), (203, -264)],
            BalticAvenue:[(116, -235), (134, -266), (121, -266), (112, -266), (94, -266)],
            ReadingRailRoad:[(3, -235)], OrientalAvenue:[(-56, -235), (-36, -262), (-45, -262), (-53, -262), (-74, -263)],
            VermontAvenue:[(-169, -236), (-151, -262), (-162, -260), (-174, -261), (-187, -261)],
            ConnecticutAvenue:[(-229, -239), (-210, -260), (-222, -260), (-235, -260), (-247, -260)],
            StCharlesPlace:[(-249, -222), (-267, -208), (-267, -222), (-267, -236), (-267, -243)],
            ElectricCompany:[(-245, -165)], StatesAvenue:[(-248, -107), (-267, -89), (-267, -104), (-267,-116),(-267, -126)],
            VirginiaAvenue:[(-247, -54), (-267, -28), (-267, -43), (-267, -55), (-267, -68)],
            PennsylvaniaRailRoad:[(-250, 5)], StJamesPlace:[(-250, 61), (-267, 82), (-267, 65), (-267, 52),(-267, 39)],
            TennesseeAvenue:[(-250, 180), (-267, 196), (-267, 183), (-267, 172), (-267, 156)],
            NewYorkAvenue:[(-250, 236), (-267, 253), (-267, 242), (-267, 231), (-267, 217)],
            KentuckyAvenue:[(-221, 255), (-207, 273), (-218, 273), (-230, 273), (-245, 274)],
            IndianaAvenue:[(-114, 251), (-99, 273), (-112, 273), (-124, 273), (-134, 273)],
            IllinoisAvenue:[(-54, 251), (-39, 273), (-53, 273), (-66, 274), (-78, 275)],
            BORailRoad:[(2, 250)], AtlanticAvenue:[(59, 250), (75, 273), (62, 273),(51, 273), (35,273)],
            VetnorAvenue:[(114, 250), (131, 273), (116, 273), (101, 273), (88, 273)],
            WaterWorks:[(175, 250)], MarvinGardens:[(227, 250), (243, 273), (231, 273), (219, 273), (207, 273)],
            PacificAvenue:[(241, 228), (263, 214), (263, 225), (263, 238), (263, 256)],
            NorthCarolinaAvenue:[(241, 176), (263, 197), (263, 185), (263, 168), (263, 154)],
            PennsylvaniaAvenue:[(241, 62), (263, 84), (263, 68), (263, 52), (263, 44)],
            ShortLineRailRoad:[(241, 7)], ParkPlace:[(241, -112), (263, -90), (263, -104), (263, -116), (263, -129)],
            Boardwalk:[(241, -222), (263, -200), (263, -212), (263, -224), (263, -240)]}


def mainGame(tl):
    print("Welcome to Monopoly!")
    playerlist=makePlayer()
    comchest = turtle.Turtle()
    chance = turtle.Turtle()
    board=turtle.Screen()
    Go.playerson=playerlist
    print("Gotcha. Good choice! Now we'll set up the board...(Caution: This will take awhile!)")
    drawBoard(comchest, chance, playerlist, board, tl)
    print("Let's start playing! Have fun!")
    givebankamount(playerlist)
    PlayTurn(playerlist)
    winner=findWinner(playerlist)
    for play in playerlist:
        if play.bank == winner:
            winner = play
    print("Congrats {}, you have won the game!".format(winner))
    print("These were the ending bank balances:{}".format(givebankamount(playerlist)))



mainGame(tl)