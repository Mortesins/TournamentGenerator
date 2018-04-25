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

import unittest
from tournamentGenerator.helper import *
from tournamentGenerator.player import Player
from datetime import time

class PlayerTest(unittest.TestCase):

    def test_sameRace(self):
        A = Player("A")
        B = Player("B")
        C = Player("C")
        D = Player("D")
        E = Player("E")
        self.assertTrue(sameRace([A,B,C,D],[A,D,C,B]))
        self.assertTrue(sameRace([A,B,C,D],[D,C,A,B]))
        self.assertTrue(sameRace([A,B,C,D],[B,A,D,C]))
        self.assertTrue(sameRace([B,A,D,C],[A,B,C,D]))
        self.assertFalse(sameRace([A,B,C,D],[B,A,E,C]))
        self.assertFalse(sameRace([A,B,C,D],[A,B,C,E]))

    def test_convertRaceResultToRace(self):
        A = Player("A")
        B = Player("B")
        C = Player("C")
        D = Player("D")
        E = Player("E")
        raceResult =\
            [\
                (A,1,time(0,1,21,340000)),\
                (B,4,time(0,1,22,450000)),\
                (E,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        
        self.assertEqual(convertRaceResultToRace(raceResult),[A,B,E,D])

    def test_convertRaceResultsToRaces(self):
        A = Player("A")
        B = Player("B")
        C = Player("C")
        D = Player("D")
        E = Player("E")
        raceResults =\
            [\
                [\
                    (A,1,time(0,1,21,340000)),\
                    (B,4,time(0,1,22,450000)),\
                    (E,2,time(0,1,21,484000)),\
                    (D,3,time(0,1,23,000000))\
                ],\
                [\
                    (C,1,time(0,1,21,340000)),\
                    (B,4,time(0,1,22,450000)),\
                    (A,2,time(0,1,21,484000)),\
                    (E,3,time(0,1,23,000000))\
                ],\
                [\
                    (E,1,time(0,1,21,340000)),\
                    (B,4,time(0,1,22,450000)),\
                    (C,2,time(0,1,21,484000)),\
                    (D,3,time(0,1,23,000000))\
                ],\
            ]
        
        self.assertEqual(\
            convertRaceResultsToRaces(raceResults),\
            [\
                [A,B,E,D],\
                [C,B,A,E],\
                [E,B,C,D]\
            ]\
        )
