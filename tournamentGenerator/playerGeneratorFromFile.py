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

from .player import Player

class PlayerGeneratorFromFile():
    '''
        Player generator class that reads players names from file. 
        Should be created and then passed to tournament.
        Tournament will call 'generate' method and assign the created players to the tournament
    '''
    def __init__(self, filename):
        self._filename = filename

    def generate(self):
        players = []
        fp = open(self._filename)
        for line in fp:
            players.append(Player(line[:-1]))
        return players
