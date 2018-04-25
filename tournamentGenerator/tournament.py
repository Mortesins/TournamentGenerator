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

from itertools import product,combinations
from math import ceil,log
from string import ascii_uppercase
from random import randint
from datetime import time

from .player import *
from .raceCosts import *
from .helper import removeList2fromList1, convertRaceResultToRace, sameRace

class Tournament():
    'Tournament class, containing players and races'
    def __init__(self, players, points=()):
        self.players = players
        # contains tuple with points assigned for each position
        self.points = points
        # races, which are lists of players in the race
        self.races = []
        # race results which are arrays of (player, time) tuples in the order of arrival
        self.raceResults = []
        # races to do (not played yet)
        self.racesToDo = []
        # list of players in the order based on points
        self.standings = list(players)
        # list of players in the order based on fastest lap
        self.standingsFastestLap = []

    @classmethod
    def init_GeneratePlayers(cls, numberOfPlayers, points=()):
        players = []
        letters = list(ascii_uppercase)
        # how many letters needed for the number of players
            # 1 letter, 26 players, 2 letters 26*26 players
            # take the logarithm base 26, and then get the nearest higher integer
        numberOfLetters = int(ceil(log(numberOfPlayers,26)))
        i = 0
        # end when added numberOfPlayers
        for nameTuple in product(letters,repeat=numberOfLetters):
            # the name is ('A','A','A'), so I need to convert to string
            name = ""
            for j in range(0,numberOfLetters):
                name = name + nameTuple[j]
            if i < numberOfPlayers:
                players.append(Player(name))
                i += 1
            else:
                break
        return cls(players,points)

    def addRace(self,race):
        # race must be a list or tuple of Player
        if ( (isinstance(race,list) or isinstance(race,tuple)) and isinstance(race[0],Player) ):
            self.races.append(race)
            # increment number of races
            for player in race:
                player.addRace()
            # add faced players
            for comb in combinations(race,2):
                # for every couple with players of the race, face each other
                playersFaceEachOther(comb[0],comb[1])
        else:
            raise TypeError(race + " is not of type Player")
        return
    
    def getPlayers(self):
        return list(self.players)
        
    def getRaces(self):
        return list(self.races)

    def getRace(self,index):
        return list(self.races[index])

    def getRaceResults(self):
        return list(self.raceResults)

    def getRaceResult(self,index):
        return self.raceResults[index]

    def raceExists(self,race):
        for r in self.races:
            # check if every player of race is contained in r, if so raceExists
            allRplayersInRace = True
            i = 0
            while (i < len(r)) and allRplayersInRace:
                # if race does not contain player (r[i])
                if not (r[i] in race):
                    allRplayersInRace = False
                i += 1
            # if all players of r are in race, then this is the race, so raceExists
            if allRplayersInRace:
                return True
        return False
        
    def playersSameNumberOfRaces(self):
        ''' checks if all players of tournament have the same number of races '''
        numberOfRaces = None
        for player in self.players:
            # first run, so I store the number of races of first player
            if numberOfRaces == None:
                numberOfRaces = player.getRaces()
            else:
                # check if current player has same number of races as the first
                    # if one player does not have the same number of races as the first, 
                    #   then all players can't have same number of races
                if numberOfRaces != player.getRaces():
                    return False
        # if all players have same number of races as first player, 
        # then everyone has same number of races
        return True
    
    def somebodyDidNotFaceEveryone(self):
        ''' checks if there is at least a player that hasn't faced every other player '''
        for player in self.players:
            # if player has at least a player not faced, then somebodyDidNotFaceEveryone (true)
            if len(player.playersNotFaced(self.players)) != 0:
                return True
        # all players have playersNotFaced list empty, so everyone has faced everyone
        return False

    def getPlayerThatHasntFacedEveryone(self):
        for player in self.players:
            # if player has at least a player not faced, then return this player
            if len(player.playersNotFaced(self.players)) != 0:
                return player
        # all players have playersNotFaced list empty, so everyone has faced everyone
        return None

    def getRandomPlayerThatHasntFacedEveryone(self):
        p = []
        for player in self.players:
            # if player has at least a player not faced, then return this player
            if len(player.playersNotFaced(self.players)) != 0:
                p.append(player)
        # random index of players that haven't faced everyone
        if (len(p) != 0):
            i = randint(0,len(p)-1) 
            return p[i]
        else:
            return None

    def averageNumberOfRaces(self):
        mean = 0.0
        for player in self.players:
            mean += player.getRaces() 
        return mean / len(self.players)

    def costOfRace(self,race):
        return costOfRace(race,self.averageNumberOfRaces())

    def addRaceResult(self,resultsTuples):
        ''' 
            resultsTuples is a list of tuple of type (player,position,time)
            the race result is added as tuple (player,time) in order of arrival
            for each player
                give points
                set fastest time
                add races done
        '''
        # creates race result
        raceResult = []
        # sort race results by position
        resultsTuples.sort(key=lambda resultsTuple : resultsTuple[1])
        i = 0
        for resultsTuple in resultsTuples:
          # give points to each player
            # if there are point for that position
            try:
                resultsTuple[0].addPoints(self.points[i])
            except IndexError:
                # there are no points for ith position
                pass
            i += 1
          # set fastest lap time of each player
            # if player has not fastest time
            # or fastest time of this race better than previous fastest time
            if ( (resultsTuple[0].getFastestLap() == None) or (resultsTuple[2] < resultsTuple[0].getFastestLap()) ): 
                resultsTuple[0].setFastestLap(resultsTuple[2])
          # add race done
            resultsTuple[0].addRaceDone()
          # append (player,time)
            raceResult.append((resultsTuple[0],resultsTuple[2]))
        self.raceResults.append(raceResult)

    def _calculateStandingsFastestLap(self):
        ''' calculates and stores players ordered by fastest lap '''
        # if standingsFastestLap does not contain all players
            # copy players to standingsFastestLap
            # remove players without fastestLap
        # sort standingsFastestLap
        if (len(self.standingsFastestLap) != len(self.players)):
            self.standingsFastestLap = list(self.players)
            i = 0
            while i < len(self.standingsFastestLap):
                if (self.standingsFastestLap[i].getFastestLap() == None):
                    self.standingsFastestLap.pop(i)
                else:
                    i += 1
        self.standingsFastestLap.sort(key=lambda player : player.getFastestLap())

    def _calculateStandings(self):
        ''' calculates and stores players ordered by points '''
        self.standings.sort(key=lambda player : player.getPoints(),reverse=True)

    def getFastestLapTime(self):
        self._calculateStandingsFastestLap()
        return self.standingsFastestLap[0].getFastestLap()

    def getFastestLapPlayer(self):
        self._calculateStandingsFastestLap()
        return self.standingsFastestLap[0]

    def getFastestLapStanding(self):
        ''' returns [ player, ... ] ordered by fastest lap '''
        self._calculateStandingsFastestLap()
        return list(self.standingsFastestLap)

    def getFastestLapStandingPrintable(self):
        ''' returns [ (player name, time), ... ] rdered by fastest lap '''
        self._calculateStandingsFastestLap()
        result = []
        for player in self.standingsFastestLap:
            result.append(\
                (\
                    player.getName(),\
                    player.getFastestLapPrintable()\
                )\
            )
        return result

    def getStandings(self):
        ''' returns [ player, ... ] ordered by points '''
        self._calculateStandings()
        return list(self.standings)

    def getStandingsPrintable(self):
        ''' returns [ (player name, number of races, points), ... ] ordered by points '''
        self._calculateStandings()
        result = []
        for player in self.standings:
            result.append(\
                (\
                    player.getName(),\
                    player.getRacesDone(),\
                    player.getPoints()\
                )\
            )
        return result

    def getRacesToDo(self):
        self._calculateRacesToDo()
        return list(self.racesToDo)

    def _calculateRacesToDo(self):
        if self.racesToDo == []:
            # all races, then I remove the ones already done
            self.racesToDo = list(self.races)
        # temporarily store races which will be removed at the end
        racesToRemove = []
        # for each race to do check if present in race results, if so remove it
        for race in self.racesToDo:
            for raceResultTmp in self.raceResults:
                raceResult = convertRaceResultToRace(raceResultTmp)
                # if raceResult is the same as race, then this race is already done
                    # so I remove it from racesToDo
                if sameRace(raceResult,race):
                    racesToRemove.append(race)
        removeList2fromList1(self.racesToDo,racesToRemove)
