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
import os.path
from cmd import Cmd
import pickle

from .tournament import *
from .randomPlayerGenerator import RandomPlayerGenerator
from .playerGeneratorFromFile import PlayerGeneratorFromFile
from .raceGenerator import RaceGenerator
from .helper import printRaces, convertRaceResultToRace, convertRaceResultsToRaces, sameRace, lapTimeToStr

class TournamentShell(Cmd):
    'Class for tournament shell interface'
    def __init__(self,t=None,np=None,pr=None,pf=None,p=None,flp=1):
        Cmd.__init__(self)
        self._tournament = t
        # number of players of the tournament needed for generation without file with player names
        self._numberOfPlayers = np
        # number of players that participate in each race
        self._playersPerRace = pr
        # a tuple containing the points received based on placement
            # (4,3,2,1)
        self._points = p
        # point for fastest lap
        self._fastestLapPoint = flp
        # filename containing the players name
        self._playerListFilename = pf
    
    @classmethod
    def init_fromPickle(cls, filename):
        tournament = pickle.load(open(filename,"rb"))
        # get the first race to see how many players per race
        return cls(\
            tournament,\
            tournament.getNumberOfPlayers(),\
            len(tournament.getRace(0)),\
            tournament.points\
        )

### CMD commands ###
    # exit function
    def do_quit(self,s):
        exit()
    def do_exit(self,s):
        exit()
    def do_q(self,s):
        exit()
    def help_quit(self):
        print("Quits the program")
    def help_exit(self):
        print("Quits the program")
    def help_q(self):
        print("Quits the program")
    
    ### creates pickle of tournamentGenerator as backup ##
    def do_backup(self,s):
        if (s != ""):
            p = s.split()
            self._backup(p[0])
        else:
            self._backup()
    def help_backup(self):
        print("Creates pickle of tournament as backup.")
        print("USAGE: backup [filename.p]")
    
    ### generate tournament ###
    def do_generateTournament(self,s):
        try:
            # if no parameters
            if (s == ""):
                self.generateTournament()
            else:
                # default no verbose no print races
                v = False
                p = False
                # parameters
                p = s.split()
                if "-v" in p:
                    v = True
                if "--printRacesOnGenerate" in p:
                    p = True
                self.generateTournament(v,p)
            # write pickle backup
            self._backup()
        except ValueError as e:
            print("ERROR: cannot generate tournament")
            print(e)
            print("NOTE: to generate the tournament the following must be set beforehand:")
            print("\t numberOfPlayers or playerListFilename")
            print("\t points")
            print("\t playersPerRace")

    def help_playRace(self,s):
        print("USAGE: generateTournament [OPTIONS]")
        print("OPTIONS:")
        print("\t -v                     : verbose, prints data to check the correctness of tournament")
        print("\t --printRacesOnGenerate : prints the races as they are generated")
        print("Generates the tournament. NOTE: the following must be set beforehand:")
        print("\t numberOfPlayers or playerListFilename")
        print("\t points")
        print("\t playersPerRace")
    ### play a race ###
    def do_playRace(self,s):
        raceInserted = False
        if (s == ""):
            self.printRacesToDo()
            raceNumberRaw = input("Number of race to be played: ")
            # quit playRace
            if (raceNumberRaw == "q"):
                return False
            incorrectNumber = True
            while (incorrectNumber):
                try:
                    raceNumber = int(raceNumberRaw)
                    if ( (raceNumber > 0) and (raceNumber <= len(self._tournament.getRacesToDo()) ) ):
                        raceInserted = self.playRace(raceNumber)
                        # end loop
                        incorrectNumber = False
                    else:
                        raceNumberRaw = input("Please enter a correct race number: ")
                        # quit playRace
                        if (raceNumberRaw == "q"):
                            return False
                except ValueError:
                    raceNumberRaw = input("Please enter a correct race number: ")
                    # quit playRace
                    if (raceNumberRaw == "q"):
                        return False
        else:
            # get player number from parameters
            p = s.split()
            try:
                raceNumber = int(p[0])
                if ( (raceNumber > 0) and (raceNumber <= len(self._tournament.getRacesToDo()) ) ):
                    raceInserted = self.playRace(raceNumber)
                else:
                    print("Wrong race number")
            except ValueError:
                print("Wrong race number")
        if (raceInserted):
            print("Race results inserted")
            # write pickle backup
            self._backup()
        else:
            print("ERROR: race results not inserted")

    def help_playRace(self):
        print("USAGE: playRace RACENUMBER")
        print("Adds the result (including fastest time) of the race specified with the number.")

  ### GETTERS AND SETTERS ###
    def do_setNumberOfPlayers(self,s):
        # check for positive integer
        error = False
        if (s != ""):
            p = s.split()
            try:
                n = int(p[0])
                # points must be positive
                if (n < 0):
                    error = True
            except ValueError:
                error = True
        else: # if no parameters
            error = True
        # if playersPerRace set, if numberOfPlayers less than playersPerRace then error
        if (not error):
            if (self._playersPerRace != None):
                if (self._playersPerRace > n):
                    error = True
        if (not error):
            self._numberOfPlayers = n
            # write pickle backup
            self._backup()
        else:
            print("Number of players must be positive integer greater than players per race")
    def help_setNumberOfPlayers(self):
        print("Sets the number of players of the tournament needed for generation without file with player names")
    def do_setPlayersPerRace(self,s):
        # check for positive integer
        error = False
        if (s != ""):
            p = s.split()
            try:
                n = int(p[0])
                # points must be positive
                if (n < 0):
                    error = True
            except ValueError:
                error = True
        else: # if no parameters
            error = True
        # if numberOfPlayers set, if numberOfPlayers less than playersPerRace then error
        if (not error):
            if (self._numberOfPlayers != None):
                if (self._numberOfPlayers < n):
                    error = True
        if (not error):
            self._playersPerRace = n
            # write pickle backup
            self._backup()
        else:
            print("Players per race must be positive integer less than number of players")
    def help_setPlayersPerRace(self):
        print("Sets the number of players that participate in each race")
    def do_setPlayerListFilename(self,s):
        p = s.split()
        self._playerListFilename = p[0]
    def help_setPlayerListFilename(self):
        print("Sets the path of the file containing the players names.\
                Each player name has to be on a new line.\
                The number of players will be the equal to the number of names in the file")
    def do_setPoints(self,s):
        # check for comma separated points (int)
        error = False
        if (s != ""):
            pointsString = (s.split())[0]
            points = pointsString.split(",")
            for i in range(0,len(points)):
                try:
                    points[i] = int(points[i])
                    # points must be positive
                    if (points[i] < 0):
                        error = True
                except ValueError:
                    error = True
        else: # if no parameters
            error = True
        if (not error):
            self._points = tuple(points)
            # write pickle backup
            self._backup()
        else:
            print("Points must be positive integers separated by a comma")
            print("EXAMPLE: 4,3,2,1")
    def help_setPoints(self):
        print("USAGE: setPoints POINTS_TUPLE.")
        print("EXAMPLE: setPoints (4,3,2,1)")
        print("\t would give 4 points to the first, 3 to the second, 2 to the third and 1 to the last")
        print("Sets the points awarded in each race.")
    def do_setFastestLapPoint(self,s):
        # check for positive integer
        error = False
        if (s != ""):
            p = s.split()
            try:
                n = int(p[0])
                # points must be positive
                if (n < 0):
                    error = True
            except ValueError:
                error = True
        else: # if no parameters
            error = True
        if (not error):
            self._fastestLapPoint = n
            # write pickle backup
            self._backup()
        else:
            print("Fastest lap point must be positive integer")
    def help_setPlayersPerRace(self):
        print("Sets the point awarded to the player who posts the fastest lap in the race")
  ###########################
  ### PRINT FUNCTIONS ###
    def do_printNumberOfPlayers(self,s):
        n = str(self._numberOfPlayers)
        print("Number of players: " + n)
    def do_printPlayersPerRace(self,s):
        n = str(self._playersPerRace)
        print("Players per race: " + n)
    def do_printPlayerListFilename(self,s):
        filename = str(self._playerListFilename)
        print("Player names list file: " + filename)
    def do_printRaces(self,s):
        self.printRaces()
    def do_printRacesDone(self,s):
        self.printRacesDone()
    def do_printRacesToDo(self,s):
        self.printRacesToDo()
    def do_printPlayers(self,s):
        self.printPlayers()
    def do_printRaceResults(self,s):
        self.printRaceResults()
    def do_printStanding(self,s):
        self.printStanding()
    def do_printFastestLapStanding(self,s):
        self.printFastestLapStanding()
    def do_printFastestLap(self,s):
        self.printFastestLap()
    def do_printNumberOfRacesOfEachPlayer(self,s):
        self.printNumberOfRacesOfEachPlayer()
    def do_printPlayersFacedByEachPlayer(self,s):
        self.printPlayersFacedByEachPlayer()
  # print function for specific player
    def do_printPlayerNumberOfRaces(self,s):
        self._printPlayerStat(s,self.printPlayerNumberOfRaces)
    def do_printPlayerNumberOfRacesDone(self,s):
        self._printPlayerStat(s,self.printPlayerNumberOfRacesDone)
    def do_printPlayerPlayersFaced(self,s):
        self._printPlayerStat(s,self.printPlayerPlayersFaced)
    def do_printPlayerFastestLap(self,s):
        self._printPlayerStat(s,self.printPlayerFastestLap)
    def do_printPlayerPoints(self,s):
        self._printPlayerStat(s,self.printPlayerPoints)
  #######################

