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

from itertools import combinations
from random import randint

def costOfRace(race,averageNumberOfRaces):
    '''
        cost increased by:
            for each player:
                differential between future number of races and current average number of race
            by 2*i, where i is the number of times somebody has already faced somebodyelse 
                NOTE: if not faced, cost is 0
                (maybe 3^i)?
    '''
    cost = 0
    # costs for differentials
    for player in race:
        cost += (player.getRaces() + 1) - averageNumberOfRaces # +1 because future races including this one
    # costs for refacing
        # for each couple of players facing each other (use combinations)
            # example: ABC -> AB,AC,BC
            # example: ABCD -> AB,AC,AD,BC,BD,CD
    for comb in combinations(race,2):
        # add cost only if already faced
        if (comb[0].hasFaced(comb[1])):
            # 3^numberTimesFaced
            cost += pow(3,comb[0].numberOfTimesAlreadyFaced(comb[1]))
            #cost += 3*comb[0].numberOfTimesAlreadyFaced(comb[1])
    return cost

def leastExpensiveRaces(players,playersPerRace,averageNumberOfRaces,fixedPlayers=None):
    '''
        returns least expensive races between "players" (if more races with same cost, returns the whole list)
        if player == None, race between players 
        if players specified in a list(= P), then players in P are fixed so they must be in the race
            for example: race can be [P[0],P[1],players[3],players[7]] 
    '''
    cost = None
    races = []
    if fixedPlayers != None:
        # test all races which contain fixedPlayers and random players in order to have playersPerRace
            # so the combinations must have (playersPerRace - len(fixedPlayers)) number of players
        for race in combinations(players,playersPerRace-len(fixedPlayers)):
            tempRace = list(race) # temporary in order to add fixedPlayer
            tempRace.extend(fixedPlayers)
            raceCost = costOfRace(tempRace,averageNumberOfRaces)
            if cost == None: # first combination, so save cost
                cost = raceCost
                races.append(tempRace)
            else:
                if round(raceCost,5) == round(cost,5):
                    races.append(tempRace)
                elif raceCost < cost:
                    races = []
                    cost = raceCost
                    races.append(tempRace)
    else:
        for race in combinations(players,playersPerRace):
            raceCost = costOfRace(race,averageNumberOfRaces)
            if cost == None: # first combination, so save cost
                cost = raceCost
                races.append(race)
            else:
                if round(raceCost,5) == round(cost,5):
                    races.append(race)
                elif raceCost < cost:
                    races = []
                    cost = raceCost
                    races.append(race)
    return races

def leastExpensiveRace(players,playersPerRace,averageNumberOfRaces,fixedPlayers=None):
    '''
        find least expensive race between "players" (if multiple races with same least cost, return random race)
        if player == None, race between players 
        if player specified (= P), then P is fixed so it must be in the race
            for example: race can be [P,players[3],players[7]] 
    '''
    races = leastExpensiveRaces(players,playersPerRace,averageNumberOfRaces,fixedPlayers)
    i = randint(0,len(races)-1) 
    return races[i]
