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
import sys

def upperfirst(x):
    return x[:1].upper() + x[1:]

if len(sys.argv) == 2:
    classname = sys.argv[1]
    tmp = __import__("tests."+classname+"Test",fromlist=[upperfirst(classname)+"Test"])
    classnameTest = getattr(tmp,upperfirst(classname)+"Test")

    suite = unittest.TestLoader().loadTestsFromTestCase(classnameTest)
else:
    suite = unittest.TestLoader().discover("./tests/", pattern='*Test.py')

unittest.TextTestRunner(verbosity=2).run(suite)
