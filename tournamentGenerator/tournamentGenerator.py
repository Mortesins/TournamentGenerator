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

from __future__ import print_function
import sys

from .tournament import *
from .raceCosts import *

class TournamentGenerator():
    'Tournament generator class, containing tournament'
    def __init__(self, tournament, numberOfPlayers, playersPerRace, printRaces = False):
        self.tournament = tournament
        self.numberOfPlayers = numberOfPlayers
        self.playersPerRace = playersPerRace
        self.printRacesFlag = printRaces

    @classmethod
    def init_GenerateTournament(cls, numberOfPlayers, playersPerRace, printRaces = False, points = ()):
        tournament = Tournament.init_GeneratePlayers(numberOfPlayers,points)
        return cls(tournament,numberOfPlayers,playersPerRace,printRaces)
    
    @classmethod
    def init_fromFile(cls, playersPerRace, filename, printRaces = False, points = ()):
        players = []
        fp = open(filename)
        for line in fp:
            players.append(Player(line[:-1]))
        return cls(Tournament(players,points), len(players), playersPerRace, printRaces, points)

    def printRace(self,race):
        if self.printRacesFlag:
            print(race)

    def generate_randomLowCost(self):
        '''
            generates by adding least cost races 
            until all players have faced each other
                every player same number of races
        '''
        # while at least a player hasn't faced everyone and not all players have same number of races
        while ( not(self.tournament.playersSameNumberOfRaces()) or (self.tournament.somebodyDidNotFaceEveryone()) ):
            race = leastExpensiveRace(self.tournament.players,self.playersPerRace,self.tournament.averageNumberOfRaces())
            self.tournament.addRace(race)
            self.printRace(race)

    def generate_AllPlayersFaceEachOther(self):
        '''
            generates by:
            until all players have faced each other:
                get player that hasn't faced someone
                add least costly race between him and players he hasn't met
                    in case not enough players, get the rest from players with least races
                    (example: 4 players per race, player has only 1 player not met, so get at least 2 from least number of races)
        '''
        # while at least a player hasn't faced everyone
        while (self.tournament.somebodyDidNotFaceEveryone()):
            player = self.tournament.getPlayerThatHasntFacedEveryone()
            playersNotFaced = player.playersNotFaced(self.tournament.getPlayers())
            # while still some players to be faced
            while (len(playersNotFaced) != 0):
                # if number of playersNotFaced equal to playersPerRace - 1 or more
                    # find combination of (playersPerRace - 1) players, that along with player gives race with least cost
                if ( len(playersNotFaced) > (self.playersPerRace - 1) ):
                    race = leastExpensiveRace(playersNotFaced,self.playersPerRace,self.tournament.averageNumberOfRaces(),[player])
                    self.tournament.addRace(race)
                    self.printRace(race)
                # if number of playersNotFaced equal to playersPerRace - 1 
                    # then by adding player I have exactly playersPerRace number of players
                    # so the race is the player with playersNotFaced
                elif ( len(playersNotFaced) == (self.playersPerRace - 1) ):
                    # append player and add race
                    race = list(playersNotFaced)
                    race.append(player)
                    self.tournament.addRace(race)
                    self.printRace(race)
                # playersNotFaced not enough for a race, so I fix playerNotFaced and player, 
                    # and get the remaining players from playerWithLeastRaces
                    # NOTE: by using atLeastNplayersWithLeastRaces, I might have more than needed, so I check the costs
                        # however they all have same number of races
                else:
                    # I fix
                    fixedPlayers = list(playersNotFaced)
                    fixedPlayers.append(player)
                    # add at least n players, where n is needed to reach playerPerRace
                        # I actually get least playerPerRace number of players, and then I remove fixedPlayers 
                            # since fixedPlayers could be in playersWithLeastRaces
                    otherPlayers = atLeastNplayersWithLeastRaces(self.playersPerRace,self.tournament.getPlayers())
                    removeList2fromList1(otherPlayers,fixedPlayers)
                    race = leastExpensiveRace(\
                            otherPlayers,\
                            self.playersPerRace,\
                            self.tournament.averageNumberOfRaces(),\
                            fixedPlayers)
                    self.tournament.addRace(race)
                    self.printRace(race)
                playersNotFaced = player.playersNotFaced(self.tournament.getPlayers())
        # 2) until every player same number of race
        # while ( not(self.tournament.playersSameNumberOfRaces()) ):
        #    self.tournament.addRace(leastExpensiveRace(self.tournament.players,self.playersPerRace,self.tournament.averageNumberOfRaces()))
   
    def generate_AllPlayersSameNumberOfRaces(self):
        '''
            generates by:
                until every player same number of races
                    add least costly races
        '''
        # until every player same number of race
        while ( not(self.tournament.playersSameNumberOfRaces()) ):
            # get a random player with least number of races
            player = playerWithLeastRaces(self.tournament.getPlayers())
            # add least cost race by fixing player, and remaining playersWithLeastRaces
            otherPlayers = atLeastNplayersWithLeastRaces(self.playersPerRace,self.tournament.getPlayers())
            removeList2fromList1(otherPlayers,[player])
            race = leastExpensiveRace(\
                        otherPlayers,\
                        self.playersPerRace,\
                        self.tournament.averageNumberOfRaces(),\
                        [player])
            self.tournament.addRace(race)
            self.printRace(race)
            
    def generate1(self):
        self.generate_AllPlayersFaceEachOther()
        self.generate_randomLowCost()

    def generate2(self):
        self.generate_AllPlayersFaceEachOther()
        self.generate_AllPlayersSameNumberOfRaces()

    def printRaces(self):
        i = 1
        for race in self.tournament.getRaces():
            if (i < 10):
                print(" " + str(i) + ".", race)
            else:
                print(str(i) + ".", race)
            i+=1
    
    def printNumberOfRacesOfEachPlayer(self):
        players = self.tournament.getPlayers()
        players.sort(key=lambda player : player.getName())
        for player in players:
            self.printPlayerNumberOfRaces(player)
            #print(str(player) + ":" + str(player.getRaces()))

    def printPlayerNumberOfRaces(self,player):
        print(str(player) + ":" + str(player.getRaces()))

    def printPlayersFacedByEachPlayer(self):
        players = self.tournament.getPlayers()
        players.sort(key=lambda player : player.getName())
        for player in players:
            self.printPlayerPlayersFaced(player)

    def printPlayerPlayersFaced(self,player):
        stringFacedPlayers = "["
        facedPlayers = player.getFacedPlayers()
        facedPlayers.sort(key=lambda player : player.getName())
        for facedPlayer in facedPlayers:
            stringFacedPlayers += ( str(facedPlayer) + "," )
        # eliminate last comma
        stringFacedPlayers = stringFacedPlayers[:-1]
        stringFacedPlayers += "]"
        print(str(player) + ":" + stringFacedPlayers)

def removeList2fromList1(a,b):
    for item in b:
        try:
            a.remove(item)
        except ValueError:
            None
    return
