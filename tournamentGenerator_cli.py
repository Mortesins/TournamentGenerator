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

import unittest
import sys

from tournamentGenerator import TournamentGenerator

if __name__ == '__main__':
    if len(sys.argv) == 4:
        debug = bool(sys.argv[3])
    elif len(sys.argv) == 3:
        debug = False
    else:
        print("tournamentGenerator.py: missing arguments")
        print("Usage: python tournamentGenerator.py NUMBER_PLAYERS_PER_RACE PLAYERS_NAME_FILE/NUMBER_OF_PLAYERS [DEBUG]")
        sys.exit()
    
    numberOfPlayers = 0
    playersPerRace = int(sys.argv[1])
    try:
        numberOfPlayers = int(sys.argv[2])
    except ValueError:
        filename = sys.argv[2]
    
    if numberOfPlayers == 0:
        tournament = TournamentGenerator.init_fromFile(playersPerRace,filename,debug)
    else:
        tournament = TournamentGenerator.init_GenerateTournament(numberOfPlayers,playersPerRace,False)
    
    tournament.generate2()
    tournament.printTournament()
    tournament.printNumberOfRacesOfEachPlayer()
    tournament.printPlayersFacedByEachPlayer()
