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

#-Function to calculate the potential evapotranspiration
def ETpot(etr, kc):
    etpot = etr * kc
    return etpot

#-Function to calculate the actual evapotranspiration
def ETact(pcr, etpot, rootwater, rootsat, etreddry, rainfrac):
    etredwet = pcr.ifthenelse(rootwater >= rootsat, pcr.scalar(0), 1)
    etact = pcr.ifthenelse(rainfrac > 0, pcr.min(etpot * etreddry * etredwet, rootwater), 0)
    return etact
    
    
    
    
    
