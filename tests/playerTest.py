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
from tournamentGenerator.player import *

class PlayerTest(unittest.TestCase):
    def _return10players(self):
        players = []
        for letter in ["A","B","C","D","E","F","G","H","I","J"]:
            players.append(Player(letter))
        return players
    
    def _addNracesToIthPlayer(self,players,i,n):
        for j in range(0,n):
            players[i].addRace()
        return

    def test_addNracesToIthPlayer(self):
        players = self._return10players()
        self._addNracesToIthPlayer(players,0,9)
        self.assertEqual(players[0].getRaces(),9)
        self._addNracesToIthPlayer(players,3,9)
        self.assertEqual(players[3].getRaces(),9)
        self._addNracesToIthPlayer(players,5,1)
        self.assertEqual(players[5].getRaces(),1)
        
####################
### PLAYER CLASS ###
####################
    def test_hasFaced(self):
        playerA = Player("A")
        playerB = Player("B")
        playerA.addFacedPlayer(playerB)
        self.assertTrue(playerA.hasFaced(playerB))
        self.assertFalse(playerA.hasFaced(Player("C")))

    def test_numberOfTimesAlreadyFaced(self):
        playerA = Player("A")
        playerB = Player("B")
        playerC = Player("C")
        playersFaceEachOther(playerA,playerB)
        playersFaceEachOther(playerA,playerB)
        playersFaceEachOther(playerA,playerB)
        playersFaceEachOther(playerB,playerC)
        self.assertEqual(playerA.numberOfTimesAlreadyFaced(playerB),3)
        self.assertEqual(playerB.numberOfTimesAlreadyFaced(playerA),3)
        self.assertEqual(playerB.numberOfTimesAlreadyFaced(playerC),1)
        self.assertEqual(playerC.numberOfTimesAlreadyFaced(playerB),1)
        self.assertEqual(playerA.numberOfTimesAlreadyFaced(playerC),0)
        self.assertEqual(playerC.numberOfTimesAlreadyFaced(playerA),0)
        playersFaceEachOther(playerA,playerC)
        self.assertEqual(playerA.numberOfTimesAlreadyFaced(playerC),1)
        self.assertEqual(playerC.numberOfTimesAlreadyFaced(playerA),1)
        self.assertEqual(playerA.numberOfTimesAlreadyFaced(playerB),3)
        self.assertEqual(playerB.numberOfTimesAlreadyFaced(playerA),3)
        self.assertEqual(playerB.numberOfTimesAlreadyFaced(playerC),1)
        self.assertEqual(playerC.numberOfTimesAlreadyFaced(playerB),1)

    def test_numberPlayersFaced(self):
        playerA = Player("A")
        playerA.addFacedPlayer(Player("B"))
        playerA.addFacedPlayer(Player("C"))
        playerA.addFacedPlayer(Player("D"))
        self.assertEqual(playerA.numberPlayersFaced(),3)

    def test_playersNotFaced(self):
        players = [Player("A"),Player("B"),Player("C"),Player("D")]
        # AvsB
        playersFaceEachOther(players[0],players[1])
        # A has not faced C D
        self.assertEqual(players[0].playersNotFaced(players),[players[2],players[3]])
        # B has not faced C D
        self.assertEqual(players[1].playersNotFaced(players),[players[2],players[3]])
        # C has not faced A B D
        self.assertEqual(players[2].playersNotFaced(players),[players[0],players[1],players[3]])
        # D has not faced A B C
        self.assertEqual(players[3].playersNotFaced(players),[players[0],players[1],players[2]])
        # CvsD
        playersFaceEachOther(players[2],players[3])
        # A has not faced C D
        self.assertEqual(players[0].playersNotFaced(players),[players[2],players[3]])
        # B has not faced C D
        self.assertEqual(players[1].playersNotFaced(players),[players[2],players[3]])
        # C has not faced A B
        self.assertEqual(players[2].playersNotFaced(players),[players[0],players[1]])
        # D has not faced A B
        self.assertEqual(players[3].playersNotFaced(players),[players[0],players[1]])
        # BvsC tre volte (potrebbe capitare se fanno piu' gare insieme)
        playersFaceEachOther(players[1],players[2])
        playersFaceEachOther(players[1],players[2])
        playersFaceEachOther(players[1],players[2])
        # A has not faced C D
        self.assertEqual(players[0].playersNotFaced(players),[players[2],players[3]])
        # B has not faced D
        self.assertEqual(players[1].playersNotFaced(players),[players[3]])
        # C has not faced A B
        self.assertEqual(players[2].playersNotFaced(players),[players[0]])
        # D has not faced A B
        self.assertEqual(players[3].playersNotFaced(players),[players[0],players[1]])
        # BvsD due volte (potrebbe capitare se fanno piu' gare insieme)
        playersFaceEachOther(players[1],players[3])
        playersFaceEachOther(players[1],players[3])
        # A has not faced C D
        self.assertEqual(players[0].playersNotFaced(players),[players[2],players[3]])
        # B has faced everyone
        self.assertEqual(players[1].playersNotFaced(players),[])
        # C has not faced A B
        self.assertEqual(players[2].playersNotFaced(players),[players[0]])
        # D has not faced A B
        self.assertEqual(players[3].playersNotFaced(players),[players[0]])

