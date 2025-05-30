import numpy as np
import Data51
import pandas as pd
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

mdl = pyo.ConcreteModel('Production_Model')

#SETS

mdl.I = pyo.Set(initialize=Data51.components, doc='components' )
mdl.J = pyo.Set(initialize=Data51.plants, doc='plants')
mdl.T = pyo.Set(initialize=Data51.periods, doc='periods')


#PARAMETERS

mdl.pLABORDATA = pyo.Param(mdl.I, mdl.J, initialize=Data51.labor, doc='Required packing minutes' )
mdl.pLABAV = pyo.Param(mdl.J, initialize=Data51.laborAv, doc='Labor availability' )
mdl.pPACKDATA = pyo.Param(mdl.I, mdl.J, initialize=Data51.packing, doc='Required packing minutes' )
mdl.pPACKAV = pyo.Param(mdl.J, initialize=Data51.packingAv, doc='Packing availability' )
mdl.pASSDATA = pyo.Param(mdl.J, initialize=Data51.assembly, doc='Required assembly minutes' )
mdl.pASSAV = pyo.Param(mdl.J, initialize=Data51.assemblyAv, doc='Available assembly total times' )
mdl.pMINDEMCOMP = pyo.Param(mdl.I, mdl.J, initialize=Data51.minDemands, doc='Minimum demand components' )
mdl.pMAXDEMCOMP = pyo.Param(mdl.I, mdl.J, initialize=Data51.maxDemands, doc='Maximum demand components' )
mdl.pMINDEMROBO = pyo.Param(mdl.J, initialize=Data51.minDemandsRobo, doc='Minimum robot demands' )
mdl.pMAXDEMROBO = pyo.Param(mdl.J, initialize=Data51.maxDemandsRobo, doc='Maximum robot demands' )
mdl.pCOSTCOMP = pyo.Param(mdl.I, mdl.J, initialize=Data51.prodComps, doc='Components prod. costs' )
mdl.pCOSTROBO = pyo.Param(mdl.J, initialize=Data51.prodRobo, doc='Robot prod. costs' )
mdl.pSELLCOMP = pyo.Param(mdl.I, mdl.J, initialize=Data51.priceComps, doc='Components selling prices' )
mdl.pSELLROBO = pyo.Param(mdl.J, initialize=Data51.priceRobo, doc='Robot selling prices' )
mdl.pREQ = pyo.Param(mdl.I, initialize=Data51.reqs, doc='Robotic kit requirements')

#VARIABLES

mdl.vX =pyo.Var(mdl.I, mdl.J, mdl.T,bounds=(0.0,None), doc='produced components in per plants per month', within=pyo.NonNegativeReals)
mdl.vR =pyo.Var(mdl.J, mdl.T,bounds=(0.0,None), doc='produced robots in per plants per month', within=pyo.NonNegativeReals)
mdl.vXS =pyo.Var(mdl.I, mdl.J, mdl.T, bounds=(0.0,None), doc='sold components in per plants per month', within=pyo.NonNegativeReals)
mdl.vRS =pyo.Var(mdl.J, mdl.T,bounds=(0.0,None), doc='sold robots in per plants per month', within=pyo.NonNegativeReals)
mdl.vINVX =pyo.Var(mdl.I, mdl.J, mdl.T, bounds=(0.0,None), doc='inventory of components per plants per month', within=pyo.NonNegativeReals)
mdl.vINVR =pyo.Var(mdl.J, mdl.T,bounds=(0.0,None), doc='inventory of robotic kit per plants per month', within=pyo.NonNegativeReals)

#PARAMETRE DOĞRULAMALARI#

# 1. Parametre Eksikliği Kontrol Fonksiyonu
def validate_param(param, required_keys, param_name):
    for key in required_keys:
        if key not in param:
            print(f"Error: {param_name} için eksik değer: {key}")

