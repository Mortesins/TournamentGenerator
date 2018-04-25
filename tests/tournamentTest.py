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
from tournamentGenerator.tournament import *

from random import shuffle

class TournamentTest(unittest.TestCase):

    def test_addRace(self):
        tournament = Tournament([])
      ### WRONG TYPE ###
        error = False
        try:
            tournament.addRace("gigi")
        except TypeError:
            error = True
        self.assertTrue(error)
        ###
        error = False
        try:
            tournament.addRace(Player("A"))
        except TypeError:
            error = True
        self.assertTrue(error)
      ### RIGHT TYPE, CHECK NUMBER OF RACES AND PLAYERS FACE EACH OTHER###
        a = Player("A")
        error = False
        try:
            tournament.addRace([a])
        except TypeError:
            error = True
        self.assertFalse(error)
        self.assertEqual(a.getRaces(),1)
        ###
        a = Player("A")
        b = Player("B")
        error = False
        try:
            tournament.addRace([a,b])
        except TypeError:
            error = True
        self.assertFalse(error)
        self.assertEqual(a.getRaces(),1)
        self.assertEqual(b.getRaces(),1)
        self.assertTrue(a.hasFaced(b))
        self.assertTrue(b.hasFaced(a))
        ###
        a = Player("A")
        b = Player("B")
        c = Player("C")
        error = False
        try:
            tournament.addRace([a,b])
            tournament.addRace([a,c])
            tournament.addRace([a,b,c])
        except TypeError:
            error = True
        self.assertFalse(error)
        self.assertEqual(a.getRaces(),3)
        self.assertEqual(b.getRaces(),2)
        self.assertEqual(b.getRaces(),2)
        self.assertTrue(a.hasFaced(b))
        self.assertTrue(a.hasFaced(c))
        self.assertTrue(b.hasFaced(a))
        self.assertTrue(c.hasFaced(a))
        self.assertTrue(b.hasFaced(c))
        self.assertEqual(a.numberOfTimesAlreadyFaced(b),2)
        self.assertEqual(b.numberOfTimesAlreadyFaced(a),2)
        self.assertEqual(a.numberOfTimesAlreadyFaced(c),2)
        self.assertEqual(c.numberOfTimesAlreadyFaced(a),2)
        self.assertEqual(b.numberOfTimesAlreadyFaced(c),1)
        self.assertEqual(c.numberOfTimesAlreadyFaced(b),1)
        
    def test_init_GeneratePlayers(self):
        tournament = Tournament.init_GeneratePlayers(5)
        self.assertEqual(len(tournament.players),5)
        self.assertEqual(tournament.players[0].getName(),"A")
        self.assertEqual(tournament.players[1].getName(),"B")
        self.assertEqual(tournament.players[2].getName(),"C")
        self.assertEqual(tournament.players[3].getName(),"D")
        self.assertEqual(tournament.players[4].getName(),"E")
        tournament = Tournament.init_GeneratePlayers(26)
        self.assertEqual(len(tournament.players),26)
        self.assertEqual(tournament.players[0].getName(),"A")
        self.assertEqual(tournament.players[25].getName(),"Z")
        tournament = Tournament.init_GeneratePlayers(104)
        self.assertEqual(len(tournament.players),104)
        self.assertEqual(tournament.players[0].getName(),"AA")
        self.assertEqual(tournament.players[50].getName(),"BY")
        self.assertEqual(tournament.players[103].getName(),"DZ")
        
    def test_raceExists(self):
        tournament = Tournament.init_GeneratePlayers(5)
        race1 = [tournament.players[0],tournament.players[1],tournament.players[2]]
        race2 = [tournament.players[3],tournament.players[4],tournament.players[0]]
        race1copy = list(race1)
        race2copy = list(race2)
        tournament.addRace(race1)
        shuffle(race1copy)
        self.assertTrue(tournament.raceExists(race1copy))
        self.assertFalse(tournament.raceExists(race2copy))
        tournament.addRace(race2)
        shuffle(race1copy)
        shuffle(race2copy)
        self.assertTrue(tournament.raceExists(race1copy))
        self.assertTrue(tournament.raceExists(race2copy))
        self.assertTrue(tournament.raceExists([tournament.players[4],tournament.players[0],tournament.players[3]]))
        self.assertFalse(tournament.raceExists([tournament.players[1],tournament.players[4],tournament.players[0]]))
        
    def test_playersSameNumberOfRaces(self):
      # three players per race
        # 3 players (ABC)
        tournament = Tournament.init_GeneratePlayers(3)
        # add ABC
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[2]])
        # ABC, so true
        self.assertTrue(tournament.playersSameNumberOfRaces())
        # 4 players (ABCD)
        tournament = Tournament.init_GeneratePlayers(4)
        # add ABC
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[2]])
        # only ABC, so false
        self.assertFalse(tournament.playersSameNumberOfRaces())
        # add ABD
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[3]])
        # only ABC, ABD, so false
        self.assertFalse(tournament.playersSameNumberOfRaces())
        # add BCD
        tournament.addRace([tournament.players[1],tournament.players[2],tournament.players[3]])
        # only ABC, ABD, BCD so false
        self.assertFalse(tournament.playersSameNumberOfRaces())
        # add ACD
        tournament.addRace([tournament.players[0],tournament.players[2],tournament.players[3]])
        # ABC, ABD, BCD, ACD so true
        self.assertTrue(tournament.playersSameNumberOfRaces())
      # two players per race
        # 3 players (ABC)
        tournament = Tournament.init_GeneratePlayers(3)
        # add AB
        tournament.addRace([tournament.players[0],tournament.players[1]])
        # only AB, so false
        self.assertFalse(tournament.playersSameNumberOfRaces())
        # add AC
        tournament.addRace([tournament.players[0],tournament.players[2]])
        # only AB, AC so false
        self.assertFalse(tournament.playersSameNumberOfRaces())
        # add BC
        tournament.addRace([tournament.players[1],tournament.players[2]])
        # AB, AC, BC so true
        self.assertTrue(tournament.playersSameNumberOfRaces())
      # four players per race
        # 8 players (ABCDEFGH)
        tournament = Tournament.init_GeneratePlayers(8)
        # add ABCD
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[2],tournament.players[3]])
        # only ABCD, so false
        self.assertFalse(tournament.playersSameNumberOfRaces())
        # add EFGH
        tournament.addRace([tournament.players[4],tournament.players[5],tournament.players[6],tournament.players[7]])
        # ABCD, EFGH so true
        self.assertTrue(tournament.playersSameNumberOfRaces())
    
    def test_somebodyDidNotFaceEveryone(self):
      # three players per race
        # 3 players (ABC)
        tournament = Tournament.init_GeneratePlayers(3)
        # add ABC
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[2]])
        # ABC, so everyone faced everyone, so false
        self.assertFalse(tournament.somebodyDidNotFaceEveryone())
        # 4 players (ABCD)
        tournament = Tournament.init_GeneratePlayers(4)
        # add ABC
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[2]])
        # only ABC, so nobody faced D, so true
        self.assertTrue(tournament.somebodyDidNotFaceEveryone())
        # add ABD
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[3]])
        # only ABC, ABD, C did not face D, so true 
        self.assertTrue(tournament.somebodyDidNotFaceEveryone())
        # add BCD
        tournament.addRace([tournament.players[1],tournament.players[2],tournament.players[3]])
        # only ABC, ABD, BCD, everyone faced everyone, so false
        self.assertFalse(tournament.somebodyDidNotFaceEveryone())
        # add ACD
        tournament.addRace([tournament.players[0],tournament.players[2],tournament.players[3]])
        # ABC, ABD, BCD, ACD, everyone faced everyone, so false
        self.assertFalse(tournament.somebodyDidNotFaceEveryone())
    # two players per race
        # 3 players (ABC)
        tournament = Tournament.init_GeneratePlayers(3)
        # add AB
        tournament.addRace([tournament.players[0],tournament.players[1]])
        # only AB, so C did not face A and B, so true
        self.assertTrue(tournament.somebodyDidNotFaceEveryone())
        # add AC
        tournament.addRace([tournament.players[0],tournament.players[2]])
        # only AB, AC so B did not face C, so true
        self.assertTrue(tournament.somebodyDidNotFaceEveryone())
        # add BC
        tournament.addRace([tournament.players[1],tournament.players[2]])
        # AB, AC, BC so everyone faced everyone, so false
        self.assertFalse(tournament.somebodyDidNotFaceEveryone())

    def test_averageNumberOfRaces(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        # add ABC
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[2]])
        self.assertEqual(tournament.averageNumberOfRaces(),3.0/5)
        # add ABD
        tournament.addRace([tournament.players[0],tournament.players[1],tournament.players[3]])
        self.assertEqual(tournament.averageNumberOfRaces(),6.0/5)
        # add BCD
        tournament.addRace([tournament.players[1],tournament.players[2],tournament.players[3]])
        self.assertEqual(tournament.averageNumberOfRaces(),9.0/5)
        # add ACD
        tournament.addRace([tournament.players[0],tournament.players[2],tournament.players[3]])
        self.assertEqual(tournament.averageNumberOfRaces(),12.0/5)

    def test_costOfRace(self):
        '''
            ABCDE:
                ABC costs: 
                    -differential:  1+1+1 - (3*0) = 3
                    -refacing:      0
                add ABC
                CDE costs:
                    -differential:  2+1+1 - (3*3/5) = 2.2
                    -refacing:      0
                add CDE
                    BCD costs:
                        -differential:  2+3+2 - (3*6/5) = 3.4
                        -refacing:      3+3
                            BC, CD
                    ABE costs:
                        -differential:  2+2+2 - (3*6/5) = 2.4
                        -refacing:      3
                            AB
                    ABC costs:
                        -differential   2+2+3 - (3*6/5) = 3.4
                        -refacing:      3+3+3
                            AB,BC,AC
                add ABE (ABC,ABE,CDE)
                    DAB costs:
                        -differential   2+3+3 - (3*9/5) = 2.59
                        -refacing:      3^2
                            AB*2
                    DAC costs:
                        -differential   2+3+3 - (3*9/5) = 2.59
                        -refacing:      3+3
                            AC,CD
                    DBE costs:
                        -differential   2+3+3 - (3*9/5) = 2.59
                        -refacing:      3+3
                            BE,ED
        '''
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        ABC = [A,B,C]
        CDE = [C,D,E]
        BCD = [B,C,D]
        ABE = [A,B,E]
        DAB = [D,A,B]
        DAC = [D,A,C]
        DBE = [D,B,E]
        # COSTS
        self.assertEqual(tournament.costOfRace(ABC),3)
      # add ABC
        tournament.addRace(ABC)
        self.assertEqual(round(tournament.costOfRace(CDE),5),round(2+1+1-3*3.0/5, 5))
      # add CDE
        tournament.addRace(CDE)
        self.assertEqual(round(tournament.costOfRace(BCD),5),round(3.4+3+3, 5))
        self.assertEqual(round(tournament.costOfRace(ABE),5),round(2.4+3, 5))
        self.assertEqual(round(tournament.costOfRace(ABC),5),round(3.4+3+3+3, 5))
      # add ABE
        tournament.addRace(ABE)
        self.assertEqual(round(tournament.costOfRace(DAB),5),round(2+3+3-(3*9.0/5)+pow(3,2), 5))
        self.assertEqual(round(tournament.costOfRace(DAC),5),round(2+3+3-(3*9.0/5)+pow(3,1)+pow(3,1), 5))
        self.assertEqual(round(tournament.costOfRace(DBE),5),round(2+3+3-(3*9.0/5)+pow(3,1)+pow(3,1), 5))

    def test_getPlayerThatHasntFacedEveryone(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        # should be A because returns the first player that hasn't faced everyone
        self.assertEqual(tournament.getPlayerThatHasntFacedEveryone(),tournament.players[0])
      # add ABC
        tournament.addRace([A,B,C])
      # add ADE
        tournament.addRace([A,D,E])
        # should be B because returns the first player that hasn't faced everyone
        self.assertEqual(tournament.getPlayerThatHasntFacedEveryone(),tournament.players[1])
      # add BDE
        tournament.addRace([B,D,E])
        # should be C because returns the first player that hasn't faced everyone
        self.assertEqual(tournament.getPlayerThatHasntFacedEveryone(),tournament.players[2])
    # add CDE
        tournament.addRace([C,D,E])
        # should return None, since all players have faced each other
        self.assertEqual(tournament.getPlayerThatHasntFacedEveryone(),None)

    def test_getRandomPlayerThatHasntFacedEveryone(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        # length of players not faced should be higher than 0
        self.assertTrue( len(tournament.getRandomPlayerThatHasntFacedEveryone().playersNotFaced(tournament.players)) > 0 )
      # add ABC
        tournament.addRace([A,B,C])
      # add ADE
        tournament.addRace([A,D,E])
        # length of players not faced should be higher than 0
        self.assertTrue( len(tournament.getRandomPlayerThatHasntFacedEveryone().playersNotFaced(tournament.players)) > 0 )
      # add BDE
        tournament.addRace([B,D,E])
        # length of players not faced should be higher than 0
        self.assertTrue( len(tournament.getRandomPlayerThatHasntFacedEveryone().playersNotFaced(tournament.players)) > 0 )
      # add CDE
        tournament.addRace([C,D,E])
        # should return None, since all players have faced each other
        self.assertEqual(tournament.getRandomPlayerThatHasntFacedEveryone(),None)

    def test_addRaceResult(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
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
            
        self.assertEqual(\
            tournament.getRaceResult(0),\
            [\
                (A,time(0,1,21,340000)),\
                (E,time(0,1,21,484000)),\
                (D,time(0,1,23,000000)),\
                (B,time(0,1,22,450000))\
            ]\
        )
        self.assertEqual(A.getFastestLap(),time(0,1,21,340000))
        self.assertEqual(B.getFastestLap(),time(0,1,22,450000))
        self.assertEqual(D.getFastestLap(),time(0,1,23,000000))
        self.assertEqual(E.getFastestLap(),time(0,1,21,484000))
        self.assertEqual(A.getPoints(),5) # +1 for fastest lap
        self.assertEqual(B.getPoints(),1)
        self.assertEqual(D.getPoints(),2)
        self.assertEqual(E.getPoints(),3)

        tournament.addRaceResult(\
            [\
                (A,2,time(0,1,21,300000)),\
                (B,3,time(0,1,21,450000)),\
                (C,1,time(0,1,20,984000)),\
                (D,4,time(0,1,24,000000))\
            ]\
        )
            
        self.assertEqual(\
            tournament.getRaceResult(1),\
            [\
                (C,time(0,1,20,984000)),\
                (A,time(0,1,21,300000)),\
                (B,time(0,1,21,450000)),\
                (D,time(0,1,24,000000))\
            ]\
        )
        self.assertEqual(A.getFastestLap(),time(0,1,21,300000))
        self.assertEqual(B.getFastestLap(),time(0,1,21,450000))
        self.assertEqual(C.getFastestLap(),time(0,1,20,984000))
        self.assertEqual(D.getFastestLap(),time(0,1,23,000000))
        self.assertEqual(E.getFastestLap(),time(0,1,21,484000))
        self.assertEqual(A.getPoints(),8)
        self.assertEqual(B.getPoints(),3)
        self.assertEqual(C.getPoints(),5) # +1 for fastest lap
        self.assertEqual(D.getPoints(),3)
        self.assertEqual(E.getPoints(),3)

### HELPER FUNCTION ###
    def generateRaceResult1(self,tournament):
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

    def generateRaceResult2(self,tournament):
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        tournament.addRaceResult(\
            [\
                (A,2,time(0,1,21,300000)),\
                (B,3,time(0,1,21,450000)),\
                (C,1,time(0,1,20,984000)),\
                (D,4,time(0,1,24,000000))\
            ]\
        )

    def generateRaceResult3(self,tournament):
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        tournament.addRaceResult(\
            [\
                (C,1,time(0,1,25,300000)),\
                (B,3,time(0,1,25,450000)),\
                (D,2,time(0,1,25,984000)),\
                (E,4,time(0,1,26,000000))\
            ]\
        )

    def test_getFastestLapTime(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        self.generateRaceResult1(tournament)
        self.assertEqual(tournament.getFastestLapTime(),time(0,1,21,340000))
        self.generateRaceResult2(tournament)
        self.assertEqual(tournament.getFastestLapTime(),time(0,1,20,984000))

    def test_getFastestLapPlayer(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        self.generateRaceResult1(tournament)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        self.assertEqual(tournament.getFastestLapPlayer(),A)
        self.generateRaceResult2(tournament)
        self.assertEqual(tournament.getFastestLapPlayer(),C)

    def test_getFastestLapStanding(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        self.generateRaceResult1(tournament)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        self.assertEqual(tournament.getFastestLapStanding(),[A,E,B,D])
        self.generateRaceResult2(tournament)
        self.assertEqual(tournament.getFastestLapStanding(),[C,A,B,E,D])

    def test_getStandings(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        self.generateRaceResult1(tournament)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        self.assertEqual(tournament.getStandings(),[A,E,D,B,C])
        self.generateRaceResult2(tournament)
        self.generateRaceResult3(tournament)
        self.assertEqual(tournament.getStandings(),[C,A,D,B,E])

    def test_getFastestLapStandingPrintable(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        self.generateRaceResult1(tournament)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        self.assertEqual(\
            tournament.getFastestLapStandingPrintable(),\
            [\
                ("A","1:21:340"),\
                ("E","1:21:484"),\
                ("B","1:22:450"),\
                ("D","1:23:000")\
            ]\
        )
                
        self.generateRaceResult2(tournament)
        self.generateRaceResult3(tournament)
        self.assertEqual(\
            tournament.getFastestLapStandingPrintable(),\
            [\
                ("C","1:20:984"),\
                ("A","1:21:300"),\
                ("B","1:21:450"),\
                ("E","1:21:484"),\
                ("D","1:23:000")\
            ]\
        )
    
    def test_getStandingsPrintable(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        self.generateRaceResult1(tournament)
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        self.assertEqual(\
            tournament.getStandingsPrintable(),\
            [\
                ("A",1,5),\
                ("E",1,3),\
                ("D",1,2),\
                ("B",1,1),\
                ("C",0,0)\
            ]\
        )
        self.generateRaceResult2(tournament)
        self.generateRaceResult3(tournament)
        self.assertEqual(\
            tournament.getStandingsPrintable(),\
            [\
                ("C",2,10),\
                ("A",2,8),\
                ("D",3,6),\
                ("B",3,5),\
                ("E",2,4)\
            ]\
        )
    
    def test_getRacesToDo1(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        # add races
        tournament.addRace([A,B,C,D])
        tournament.addRace([A,B,C,E])
        tournament.addRace([B,C,D,E])
        tournament.addRace([A,C,D,E])
        tournament.addRace([A,B,D,E])
        
        self.assertEqual(\
            tournament.getRacesToDo(),\
            [\
                [A,B,C,D],\
                [A,B,C,E],\
                [B,C,D,E],\
                [A,C,D,E],\
                [A,B,D,E]\
            ]\
        )
        # add race result
        tournament.addRaceResult(\
            [\
                (A,1,time(0,1,21,340000)),\
                (B,4,time(0,1,22,450000)),\
                (E,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        
        self.assertEqual(\
            tournament.getRacesToDo(),\
            [\
                [A,B,C,D],\
                [A,B,C,E],\
                [B,C,D,E],\
                [A,C,D,E]\
            ]\
        )
        # add race result
        tournament.addRaceResult(\
            [\
                (A,1,time(0,1,21,340000)),\
                (B,4,time(0,1,22,450000)),\
                (C,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        
        self.assertEqual(\
            tournament.getRacesToDo(),\
            [\
                [A,B,C,E],\
                [B,C,D,E],\
                [A,C,D,E]\
            ]\
        )
        # add race result
        tournament.addRaceResult(\
            [\
                (B,1,time(0,1,21,340000)),\
                (E,4,time(0,1,22,450000)),\
                (C,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        
        self.assertEqual(\
            tournament.getRacesToDo(),\
            [\
                [A,B,C,E],\
                [A,C,D,E]\
            ]\
        )

    def test_getRacesToDo2(self):
        # 5 players (ABCDE)
        tournament = Tournament.init_GeneratePlayers(5,(4,3,2,1))
        A = tournament.players[0]
        B = tournament.players[1]
        C = tournament.players[2]
        D = tournament.players[3]
        E = tournament.players[4]
        # add races
        tournament.addRace([A,B,C,D])
        tournament.addRace([A,B,C,E])
        tournament.addRace([B,C,D,E])
        tournament.addRace([A,C,D,E])
        tournament.addRace([A,B,D,E])
        
        self.assertEqual(\
            tournament.getRacesToDo(),\
            [\
                [A,B,C,D],\
                [A,B,C,E],\
                [B,C,D,E],\
                [A,C,D,E],\
                [A,B,D,E]\
            ]\
        )
        # add race result
        tournament.addRaceResult(\
            [\
                (A,1,time(0,1,21,340000)),\
                (B,4,time(0,1,22,450000)),\
                (E,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        # add race result
        tournament.addRaceResult(\
            [\
                (A,1,time(0,1,21,340000)),\
                (B,4,time(0,1,22,450000)),\
                (C,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        # add race result
        tournament.addRaceResult(\
            [\
                (B,1,time(0,1,21,340000)),\
                (E,4,time(0,1,22,450000)),\
                (C,2,time(0,1,21,484000)),\
                (D,3,time(0,1,23,000000))\
            ]\
        )
        
        self.assertEqual(\
            tournament.getRacesToDo(),\
            [\
                [A,B,C,E],\
                [A,C,D,E]\
            ]\
        )
