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

from itertools import product
from string import ascii_uppercase
from math import ceil,log

from .player import Player

class RandomPlayerGenerator():
    '''
        Random player generator class. 
        Should be created and then passed to tournament.
        Tournament will call 'generate' method and assign the created players to the tournament
    '''
    def __init__(self, numberOfPlayers):
        self._numberOfPlayers = numberOfPlayers

    def generate(self):
        players = []
        letters = list(ascii_uppercase)
        # how many letters needed for the number of players
            # 1 letter, 26 players, 2 letters 26*26 players
            # take the logarithm base 26, and then get the nearest higher integer
        numberOfLetters = int(ceil(log(self._numberOfPlayers,26)))
        i = 0
        # end when added numberOfPlayers
        for nameTuple in product(letters,repeat=numberOfLetters):
            # the name is ('A','A','A'), so I need to convert to string
            name = ""
            for j in range(0,numberOfLetters):
                name = name + nameTuple[j]
            if i < self._numberOfPlayers:
                players.append(Player(name))
                i += 1
            else:
                break
        return players