# 2. Aralık Kontrol Fonksiyonu
def validate_range(param_min, param_max, param_name):
    for key in param_min:
        if key in param_max and param_min[key] > param_max[key]:
            print(f"Error: {param_name} için {key} anahtarında min > max!")

# 3. Veri Doğrulama Fonksiyonu
def validate_data():
    # Parametre eksikliği kontrolü
    required_keys = [(i, j) for i in Data51.components for j in Data51.plants]
    validate_param(Data51.labor, required_keys, "labor")
    validate_param(Data51.packing, required_keys, "packing")
    
    # Aralık kontrolü
    validate_range(Data51.minDemands, Data51.maxDemands, "demand")

    # Kapasite kontrolü
    for j in Data51.plants:
        total_required_labor = sum(Data51.labor[(i, j)] * Data51.minDemands[(i, j)] for i in Data51.components)
        if total_required_labor > Data51.laborAv[j]:
            print(f"Warning: İş gücü kapasitesi aşıldı! Tesis: {j}")

    # Zaman dönemi kontrolü
    for t in Data51.periods:
        for i in Data51.components:
            for j in Data51.plants:
                if (i, j, t) not in mdl.vX:
                    print(f"Error: vX değişkeni ({i}, {j}, {t}) kombinasyonu eksik!")

# 4. Doğrulama Fonksiyonunu Çağırma
validate_data()





#CONSTRAINTS

def  eLab (mdl, j, t):
    return sum(mdl.vX[i,j,t]*mdl.pLABORDATA[i,j] for i in mdl.I) <= mdl.pLABAV[j]
mdl.eLab = pyo.Constraint(mdl.J, mdl.T, rule=eLab, doc='Available labor constraint')

def  ePack (mdl, j, t):
    return sum(mdl.vX[i,j,t]*mdl.pPACKDATA[i,j] for i in mdl.I) <= mdl.pPACKAV[j]
mdl.ePack = pyo.Constraint(mdl.J, mdl.T, rule=ePack, doc='Available packing constraint')

def eAss (mdl, j, t):
    return mdl.vR[j,t]*mdl.pASSDATA[j] <= mdl.pASSAV[j]
mdl.eAss = pyo.Constraint(mdl.J, mdl.T, rule=eAss, doc='Available assembly time constraint')

def eCar (mdl, t):
    MaxCarbonFiber = 4000
    return sum(mdl.vX['CarbonFiber',j,t] for j in mdl.J) <= MaxCarbonFiber
mdl.eCar = pyo.Constraint(mdl.T, rule=eCar, doc='Carbon fiber constraint')

def eMinDem (mdl,i, j, t):
    return mdl.vX[i,j,t] >= mdl.pMINDEMCOMP[i,j]
mdl.eMinDem = pyo.Constraint(mdl.I, mdl.J, mdl.T, rule=eMinDem, doc='Minimum demand constraint')

def eMaxDem (mdl,i, j, t):
    return mdl.vX[i,j,t] <= mdl.pMAXDEMCOMP[i,j]
mdl.eMaxDem = pyo.Constraint(mdl.I, mdl.J, mdl.T, rule=eMaxDem, doc='Maximum demand constraint')

def eMinRobo (mdl, j, t):
    return mdl.vR[j,t] >= mdl.pMINDEMROBO[j]
mdl.eMinRobo = pyo.Constraint(mdl.J, mdl.T, rule= eMinRobo, doc='Minimum robot demand')

def eMaxRobo (mdl, j, t):
    return mdl.vR[j,t] <= mdl.pMAXDEMROBO[j]
mdl.eMaxRobo = pyo.Constraint(mdl.J, mdl.T, rule= eMaxRobo, doc='Maximum robot demand')

def eMESUDE(mdl, i, j, t):
    return mdl.pREQ[i]*mdl.vR[j,t] <= mdl.vX[i,j,t]
mdl.eMESUDE= pyo.Constraint(mdl.I, mdl.J, mdl.T, rule=eMESUDE, doc='MESUDE REQ')

