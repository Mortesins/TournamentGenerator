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
from tournamentGenerator.raceCosts import *

from tournamentGenerator.tournament import *
from random import shuffle

class RaceCostsTest(unittest.TestCase):
    def test_leastExpensiveRaces_fixedPlayer(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
      # 3 players per race
        # all the races cost the same, so should have 4*3/2 races (all combinations of two players, since one is fixed)
        players = list(tournament.players)
        players.remove(A) # because I fix A
        self.assertEquals(len(leastExpensiveRaces(players,3,tournament.averageNumberOfRaces(),[A])),4*3/2)
      # add ABC
        tournament.addRace([A,B,C])
        # least expensive ADE,BDE,CDE
        # fix A or B or C, length 1
        players = list(tournament.players)
        players.remove(A) # because I fix A
        self.assertEquals(len(leastExpensiveRaces(players,3,tournament.averageNumberOfRaces(),[A])),1)
        players = list(tournament.players)
        players.remove(B) # because I fix B
        self.assertEquals(len(leastExpensiveRaces(players,3,tournament.averageNumberOfRaces(),[B])),1)
        players = list(tournament.players)
        players.remove(C) # because I fix C
        self.assertEquals(len(leastExpensiveRaces(players,3,tournament.averageNumberOfRaces(),[C])),1)
        # fix E or D, length 3
        players = list(tournament.players)
        players.remove(D) # because I fix D
        self.assertEquals(len(leastExpensiveRaces(players,3,tournament.averageNumberOfRaces(),[D])),3)
        players = list(tournament.players)
        players.remove(E) # because I fix E
        self.assertEquals(len(leastExpensiveRaces(players,3,tournament.averageNumberOfRaces(),[E])),3)
      # 4 players per race
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        # all the races cost the same, so should have 2 races since three players are fixed (ABCD ABCE)
        players = list(tournament.players)
        players.remove(A) # because I fix A
        players.remove(B) # because I fix B
        players.remove(C) # because I fix C
        self.assertEquals(len(leastExpensiveRaces(players,4,tournament.averageNumberOfRaces(),[A,B,C])),2)
        # all the races cost the same, so should have 3*2/(2) races (all combinations of two players, since two are fixed)
        players = list(tournament.players)
        players.remove(A) # because I fix A
        players.remove(B) # because I fix B
        self.assertEquals(len(leastExpensiveRaces(players,4,tournament.averageNumberOfRaces(),[A,B])),3)
        # 6 players (ABCDEF)
        tournament = Tournament.init_GeneratePlayers(6)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        F = tournament.players[5]
        # all the races cost the same, so should have 5*4*3/3*2 races (all combinations of two players, since one player is fixed, A)
        players = list(tournament.players)
        players.remove(A) # because I fix A
        self.assertEquals(len(leastExpensiveRaces(players,4,tournament.averageNumberOfRaces(),[A])),10)
      # add ABC
        tournament.addRace([A,B,C,D])
        # I fix A,E,F, so races are ABEF,ACEF,ADEF and should all have the same cost
        players = list(tournament.players)
        players.remove(A) # because I fix A
        players.remove(E) # because I fix E
        players.remove(F) # because I fix F
        self.assertEquals(len(leastExpensiveRaces(players,4,tournament.averageNumberOfRaces(),[A,E,F])),3)


    def test_leastExpensiveRaces_noFixedPlayer(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
      # 3 players per race
        # all the races cost the same, so should have 5*4*3/(3*2) races (all combinations of two players, since one is fixed)
        self.assertEquals(len(leastExpensiveRaces(tournament.players,3,tournament.averageNumberOfRaces())),10)
      # add ABC
        tournament.addRace([A,B,C])
        # least expensive ADE,BDE,CDE
        self.assertEquals(len(leastExpensiveRaces(tournament.players,3,tournament.averageNumberOfRaces())),3)
      # 4 players per race
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        # all the races cost the same, so should have 5*4*3*2/(2*3*4) races (all combinations of three players, since one is fixed)
        self.assertEquals(len(leastExpensiveRaces(tournament.players,4,tournament.averageNumberOfRaces())),5)
