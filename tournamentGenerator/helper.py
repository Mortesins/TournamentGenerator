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

def removeList2fromList1(a,b):
    for item in b:
        try:
            a.remove(item)
        except ValueError:
            None
    return

def printRaces(races):
    i = 1
    for race in races:
        if (i < 10):
            print(" " + str(i) + ".", race)
        else:
            print(str(i) + ".", race)
        i+=1

def sameRace(race1,race2):
    # check for length
    if (len(race1) != len(race2)):
        return False
    # for each player race1, see if player is in race two
        # if player not in race2, then races are not equal
    for player in race1:
        if player not in race2:
            return False
    # if out of loop, then every player in race1 is in race2
    return True

def convertRaceResultToRace(raceResult):
    race = []
    for playerResult in raceResult:
        race.append(playerResult[0])
    return race

def convertRaceResultsToRaces(raceResults):
    races = []
    for raceResult in raceResults:
        races.append(convertRaceResultToRace(raceResult))
    return races

def lapTimeToStr(lapTime):
    return lapTime.strftime('%M:%S:%f')[1:-3]
