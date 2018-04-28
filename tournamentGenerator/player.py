########################################################################
# Software for generating races of a tournament
# Copyright (C) 2018 Axel Bernardinis <abernardinis@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
########################################################################

from random import randint
from datetime import time

from .helper import lapTimeToStr

class Player():
    'Player class'
    def __init__(self, name):
        self.name = name
        self.races = 0
        self.racesDone = 0
        self.points = 0
        self.fastestLap = None
        self.facedPlayers = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def addRace(self):
        self.races += 1
        return

    def addFacedPlayer(self, player):
        self.facedPlayers.append(player)
        return

    def getRaces(self):
        return self.races

    def getFacedPlayers(self):
        return self.facedPlayers

    def getName(self):
        return self.name

    def addRaceDone(self):
        self.racesDone += 1
        return

    def addPoints(self,points):
        if (points >= 0):
            self.points += points

    def setFastestLap(self, fastestLap):
        # check fastestLap of type datetime.time
        if type(fastestLap) is time:
            self.fastestLap = fastestLap

    def getRacesDone(self):
        return self.racesDone

    def getPoints(self):
        return self.points

    def getFastestLap(self):
        return self.fastestLap

    def getFastestLapPrintable(self):
        if self.fastestLap == None:
            return "None"
        return lapTimeToStr(self.fastestLap)

    def hasFaced(self, player):
        for p in self.facedPlayers:
            if p == player:
                return True
        return False

    def numberOfTimesAlreadyFaced(self, player):
        n = 0
        for p in self.facedPlayers:
            if (p == player):
                n += 1
        return n

    def numberPlayersFaced(self):
        return len(self.facedPlayers)

    def playersNotFaced(self, allPlayers):
        listPlayersNotFaced = []
        for player in allPlayers:
            if not self.hasFaced(player) and self != player:
                listPlayersNotFaced.append(player)
        return listPlayersNotFaced


def playersFaceEachOther(player1, player2):
    player1.addFacedPlayer(player2)
    player2.addFacedPlayer(player1)
    return


def playersWithLeastRaces(players):
    ''' given list of players, returns list of players with less races '''
    # find least amount of races
    plr = []
    minRaces = players[0].getRaces()
    plr.append(players[0])
    i = 1
    while (i < len(players)):
        if players[i].getRaces() < minRaces:
            minRaces = players[i].getRaces()
            plr = []
            plr.append(players[i])
        elif players[i].getRaces() == minRaces:
            plr.append(players[i])
        i += 1
    return plr

def playerWithLeastRaces(players):
    p = playersWithLeastRaces(players)
    i = randint(0,len(p)-1) 
    return p[i]

def nPlayersWithLeastRaces(n, players):
    ''' given list of players, returns n players with the least races '''
    players.sort(key=lambda player : player.getRaces())
    return players[:n]

def atLeastNplayersWithLeastRaces(n, players):
    ''' 
        given list of players, 
        returns n players with the least races along with all the players with the same number of races 
        EXAMPLE: # 4,4,4,6,7,7,7,8,8,9
            if n is 5, then it will return 4,4,4,6,7 plus all other with 7 races, so 4,4,4,6,7,7,7
    '''
    players.sort(key=lambda player : player.getRaces())
    # number of races of the nth player
    racesNthPlayer = players[n-1].getRaces()
    # get other players with same number of races
        # find index (starting from n) at which the player has more races than the nth player
    i = n
    indexFound = False
    while (i < len(players) and (not indexFound)):
        # if ith player has different number of races, than return players from 0 to i-1
            # because i-1 is the last index which had racesNthPlayer
        if (players[i].getRaces() != racesNthPlayer):
            indexFound = True
        else: # so I don't increment i when I find it
            i += 1
    # return until i-1, but :i excludes i
    return players[:i]



