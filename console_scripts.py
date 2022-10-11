#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:40:37 2022

@author: yalinli_cabbi
"""

from biorefineries.wwt import (
    AnMBR as AnMBRclass,
    BiogasUpgrading,
    compute_stream_COD,
    InternalCirculationRx,
    PolishingFilter,
    )
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

modules_1g = ['cn', 'sc1g', 'oc1g']
modules_2g = ['sc2g', 'oc2g', 'la']
modules_all = modules_1g + modules_2g

def load(module):
    f = f_dct[module]
    global exist_model, new_model, exist_sys, new_sys, exist_f, new_f, \
            exist_u, new_u, exist_s, new_s, exist_tea, new_tea
    exist_model, new_model = f()
    exist_sys, new_sys = exist_model.system, new_model.system
    exist_f, new_f = exist_sys.flowsheet, new_sys.flowsheet
    exist_u, new_u = exist_f.unit, new_f.unit
    exist_s, new_s = exist_f.stream, new_f.stream
    exist_tea, new_tea = exist_sys.TEA, new_sys.TEA

if __name__ == '__main__':
    module = 'cn'
    # module = 'sc1g'
    # module = 'oc1g'
    # module = 'cs'
    # module = 'sc2g'
    # module = 'oc2g'
    # module = 'la'
    load(module)
    for m in (exist_model, new_model): m.metrics_at_baseline()
    
    WWTC = AD = AeD = IC = AnMBR = AeF = Upgrading = None
    for u in exist_sys.units:
        name = u.__class__.__name__.lower()
        if name == 'wastewatersystemcost': WWTC = u
        elif name == 'anaerobicdigestion': AD = u
        elif name == 'aerobicdigestion': AeD = u
    for u in new_sys.units:
        if isinstance(u, InternalCirculationRx): IC = u
        elif isinstance(u, AnMBRclass): AnMBR = u
        elif isinstance(u, PolishingFilter): AeF = u
        elif isinstance(u, BiogasUpgrading): Upgrading = u
    
    if AD:
        CODinf_exist = compute_stream_COD(AD.ins[0])
        CODaer_inf_exist = compute_stream_COD(AeD.ins[0])
    if AeF:
        AeF.power_utility.rate/new_f.system.new_sys_wwt.power_utility.rate

    CODinf_new = compute_stream_COD(IC.ins[0])
    CODaer_inf_new = compute_stream_COD(AnMBR.outs[1])
    