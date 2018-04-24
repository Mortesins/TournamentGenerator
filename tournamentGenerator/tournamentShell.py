########################################################################
# Software for collecting data from PV energy meters
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
import os.path

from .tournamentGenerator import *

class TournamentShell():
    'Class for tournament shell interfacet'
    def __init__(self):
        self._tournamentGenerator = None
        self._numberOfPlayers = None
        self._playersPerRace = None
        self._playerListFilename = None

    @property
    def numberOfPlayers(self):
        return self._numberOfPlayers

    @numberOfPlayers.setter
    def numberOfPlayers(self, value):
        if value < 0:
            raise ValueError("Number of players must be positive")
        self._numberOfPlayers = value

    @property
    def playersPerRace(self):
        return self._playersPerRace

    @playersPerRace.setter
    def playersPerRace(self, value):
        if value < 0:
            raise ValueError("Players per race must be positive")
        self._playersPerRace = value

    @property
    def playerListFilename(self):
        return self._playerListFilename

    @playerListFilename.setter
    def playerListFilename(self, value):
        if type(value) is str:
            self._playerListFilename = value
        else:
            raise ValueError("Player list file name must be a string")
    
    def generateTournament(self,points=(),verbose=False,printRacesOnGenerate=False):
        if (self._playersPerRace == None):
            raise ValueError("Players per race must be defined")
        else:
            if (self._playerListFilename != None):
                if os.path.isfile(self._playerListFilename)  : 
                    self._tournamentGenerator = TournamentGenerator.init_fromFile(self._playersPerRace,self._playerListFilename,printRacesOnGenerate,points)
            elif (self._numberOfPlayers  != None):
                self._tournamentGenerator = TournamentGenerator.init_GenerateTournament(self._numberOfPlayers,self._playersPerRace,printRacesOnGenerate,points)
            else:
                raise ValueError("Either players list filename or number of players must be defined")
        self._tournamentGenerator.generate2()
        if verbose:
            self._tournamentGenerator.printRaces()
            self._tournamentGenerator.printNumberOfRacesOfEachPlayer()
            self._tournamentGenerator.printPlayersFacedByEachPlayer()
            
            
            
### PRINT FUNCTIONS ###
    def printRaces(self):
        print("RACES:")
        self._tournamentGenerator.printRaces()

    def printPlayers(self):
        print("PLAYERS:")
        players = self._tournamentGenerator.tournament.players
        players.sort(key=lambda player : player.getName())
        i = 1
        for player in players:
            if (i < 10):
                print(" " + str(i) + ".", player)
            else:
                print(str(i) + ".", player)
            i += 1
    
    def printPlayedRaces(self):
        print("RACES DONE:")
        i = 1
        for race in self._tournamentGenerator.tournament.getRaceResults():
            print("\tRACE"+str(i)+":")
            j = 1
            for result in race:
                print("\t\t" + str(j) + ". " + result[0].getName())
                j+=1
            i+=1

    def printPlayedRacesCompact(self):
        print("RACES DONE:")
        i = 1
        for race in self._tournamentGenerator.tournament.getRaceResults():
            string = ""
            if (i < 10):
                string = " " + str(i) + ". "
            else:
                string = str(i) + ". "
            string += "["
            for playerResult in race:
                string += ( playerResult[0].getName() + "," )
            # eliminate last comma
            string = string[:-1]
            string += "]"
            print(string)
            i+=1

    def printStanding(self):
        print("STANDINGS:")
        standings = self._tournamentGenerator.tournament.getStandingsPrintable()
        # find max length of player name
        maxLength = 0
        for player in self._tournamentGenerator.tournament.getPlayers():
            if (len(player.getName()) > maxLength):
                maxLength = len(player.getName())
        # if max length name shorter than "PLAYER" than I take "PLAYER" length
        if maxLength < 6:
            maxLength = 6
        print("._"+"_"*maxLength+"_._______.________.")
        # header
        trailingSpaces = " " * (maxLength - 6)
        print("| PLAYER" + trailingSpaces + " | RACES | POINTS |")
        print("+-"+"-"*maxLength+"-+-------+--------+")
        # entries
        for entry in standings:
            trailingSpaces = " " * (maxLength - len(entry[0]))
            if entry[1] >= 10:
                racesSpacing = "   "
            else:
                racesSpacing = "    "
            if entry[2] >= 10:
                pointsSpacing = "    "
            else:
                pointsSpacing = "     "
            print("| " + entry[0] + trailingSpaces + " | " + racesSpacing + str(entry[1]) + " | " + pointsSpacing + str(entry[2]) + " |")
        print("+-"+"-"*maxLength+"-+-------+--------+")
            

    def printFastestLapStanding(self):
        print("FASTEST LAP STANDINGS:")
        standings = self._tournamentGenerator.tournament.getFastestLapStandingPrintable()
        # find max length of player name
        maxLength = 0
        for player in self._tournamentGenerator.tournament.getPlayers():
            if (len(player.getName()) > maxLength):
                maxLength = len(player.getName())
        # if max length name shorter than "PLAYER" than I take "PLAYER" length
        if maxLength < 6:
            maxLength = 6
        print("._"+"_"*maxLength+"_.__________.")
        # header
        trailingSpaces = " " * (maxLength - 6)
        print("| PLAYER" + trailingSpaces + " |   TIME   |")
        print("+-"+"-"*maxLength+"-+----------+")
        # entries
        for entry in standings:
            trailingSpaces = " " * (maxLength - len(entry[0]))
            print("| " + entry[0] + trailingSpaces + " | " + str(entry[1]) + " |")
        print("+-"+"-"*maxLength+"-+----------+")

  # print functions for checking tournament
    def printNumberOfRacesOfEachPlayer(self):
        print("NUMBER OF RACES:")
        self._tournamentGenerator.printNumberOfRacesOfEachPlayer()

    def printPlayersFacedByEachPlayer(self):
        print("PLAYERS FACED BY EACH PLAYER:")
        self._tournamentGenerator.printPlayersFacedByEachPlayer()

  # print function for specific player
    def printPlayerNumberOfRaces(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournamentGenerator.tournament.players[playerNumber - 1]
        print("NUMBER OF RACES:")
        self._tournamentGenerator.printPlayerNumberOfRaces(player)

    def printPlayerNumberOfRacesDone(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournamentGenerator.tournament.players[playerNumber - 1]
        print("NUMBER OF RACES DONE:")
        print(player.getName() + ": " + str(player.getRacesDone()))
        
    def printPlayerPlayersFaced(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournamentGenerator.tournament.players[playerNumber - 1]
        print("PLAYERS FACED:")
        self._tournamentGenerator.printPlayerPlayersFaced(player)

    def printPlayerFastestLap(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournamentGenerator.tournament.players[playerNumber - 1]
        print("FASTEST LAP:")
        print(player.getName() + ": " + player.getFastestLapPrintable())

    def printPlayerPoints(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournamentGenerator.tournament.players[playerNumber - 1]
        print("POINTS:")
        print(player.getName() + ": " + str(player.getPoints()))
#######################