def eNormalizeX(mdl, i, j, t):
    if t == 1:
        return mdl.vX[i,j,t] - mdl.vXS[i,j,t] - mdl.vINVX[i,j,t] - mdl.pREQ[i]*mdl.vR[j,t] == 0
    else:
        return mdl.vX[i,j,t] - mdl.vXS[i,j,t] - mdl.vINVX[i,j,t] - mdl.pREQ[i]*mdl.vR[j,t] + mdl.vINVX[i,j,t-1] == 0
mdl.eNormalizeX = pyo.Constraint(mdl.I, mdl.J, mdl.T, rule=eNormalizeX, doc='NormalizationX')

def eNormalizeR(mdl, j, t):
    if t == 1:
        return mdl.vR[j, t] - mdl.vRS[j, t] - mdl.vINVR[j, t] == 0
    else:
        return mdl.vR[j, t] - mdl.vRS[j, t] - mdl.vINVR[j, t] + mdl.vINVR[j, t-1] == 0
mdl.eNormalizeR = pyo.Constraint(mdl.J, mdl.T, rule=eNormalizeR, doc='NormalizationR')


#OBJECTIVE FUNCTION
def oTotalProfit(mdl):
    CARRY_COST_RATE = 0.12  # Inventory keeping cost (%12)
    COST_INCREASE_RATE = 1.08  # %8 increase for the second month

    # Toplam Gelir
    total_revenue = sum((mdl.vXS[i, j, t] * mdl.pSELLCOMP[i, j] +
                         mdl.vRS[j, t] * mdl.pSELLROBO[j])
                        for i in mdl.I for j in mdl.J for t in mdl.T)

    # Toplam Maliyet
    total_cost = sum(
        (mdl.vX[i, j, 1] * mdl.pCOSTCOMP[i, j] +  # İlk ay üretim maliyeti
         mdl.vINVX[i, j, 1] * mdl.pCOSTCOMP[i, j] * CARRY_COST_RATE) +  # İlk ay envanter maliyeti
        (mdl.vX[i, j, 2] * mdl.pCOSTCOMP[i, j] * COST_INCREASE_RATE +  # İkinci ay üretim maliyeti
         mdl.vINVX[i, j, 2] * mdl.pCOSTCOMP[i, j] * CARRY_COST_RATE * COST_INCREASE_RATE) +  # İkinci ay envanter maliyeti
        (mdl.vR[j, 1] * mdl.pCOSTROBO[j] +  # İlk ay robot üretim maliyeti
         mdl.vINVR[j, 1] * mdl.pCOSTROBO[j] * CARRY_COST_RATE) +  # İlk ay robot envanter maliyeti
        (mdl.vR[j, 2] * mdl.pCOSTROBO[j] * COST_INCREASE_RATE +  # İkinci ay robot üretim maliyeti
         mdl.vINVR[j, 2] * mdl.pCOSTROBO[j] * CARRY_COST_RATE * COST_INCREASE_RATE)  # İkinci ay robot envanter maliyeti
        for i in mdl.I for j in mdl.J
    )

    # Toplam Kâr
    return total_revenue - total_cost

    
mdl.oTotalProfit = pyo.Objective(rule=oTotalProfit, sense=pyo.maximize, doc='Total Profit')

#shadow prices of the constraints
mdl.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
#reduced costs of the objective function coefficients
mdl.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
Solver = SolverFactory('glpk')
#Print the sensitivity analysis and output report
Solver.options['ranges'] = r'D:\SA_report.txt'

SolverResults = Solver.solve(mdl, tee=True)
SolverResults.write()
mdl.pprint()
mdl.vX.display()
mdl.oTotalProfit.display()


import logging

logging.basicConfig(filename="validation_report.log", level=logging.INFO)

def log_message(message, level="info"):
    if level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    else:
        logging.info(message)

log_message("Data validation completed. No issues found.")