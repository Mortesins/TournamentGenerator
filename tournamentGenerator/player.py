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
        self._name = name
        self._races = 0
        self._racesDone = 0
        self._points = 0
        self._fastestLap = None
        self._facedPlayers = []

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

### GETTERS AND SETTERS ###
    @property
    def races(self):
        return self._races
    
    @property
    def facedPlayers(self):
        return list(self._facedPlayers)

    @property
    def name(self):
        return self._name

    @property
    def racesDone(self):
        return self._racesDone
    
    @property
    def points(self):
        return self._points
    
    @property
    def fastestLap(self):
        return self._fastestLap

    @fastestLap.setter
    def fastestLap(self, fastestLap):
        # check fastestLap of type datetime.time
        if type(fastestLap) is time:
            self._fastestLap = fastestLap
###########################

    def addRace(self):
        self._races += 1
        return

    def addFacedPlayer(self, player):
        self._facedPlayers.append(player)
        return

    def addRaceDone(self):
        self._racesDone += 1
        return

    def addPoints(self,points):
        if (type(points) == int and points >= 0):
            self._points += points

    def getFastestLapPrintable(self):
        if self._fastestLap == None:
            return "None"
        return lapTimeToStr(self._fastestLap)

    def hasFaced(self, player):
        for p in self._facedPlayers:
            if p == player:
                return True
        return False

    def numberOfTimesAlreadyFaced(self, player):
        n = 0
        for p in self._facedPlayers:
            if (p == player):
                n += 1
        return n

    def numberPlayersFaced(self):
        return len(self._facedPlayers)

    def playersNotFaced(self, allPlayers):
        listPlayersNotFaced = []
        for player in allPlayers:
            if not self.hasFaced(player) and self != player:
                listPlayersNotFaced.append(player)
        return listPlayersNotFaced

### PRINT FUNCTIONS ###
    def printNumberOfRaces(self):
        print(str(self) + ":" + str(self._races))
    
    def printPlayersFaced(self):
        stringFacedPlayers = "["
        facedPlayers = list(self._facedPlayers)
        facedPlayers.sort(key=lambda player : player.name)
        for facedPlayer in facedPlayers:
            stringFacedPlayers += ( str(facedPlayer) + "," )
        # eliminate last comma
        stringFacedPlayers = stringFacedPlayers[:-1]
        stringFacedPlayers += "]"
        print(str(self) + ":" + stringFacedPlayers)
#######################


def playersFaceEachOther(player1, player2):
    player1.addFacedPlayer(player2)
    player2.addFacedPlayer(player1)
    return


def playersWithLeastRaces(players):
    ''' given list of players, returns list of players with less races '''
    # find least amount of races
    plr = []
    minRaces = players[0].races
    plr.append(players[0])
    i = 1
    while (i < len(players)):
        if players[i].races < minRaces:
            minRaces = players[i].races
            plr = []
            plr.append(players[i])
        elif players[i].races == minRaces:
            plr.append(players[i])
        i += 1
    return plr

def playerWithLeastRaces(players):
    p = playersWithLeastRaces(players)
    i = randint(0,len(p)-1) 
    return p[i]

def nPlayersWithLeastRaces(n, players):
    ''' given list of players, returns n players with the least races '''
    players.sort(key=lambda player : player.races)
    return players[:n]

def atLeastNplayersWithLeastRaces(n, players):
    ''' 
        given list of players, 
        returns n players with the least races along with all the players with the same number of races 
        EXAMPLE: # 4,4,4,6,7,7,7,8,8,9
            if n is 5, then it will return 4,4,4,6,7 plus all other with 7 races, so 4,4,4,6,7,7,7
    '''
    players.sort(key=lambda player : player.races)
    # number of races of the nth player
    racesNthPlayer = players[n-1].races
    # get other players with same number of races
        # find index (starting from n) at which the player has more races than the nth player
    i = n
    indexFound = False
    while (i < len(players) and (not indexFound)):
        # if ith player has different number of races, than return players from 0 to i-1
            # because i-1 is the last index which had racesNthPlayer
        if (players[i].races != racesNthPlayer):
            indexFound = True
        else: # so I don't increment i when I find it
            i += 1
    # return until i-1, but :i excludes i
    return players[:i]



