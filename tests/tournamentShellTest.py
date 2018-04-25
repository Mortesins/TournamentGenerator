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

from tournamentGenerator.tournamentShell import *

from random import shuffle, randint

class TournamentShellTest():

    def _generateRaceResult1(self,tournament):
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        tournament.addRaceResult(\
            [\
                (A,1,time(0,1,21,340000)),\
                (B,4,time(0,1,22,450000)),\
                (E,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        return
    
    def _generateRaceResult2(self,tournament):
        A = tournament.players[0]
        C = tournament.players[2]
        D = tournament.players[3]
        F = tournament.players[5]
        tournament.addRaceResult(\
            [\
                (A,1,time(0,1,21,340000)),\
                (F,2,time(0,1,22,450000)),\
                (C,3,time(0,1,21,484000)),\
                (D,4,time(0,1,23,111000))\
            ]\
        )
        return

    def _generateCoherentRaceResult(self,tournament):
        races = tournament.getRaces()
        randomRaceIndex = randint(0,len(races)-1)
        # adds race result with players of random race
             # tournament[randomRaceIndex][0] = first player of random race
        tournament.addRaceResult(\
            [\
                (races[randomRaceIndex][0],1,time(0,1,21,340000)),\
                (races[randomRaceIndex][1],2,time(0,1,22,450000)),\
                (races[randomRaceIndex][2],3,time(0,1,21,484000)),\
                (races[randomRaceIndex][3],4,time(0,1,23,111000))\
            ]\
        )
        return

    def test1(self):
        a = TournamentShell()
        a.playersPerRace = 4
        a.numberOfPlayers = 10
        a.points = (4,3,2,1)
        a.generateTournament()
    
        a.printStanding()
        a.printFastestLapStanding()
    
        
        a.printRaces()
        a.printRacesDone()
        a.printRacesToDo()
        self._generateCoherentRaceResult(a._tournamentGenerator.tournament)
        a.printRacesDoneCompact()
        a.printRacesDone()
        a.printRacesToDo()
        self._generateCoherentRaceResult(a._tournamentGenerator.tournament)
        a.printRacesDoneCompact()
        a.printRacesToDo()
        a.printRacesDone()
        
        a.printPlayers()
        a.printPlayersFacedByEachPlayer()
        a.printNumberOfRacesOfEachPlayer()
        a.printPlayerNumberOfRaces(2)
        a.printPlayerPlayersFaced(2)
        a.printPlayerNumberOfRacesDone(2)
        a.printPlayerFastestLap(2)
        a.printPlayerPoints(2)
        a.printStanding()
        a.printFastestLapStanding()