####################

    @property
    def numberOfPlayers(self):
        return self._numberOfPlayers

    @numberOfPlayers.setter
    def numberOfPlayers(self, value):
        if (type(value) is not int) or (value < 0):
            raise ValueError("Number of players must be positive")
        else:
            self._numberOfPlayers = value

    @property
    def playersPerRace(self):
        return self._playersPerRace

    @playersPerRace.setter
    def playersPerRace(self, value):
        if (type(value) is not int) or (value < 0):
            raise ValueError("Players per race must be positive")
        else:
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
    
    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if type(value) is tuple:
            self._points = value
        else:
            raise ValueError("Points must be a tuple of ints, like (4,3,2,1)")
    
    @property
    def fastestLapPoint(self):
        return self._fastestLapPoint
    
    @fastestLapPoint.setter
    def fastestLapPoint(self, value):
        if (type(value) is not int) or (value < 0):
            raise ValueError("Fastest lap point must be positive")
        else:
            self._fastestLapPoint = value
    
    def generateTournament(self,verbose=False,printRacesOnGenerate=False):
        if (self._playersPerRace == None):
            raise ValueError("Players per race must be defined")
        elif (self._points == None):
            raise ValueError("Points must be defined")
        else:
            playerGenerator = None
            # first try with file
            if (self._playerListFilename != None):
                if os.path.isfile(self._playerListFilename) :
                    playerGenerator = PlayerGeneratorFromFile(self._playerListFilename)
            # if no filename or file does not exist
            if (playerGenerator == None):
                if (self._numberOfPlayers  != None):
                    playerGenerator = RandomPlayerGenerator(self._numberOfPlayers)
                else:
                    raise ValueError("Either players list filename or number of players must be defined")
        
        # generate tournament
        self._tournament = Tournament.init_WithPlayerGenerator(playerGenerator,self._points,self._fastestLapPoint)
        # in case tournament set from file
        if (self._numberOfPlayers == None):
            self._numberOfPlayers = self._tournament.getNumberOfPlayers()
        # generate races
        raceGenerator = RaceGenerator(self._playersPerRace,printRacesOnGenerate)
        raceGenerator.generate_lowCostForPlayerWithLeastRaces(self._tournament)
        print("Tournament generated")
        if verbose:
            printRaces(self._tournament.getRaces())
            self._tournament.printNumberOfRacesOfEachPlayer()
            self._tournament.printPlayersFacedByEachPlayer()
            
    def playRace(self,raceNumber):
        if ( (raceNumber < 1) and (raceNumber > len(self._tournament.getRacesToDo())) ):
            print("Wrong race number")
            return False
        i = raceNumber - 1
        race = self._tournament.getRaceToDo(i)
        raceResult = []
        # positions entered, needed to check that the same players won't have same position
        positions = []
        for player in race:
            print(player.getName() + ": ")
            # get position
            positionRaw = input("\tPosition: ")
            # quit playRace
            if (positionRaw == "q"):
                return False
            incorrectNumber = True
            while (incorrectNumber):
                try:
                    position = int(positionRaw)
                    # if position not already set, and position >= 1 and < playersPerRace
                    if ( (position not in positions) and (position > 0) and (position <= self.playersPerRace) ):
                        #found position, add it to positions
                        positions.append(position)
                        incorrectNumber = False
                except ValueError:
                    pass
                if (incorrectNumber):
                    positionRaw = input("\tPosition: ")
                    # quit playRace
                    if (positionRaw == "q"):
                        return False
            # get fastest lap
            fastestLapString = input("\tFastest Lap Time: ")
            # quit playRace
            if (fastestLapString == "q"):
                return False
            incorrectString = True
            while (incorrectString):
                # check correct length  x:xx:xxx  so length 8
                if (len(fastestLapString) == 8):
                    # check 3 number divided by :
                    splitted = fastestLapString.split(":")
                    if (len(splitted) == 3):
                        try:
                            minutes = int(splitted[0])
                            seconds = int(splitted[1])
                            milliseconds = int(splitted[2])
                            # exclude cases with negative seconds or milliseconds (minutes only 1 letter so can't be negative)
                            if (seconds > 0 and milliseconds > 0): 
                                # fastestLapTime correctly parsed, so quit loop
                                incorrectString = False
                        except ValueError:
                            pass
                if (incorrectString):
                    fastestLapString = input("\tFastest Lap Time: ")
                    # quit playRace
                    if (fastestLapString == "q"):
                        return False
            fastestLap = time(0,minutes,seconds,milliseconds*1000) # *1000 because time needs microseconds
            # add race result
            raceResult.append([player,position,fastestLap])
        self._tournament.addRaceResult(raceResult)
        return True
        

            
    def _backup(self,filename="tournament.p"):
        ''' creates a pickle as a backup '''
        pickle.dump(self._tournament,open(filename,"wb"))
        