###############################
### PLAYER HELPER FUNCTIONS ###
###############################
    def test_playersFaceEachOther(self):
        playerA = Player("A")
        playerB = Player("B")
        self.assertFalse(playerA.hasFaced(playerB))
        self.assertFalse(playerB.hasFaced(playerA))
        playersFaceEachOther(playerA,playerB)
        self.assertTrue(playerA.hasFaced(playerB))
        self.assertTrue(playerB.hasFaced(playerA))

    def test_playersWithLeastRaces1(self):
        players = self._return10players()
        # 1,2,4,4,7,7,7,8,8,9
        self._addNracesToIthPlayer(players,0,9)
        self._addNracesToIthPlayer(players,1,1)
        self._addNracesToIthPlayer(players,2,7)
        self._addNracesToIthPlayer(players,3,2)
        self._addNracesToIthPlayer(players,4,8)
        self._addNracesToIthPlayer(players,5,4)
        self._addNracesToIthPlayer(players,6,7)
        self._addNracesToIthPlayer(players,7,7)
        self._addNracesToIthPlayer(players,8,4)
        self._addNracesToIthPlayer(players,9,8)
        
        playersLeastRaces = playersWithLeastRaces(players)
        self.assertEqual(len(playersLeastRaces),1)
        self.assertEqual(playersLeastRaces[0].getRaces(),1)
     
    def test_playersWithLeastRaces2(self):
        players = self._return10players()
        # 2,2,4,4,7,7,7,8,8,9
        self._addNracesToIthPlayer(players,0,9)
        self._addNracesToIthPlayer(players,1,2)
        self._addNracesToIthPlayer(players,2,7)
        self._addNracesToIthPlayer(players,3,2)
        self._addNracesToIthPlayer(players,4,8)
        self._addNracesToIthPlayer(players,5,4)
        self._addNracesToIthPlayer(players,6,7)
        self._addNracesToIthPlayer(players,7,7)
        self._addNracesToIthPlayer(players,8,4)
        self._addNracesToIthPlayer(players,9,8)

        playersLeastRaces = playersWithLeastRaces(players)
        self.assertEqual(len(playersLeastRaces),2)
        self.assertEqual(playersLeastRaces[0].getRaces(),2)
        self.assertEqual(playersLeastRaces[1].getRaces(),2)
    
    def test_playersWithLeastRaces3(self):
        players = self._return10players()
        # 4,4,4,6,7,7,7,8,8,9
        self._addNracesToIthPlayer(players,0,9)
        self._addNracesToIthPlayer(players,1,6)
        self._addNracesToIthPlayer(players,2,7)
        self._addNracesToIthPlayer(players,3,4)
        self._addNracesToIthPlayer(players,4,8)
        self._addNracesToIthPlayer(players,5,4)
        self._addNracesToIthPlayer(players,6,7)
        self._addNracesToIthPlayer(players,7,7)
        self._addNracesToIthPlayer(players,8,4)
        self._addNracesToIthPlayer(players,9,8)

        playersLeastRaces = playersWithLeastRaces(players)
        self.assertEqual(len(playersLeastRaces),3)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
    
    def test_nPlayersWithLeastRaces(self):
        players = self._return10players()
        # 4,4,4,6,7,7,7,8,8,9
        self._addNracesToIthPlayer(players,0,9)
        self._addNracesToIthPlayer(players,1,6)
        self._addNracesToIthPlayer(players,2,7)
        self._addNracesToIthPlayer(players,3,4)
        self._addNracesToIthPlayer(players,4,8)
        self._addNracesToIthPlayer(players,5,4)
        self._addNracesToIthPlayer(players,6,7)
        self._addNracesToIthPlayer(players,7,7)
        self._addNracesToIthPlayer(players,8,4)
        self._addNracesToIthPlayer(players,9,8)

        playersLeastRaces = nPlayersWithLeastRaces(1,players)
        self.assertEqual(len(playersLeastRaces),1)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        
        playersLeastRaces = nPlayersWithLeastRaces(3,players)
        self.assertEqual(len(playersLeastRaces),3)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        
        playersLeastRaces = nPlayersWithLeastRaces(5,players)
        self.assertEqual(len(playersLeastRaces),5)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        self.assertEqual(playersLeastRaces[3].getRaces(),6)
        self.assertEqual(playersLeastRaces[4].getRaces(),7)

    def test_atLeastNplayersWithLeastRaces(self):
        players = self._return10players()
        # 4,4,4,6,7,7,7,8,8,9
        self._addNracesToIthPlayer(players,0,9)
        self._addNracesToIthPlayer(players,1,6)
        self._addNracesToIthPlayer(players,2,7)
        self._addNracesToIthPlayer(players,3,4)
        self._addNracesToIthPlayer(players,4,8)
        self._addNracesToIthPlayer(players,5,4)
        self._addNracesToIthPlayer(players,6,7)
        self._addNracesToIthPlayer(players,7,7)
        self._addNracesToIthPlayer(players,8,4)
        self._addNracesToIthPlayer(players,9,8)

        playersLeastRaces = atLeastNplayersWithLeastRaces(1,players)
        self.assertEqual(len(playersLeastRaces),3)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        
        playersLeastRaces = atLeastNplayersWithLeastRaces(2,players)
        self.assertEqual(len(playersLeastRaces),3)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        
        playersLeastRaces = atLeastNplayersWithLeastRaces(3,players)
        self.assertEqual(len(playersLeastRaces),3)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        
        playersLeastRaces = atLeastNplayersWithLeastRaces(4,players)
        self.assertEqual(len(playersLeastRaces),4)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        self.assertEqual(playersLeastRaces[3].getRaces(),6)

        playersLeastRaces = atLeastNplayersWithLeastRaces(5,players)
        self.assertEqual(len(playersLeastRaces),7)
        self.assertEqual(playersLeastRaces[0].getRaces(),4)
        self.assertEqual(playersLeastRaces[1].getRaces(),4)
        self.assertEqual(playersLeastRaces[2].getRaces(),4)
        self.assertEqual(playersLeastRaces[3].getRaces(),6)
        self.assertEqual(playersLeastRaces[4].getRaces(),7)
        self.assertEqual(playersLeastRaces[5].getRaces(),7)
        self.assertEqual(playersLeastRaces[6].getRaces(),7)
