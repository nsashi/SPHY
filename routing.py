# -*- coding: utf-8 -*-
#
# The Spatial Processes in HYdrology (SPHY) model:
# A spatially distributed hydrological model that calculates soil-water and
# cryosphere processes on a cell-by-cell basis.
#
# Copyright (C) 2013  Wilco Terink
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email: terinkw@gmail.com

#-Authorship information-###################################################################
__author__ = "Wilco Terink"
__copyright__ = "Wilco Terink"
__license__ = "GPL"
__version__ = "2.2"
__email__ = "terinkw@gmail.com"
__date__ ='16 October 2018'
############################################################################################

print 'routing module imported'

def ROUT(pcr, q, oldq, flowdir, kx):
    rr = (q * 0.001 * pcr.cellarea()) / (24*3600)
    ra = pcr.accuflux(flowdir, rr)
    ra = (1 - kx) * ra + kx * oldq
    return ra
