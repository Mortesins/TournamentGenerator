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

from .tournament import *
from .raceCosts import *
from .helper import removeList2fromList1, printRaces

class RaceGenerator():
    'Race generator class'
    def __init__(self, playersPerRace, printRaces = False):
        self.playersPerRace = playersPerRace
        self.printRacesFlag = printRaces

    def generate_randomLowCost(self,tournament):
        '''
            generates by adding least cost races 
            until all players have faced each other
                every player same number of races
        '''
        # while at least a player hasn't faced everyone and not all players have same number of races
        while ( not(tournament.playersSameNumberOfRaces()) or (tournament.somebodyDidNotFaceEveryone()) ):
            race = leastExpensiveRace(tournament.players,self.playersPerRace,tournament.averageNumberOfRaces())
            tournament.addRace(race)
            self.printRace(race)

    def generate_AllPlayersFaceEachOther(self,tournament):
        '''
            generates by:
            until all players have faced each other:
                get player that hasn't faced someone
                add least costly race between him and players he hasn't met
                    in case not enough players, get the rest from players with least races
                    (example: 4 players per race, player has only 1 player not met, so get at least 2 from least number of races)
        '''
        # while at least a player hasn't faced everyone
        while (tournament.somebodyDidNotFaceEveryone()):
            player = tournament.getPlayerThatHasntFacedEveryone()
            playersNotFaced = player.playersNotFaced(tournament.getPlayers())
            # while still some players to be faced
            while (len(playersNotFaced) != 0):
                # if number of playersNotFaced equal to playersPerRace - 1 or more
                    # find combination of (playersPerRace - 1) players, that along with player gives race with least cost
                if ( len(playersNotFaced) > (self.playersPerRace - 1) ):
                    race = leastExpensiveRace(playersNotFaced,self.playersPerRace,tournament.averageNumberOfRaces(),[player])
                    tournament.addRace(race)
                    self.printRace(race)
                # if number of playersNotFaced equal to playersPerRace - 1 
                    # then by adding player I have exactly playersPerRace number of players
                    # so the race is the player with playersNotFaced
                elif ( len(playersNotFaced) == (self.playersPerRace - 1) ):
                    # append player and add race
                    race = list(playersNotFaced)
                    race.append(player)
                    tournament.addRace(race)
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
                    otherPlayers = atLeastNplayersWithLeastRaces(self.playersPerRace,tournament.getPlayers())
                    removeList2fromList1(otherPlayers,fixedPlayers)
                    race = leastExpensiveRace(\
                            otherPlayers,\
                            self.playersPerRace,\
                            tournament.averageNumberOfRaces(),\
                            fixedPlayers)
                    tournament.addRace(race)
                    self.printRace(race)
                playersNotFaced = player.playersNotFaced(tournament.getPlayers())
        # 2) until every player same number of race
        # while ( not(tournament.playersSameNumberOfRaces()) ):
        #    tournament.addRace(leastExpensiveRace(tournament.players,self.playersPerRace,tournament.averageNumberOfRaces()))
   
    def generate_AllPlayersSameNumberOfRaces(self,tournament):
        '''
            generates by:
                until every player same number of races
                    add least costly races
        '''
        # until every player same number of race
        while ( not(tournament.playersSameNumberOfRaces()) ):
            # get a random player with least number of races
            player = playerWithLeastRaces(tournament.getPlayers())
            # add least cost race by fixing player, and remaining playersWithLeastRaces
            otherPlayers = atLeastNplayersWithLeastRaces(self.playersPerRace,tournament.getPlayers())
            removeList2fromList1(otherPlayers,[player])
            race = leastExpensiveRace(\
                        otherPlayers,\
                        self.playersPerRace,\
                        tournament.averageNumberOfRaces(),\
                        [player])
            tournament.addRace(race)
            self.printRace(race)
       
    def printRace(self,race):
        if self.printRacesFlag:
            print(race)
            
    def generate_randomUntilSameNumberOfRaces(self,tournament):
        self.generate_AllPlayersFaceEachOther(tournament)
        self.generate_randomLowCost(tournament)

    def generate_lowCostForPlayerWithLeastRaces(self, tournament):
        self.generate_AllPlayersFaceEachOther(tournament)
        self.generate_AllPlayersSameNumberOfRaces(tournament)


