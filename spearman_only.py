# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 08:32:00 2022

@author: Yalin Li
"""

import os, pandas as pd
from biorefineries.wwt.corn import create_cn_comparison_models as f_cn
from biorefineries.wwt.sugarcane1g import create_sc1g_comparison_models as f_sc1g
from biorefineries.wwt.oilcane1g import create_oc1g_comparison_models as f_oc1g
from biorefineries.wwt.cornstover import create_cs_comparison_models as f_cs
from biorefineries.wwt.sugarcane2g import create_sc2g_comparison_models as f_sc2g
from biorefineries.wwt.oilcane2g import create_oc2g_comparison_models as f_oc2g
from biorefineries.wwt.lactic import create_la_comparison_models as f_la

f_dct = {
    'cn': f_cn,
    'sc1g': f_sc1g,
    'oc1g': f_oc1g,
    'cs': f_cs,
    'sc2g': f_sc2g,
    'oc2g': f_oc2g,
    'la': f_la,
    }

folder = os.path.dirname(__file__)
ufolder = os.path.join(folder, 'uncertainties')

modules_all = list(f_dct.keys())
N = 1000

get_raw = lambda kind: pd.read_excel(os.path.join(ufolder, f'{m}_{kind}_{N}.xlsx'),
                                     sheet_name='Raw data', header=[0,1], index_col=[0])

# %%

m = modules_all[6]
raw_exist = get_raw('exist')
raw_new = get_raw('new')
exist_model, new_model = f_dct[m]()
exist_model.table = raw_exist
new_model.table = raw_new

kind = 'new'
rho, p = exist_model.spearman_r(filter='omit nan') if kind == 'exist' else new_model.spearman_r(filter='omit nan')
rho = rho.droplevel(0, axis=1)
p = p.droplevel(0, axis=1)

with pd.ExcelWriter(os.path.join(folder, f'tmp_{m}_{kind}.xlsx')) as writer:
    rho.to_excel(writer, sheet_name='Spearman_rho')
    p.to_excel(writer, sheet_name='Spearman_p')
