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
# Email: w.terink@futurewater.nl OR terinkw@gmail.com

#-Authorship information-###################################################################
__author__ = "Wilco Terink"
__copyright__ = "Wilco Terink"
__license__ = "GPL"
__version__ = "erosion testing"
__email__ = "w.terink@futurewater.nl, terinkw@gmail.com"
__date__ ='1 January 2017'
############################################################################################

print 'Lake module imported'

#-Function that updates the lake storage and lake level given a measured lake level. If no lake
# level is measured, then the actual storage is not updated with a measured level. The function
# returns the updated storage and lake level
def UpdateLakeHStore(self, pcr, pcrm):
    #-buffer actual storage
    OldStorage = self.StorAct
    #-Check if measured lake levels area available
    try:
        LakeLevel = pcr.readmap(pcrm.generateNameT(self.LLevel, self.counter))
        Level = True
    except:
        Level = False
    if Level:
        #-update lake storage according to measured water level
        self.StorAct = pcr.ifthenelse(self.UpdateLakeLevel, pcr.ifthenelse(pcr.defined(LakeLevel), pcr.ifthenelse(self.LakeSH_Func==1,\
            self.LakeSH_exp_a * pcr.exp(self.LakeSH_exp_b * LakeLevel), pcr.ifthenelse(self.LakeSH_Func==2, self.LakeSH_pol_a1 \
            * LakeLevel + self.LakeSH_pol_b, pcr.ifthenelse(self.LakeSH_Func==3, (self.LakeSH_pol_a2 * LakeLevel**2) + \
            self.LakeSH_pol_a1 * LakeLevel + self.LakeSH_pol_b, (self.LakeSH_pol_a3 * LakeLevel**3) + (self.LakeSH_pol_a2 \
            * LakeLevel**2) + (self.LakeSH_pol_a1 * LakeLevel + self.LakeSH_pol_b)))), self.StorAct), self.StorAct)
        # prevent storage becoming negative for whatever reason
        self.StorAct = pcr.max(self.StorAct, 0)
        #-Update the lake level based on the storage for lakes where no levels are measured
        LakeLevel = pcr.ifthenelse(self.UpdateLakeLevel, pcr.ifthenelse(pcr.defined(LakeLevel), LakeLevel, \
            pcr.ifthenelse(self.LakeHS_Func==1, self.LakeHS_exp_a * pcr.exp(self.LakeHS_exp_b * self.StorAct), pcr.ifthenelse(self.LakeHS_Func==2, self.LakeHS_pol_a1 * \
            self.StorAct + self.LakeHS_pol_b, pcr.ifthenelse(self.LakeHS_Func==3, (self.LakeHS_pol_a2 * self.StorAct**2) + \
            self.LakeHS_pol_a1 * self.StorAct + self.LakeHS_pol_b, (self.LakeHS_pol_a3 * self.StorAct**3) + (self.LakeHS_pol_a2 *\
            self.StorAct**2) + self.LakeHS_pol_a1 * self.StorAct + self.LakeHS_pol_b)))), pcr.ifthenelse(self.LakeHS_Func==1, \
            self.LakeHS_exp_a * pcr.exp(self.LakeHS_exp_b * self.StorAct), pcr.ifthenelse(self.LakeHS_Func==2, self.LakeHS_pol_a1 * \
            self.StorAct + self.LakeHS_pol_b, pcr.ifthenelse(self.LakeHS_Func==3, (self.LakeHS_pol_a2 * self.StorAct**2) + \
            self.LakeHS_pol_a1 * self.StorAct + self.LakeHS_pol_b, (self.LakeHS_pol_a3 * self.StorAct**3) + (self.LakeHS_pol_a2 *\
            self.StorAct**2) + self.LakeHS_pol_a1 * self.StorAct + self.LakeHS_pol_b))))

    else:
        # if no lake level map is available, then calculate the h based on storages
        LakeLevel = pcr.ifthenelse(self.LakeHS_Func==1, self.LakeHS_exp_a * pcr.exp(self.LakeHS_exp_b * self.StorAct), \
            pcr.ifthenelse(self.LakeHS_Func==2, self.LakeHS_pol_a1 * self.StorAct + self.LakeHS_pol_b, pcr.ifthenelse(\
            self.LakeHS_Func==3, (self.LakeHS_pol_a2 * self.StorAct**2) + self.LakeHS_pol_a1 * self.StorAct + self.LakeHS_pol_b,\
            (self.LakeHS_pol_a3 * self.StorAct**3) + (self.LakeHS_pol_a2 * self.StorAct**2) + self.LakeHS_pol_a1 * self.StorAct +\
            self.LakeHS_pol_b)))
    self.StorAct = pcr.ifthenelse(self.LakeID != 0, self.StorAct, OldStorage)
    return LakeLevel, self.StorAct

#-function that calculates the fraction of lake storage that is available for routing
def QFrac(self, pcr, LakeLevel):
    Q = pcr.ifthenelse(self.LakeQH_Func==1, self.LakeQH_exp_a * pcr.exp(self.LakeQH_exp_b * LakeLevel), pcr.ifthenelse(\
        self.LakeQH_Func==2, self.LakeQH_pol_a1 * LakeLevel + self.LakeQH_pol_b, pcr.ifthenelse(self.LakeQH_Func==3, \
        (self.LakeQH_pol_a2 * LakeLevel**2) + self.LakeQH_pol_a1 * LakeLevel + self.LakeQH_pol_b, (self.LakeQH_pol_a3 * \
        LakeLevel**3) + (self.LakeQH_pol_a2 * LakeLevel**2) + self.LakeQH_pol_a1 * LakeLevel + self.LakeQH_pol_b)))
    Q = pcr.max(0, Q)
    #-convert to m3/d
    Q = Q * 3600 * 24
    Qfrac = pcr.min(pcr.max(Q / self.StorAct, 0), 1)
    Qfrac = pcr.ifthenelse(self.LakeID != 0, Qfrac, 1-self.kx) # for non-lakes, qfrac = 1-kx
    return Qfrac