### PRINT FUNCTIONS ###
    def printRaces(self):
        print("RACES:")
        printRaces(self._tournament.getRaces())

    def printRacesDone(self):
        print("RACES DONE:")
        printRaces(convertRaceResultsToRaces(self._tournament.getRaceResults()))

    def printRacesToDo(self):
        print("RACES TO DO:")
        printRaces(self._tournament.getRacesToDo())

    def printPlayers(self):
        print("PLAYERS:")
        players = self._tournament.players
        players.sort(key=lambda player : player.getName())
        i = 1
        for player in players:
            if (i < 10):
                print(" " + str(i) + ".", player)
            else:
                print(str(i) + ".", player)
            i += 1

    def printRaceResults(self):
        print("RACES RESULTS:")
        i = 1
        for race in self._tournament.getRaceResults():
            print("\tRACE"+str(i)+":")
            j = 1
            for result in race:
                name = result[0].getName()
                if (len(name) < 5):
                    name += " "*(5-len(name))
                print("\t\t" + str(j) + ". " + name + " \t" + lapTimeToStr(result[1]))
                j+=1
            i+=1

    def printStanding(self):
        print("STANDINGS:")
        standings = self._tournament.getStandingsPrintable()
        # find max length of player name
        maxLength = 0
        for player in self._tournament.getPlayers():
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
        standings = self._tournament.getFastestLapStandingPrintable()
        # find max length of player name
        maxLength = 0
        for player in self._tournament.getPlayers():
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

    def printFastestLap(self):
        player = self._tournament.getFastestLapPlayer()
        print("FASTEST LAP:")
        if (player != None):
            print("\t" + player.getName() + ": " + player.getFastestLapPrintable())
        else:
            print("No time")

  # print functions for checking tournament
    def printNumberOfRacesOfEachPlayer(self):
        print("NUMBER OF RACES:")
        self._tournament.printNumberOfRacesOfEachPlayer()

    def printPlayersFacedByEachPlayer(self):
        print("PLAYERS FACED BY EACH PLAYER:")
        self._tournament.printPlayersFacedByEachPlayer()

  # print function for specific player
    def printPlayerNumberOfRaces(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournament.players[playerNumber - 1]
        print("NUMBER OF RACES FOR PLAYER: " + player.getName())
        player.printNumberOfRaces()

    def printPlayerNumberOfRacesDone(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournament.players[playerNumber - 1]
        print("NUMBER OF RACES DONE BY PLAYER: " + player.getName())
        print(str(player.getRacesDone()))
        
    def printPlayerPlayersFaced(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournament.players[playerNumber - 1]
        print("PLAYERS FACED OF PLAYER: " + player.getName())
        player.printPlayersFaced()

    def printPlayerFastestLap(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournament.players[playerNumber - 1]
        print("FASTEST LAP OF PLAYER: " + player.getName())
        print(player.getFastestLapPrintable())

    def printPlayerPoints(self,playerNumber):
        # playerNumber is printed on screen so it is index+1
        player = self._tournament.players[playerNumber - 1]
        print("POINTS OF PLAYER: " + player.getName())
        print(str(player.getPoints()))
#######################

    def _printPlayerStat(self,parameterString,function):
        '''
            checks correctness of player number
            asks the number until number is correct
            calls the function passed as parameter (the stat function)
        '''
        # if no parameter, ask for player number
        if (parameterString == ""):
            self.printPlayers()
            playerNumberRaw = input("Enter number of player: ")
            incorrectNumber = True
            while (incorrectNumber):
                try:
                    playerNumber = int(playerNumberRaw)
                    if ( (playerNumber > 0) and (playerNumber <= self.numberOfPlayers) ):
                        # call stat function
                        function(playerNumber)
                        # end loop
                        incorrectNumber = False
                    else:
                        playerNumberRaw = input("Please enter a correct player number: ")
                except ValueError:
                    playerNumberRaw = input("Please enter a correct player number: ")
        else:
            # get player number from parameters
            parameters = parameterString.split()
            try:
                playerNumber = int(parameters[0])
                if ( (playerNumber > 0) and (playerNumber <= self.numberOfPlayers) ):
                    # call stat function
                    function(playerNumber)
                else:
                    print("Wrong player number")
            except ValueError:
                print("Wrong player number")
