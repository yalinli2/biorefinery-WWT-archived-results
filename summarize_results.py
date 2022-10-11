# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 12:48:54 2022

@author: Yalin Li
"""

import os, numpy as np, pandas as pd
from copy import deepcopy

folder = os.path.dirname(__file__)
modules_all = ['cn', 'sc1g', 'oc1g', 'cs', 'sc2g', 'oc2g', 'la']
modules_2G = ['cs', 'sc2g', 'oc2g', 'la']


# %%

def summarize_baselines():
    COD_in_new = []
    MPSP_exist, MPSP_new, MPSP_RIN, MPSP_no_WWT = [], [], [], []
    GWP_exist, GWP_new, GWP_RIN, GWP_no_WWT = [], [], [], []
    CAPEX_WWT_exist, CAPEX_WWT_new = [], []
    CAPEX_WWT_frac_exist, CAPEX_WWT_frac_new = [], []
    electricity_WWT_exist, electricity_WWT_new = [], []
    electricity_WWT_frac_exist, electricity_WWT_frac_new = [], []
    ECR_exist, ECR_new = [], []
    get_val = lambda key1, key2: df[(df.type==key1) & (df.metric==key2)].value.item()

    dir_path = os.path.join(folder, 'baselines')
    for module in modules_all:
        df_path = os.path.join(dir_path, f'{module}.csv')
        df = pd.read_csv(df_path, names=('type', 'metric', 'value'), skiprows=(0,))
        
        COD_in_new.append(get_val('new', 'COD in [mg/L]'))
        
        per = 'gal'
        try:
            MPSP_exist.append(get_val('exist', f'MPSP [$/{per}]'))
        except:
            per = 'kg'
            MPSP_exist.append(get_val('exist', f'MPSP [$/{per}]'))
        MPSP_new.append(get_val('new', f'MPSP [$/{per}]'))
        MPSP_RIN.append(get_val('new', f'MPSP_RIN [$/{per}]'))
        MPSP_no_WWT.append(get_val('new', f'MPSP_no WWT [$/{per}]'))

        # Use the displacement or allocation approach for LCA
        GWP_exist.append(get_val('exist', f'Product GWP disp [kg CO2/{per}]'))
        GWP_new.append(get_val('new', f'Product GWP disp [kg CO2/{per}]'))
        GWP_RIN.append(get_val('new', f'Product GWP disp_RIN [kg CO2/{per}]'))
        GWP_no_WWT.append(get_val('new', f'Product GWP disp_no WWT [kg CO2/{per}]'))

        CAPEX_WWT_exist.append(get_val('exist', 'WWT CAPEX [MM$]'))
        CAPEX_WWT_new.append(get_val('new', 'WWT CAPEX [MM$]'))
        CAPEX_WWT_frac_exist.append(get_val('exist', 'WWT CAPEX frac'))
        CAPEX_WWT_frac_new.append(get_val('new', 'WWT CAPEX frac'))

        electricity_WWT_exist.append(get_val('exist', 'WWT annual electricity consumption [MWh/yr]'))
        electricity_WWT_new.append(get_val('new', 'WWT annual electricity consumption [MWh/yr]'))
        electricity_WWT_frac_exist.append(get_val('exist', 'WWT annual electricity consumption frac'))
        electricity_WWT_frac_new.append(get_val('new', 'WWT annual electricity consumption frac'))

        ECR_exist.append(get_val('exist', 'WWT ECR'))
        ECR_new.append(get_val('new', 'WWT ECR'))

    df_all = pd.DataFrame({
        'COD_in': COD_in_new,
        'MPSP_exist': MPSP_exist,
        'MPSP_new': MPSP_new,
        'MPSP_RIN': MPSP_RIN,
        'MPSP_no_WWT': MPSP_no_WWT,
        })
    df_all['MPSP_new_frac_reduction'] = (df_all.MPSP_exist-df_all.MPSP_new)/df_all.MPSP_exist
    df_all['MPSP_RIN_frac_reduction'] = (df_all.MPSP_exist-df_all.MPSP_RIN)/df_all.MPSP_exist

    df_all['GWP_exist'] = GWP_exist
    df_all['GWP_new'] = GWP_new
    df_all['GWP_RIN'] = GWP_RIN
    df_all['GWP_no_WWT'] = GWP_no_WWT
    df_all['GWP_new_frac_reduction'] = (df_all.GWP_exist-df_all.GWP_new)/df_all.GWP_exist
    df_all['GWP_RIN_frac_reduction'] = (df_all.GWP_exist-df_all.GWP_RIN)/df_all.GWP_exist

    df_all['CAPEX_WWT_exist'] = CAPEX_WWT_exist
    df_all['CAPEX_WWT_new'] = CAPEX_WWT_new
    df_all['CAPEX_reduction'] = (df_all.CAPEX_WWT_exist-df_all.CAPEX_WWT_new)/df_all.CAPEX_WWT_exist
    df_all['CAPEX_WWT_frac_exist'] = CAPEX_WWT_frac_exist
    df_all['CAPEX_WWT_frac_new'] = CAPEX_WWT_frac_new

    df_all['electricity_WWT_exist'] = electricity_WWT_exist
    df_all['electricity_WWT_new'] = electricity_WWT_new
    df_all['electricity_WWT_reduction'] = \
        (df_all.electricity_WWT_exist-df_all.electricity_WWT_new)/df_all.electricity_WWT_exist
    df_all['electricity_WWT_frac_exist'] = electricity_WWT_frac_exist
    df_all['electricity_WWT_frac_new'] = electricity_WWT_frac_new

    df_all['ECR_exist'] = ECR_exist
    df_all['ECR_new'] = ECR_new

    df_all['biorefinery'] = modules_all
    df_all.set_index('biorefinery', inplace=True)
    summary_path = os.path.join(folder, 'summary_baseline.xlsx')
    df_all.to_excel(summary_path)


# %%

ufolder = os.path.join(folder, 'uncertainties')
def summarize_uncertainties(N=1000):
    get_df_dct = lambda kind: {
        m: pd.read_excel(
            os.path.join(ufolder, f'{m}_{kind}_{N}.xlsx'),
            sheet_name='Uncertainty results',
            header=[0,1],
            index_col=[0])
        for m in modules_all}
    exist_df_dct = get_df_dct('exist')
    new_df_dct = get_df_dct('new')
    
    empty_df = exist_df_dct['cn'].iloc[:,0].copy()
    empty_df[:] = np.nan
    empty_df.name = ('Biorefinery', 'foo')
    
    def get_col_names(module):
        per = 'gal' if module != 'la' else 'kg'
        return [
            ('Biorefinery', f'MPSP [$/{per}]'),
            ('Biorefinery', f'MPSP_RIN [$/{per}]'),
            ('Biorefinery', f'MPSP_no WWT [$/{per}]'),
            ('Biorefinery', f'Product GWP disp [kg CO2/{per}]'),
            ('Biorefinery', f'Product GWP disp_RIN [kg CO2/{per}]'),
            ('Biorefinery', f'Product GWP disp_no WWT [kg CO2/{per}]'),
            ('Biorefinery', 'WWT CAPEX frac'),
            ('Biorefinery', 'WWT annual electricity consumption frac'),
            ('Biorefinery', 'WWT ECR'),
            ('Biorefinery', 'CO2 cost total [$/tonne CO2]'),
            ('Biorefinery', 'CO2 cost net [$/tonne CO2]'),            ]
    
    get_data = lambda df, cols: [df.get(col, empty_df) for col in cols]
    get_module_results = lambda df_dct: {m: get_data(df, get_col_names(m)) for m, df in df_dct.items()}
    
    exist_results_dct = get_module_results(exist_df_dct)
    new_results_dct = get_module_results(new_df_dct)
    
    dct_lst = [{}, {}, {}, {}, {}, {}, {}]
    mpsp_dct, gwp_dct, capex_dct, electricity_dct, ecr_dct, co2_tot_dct, co2_net_dct = dct_lst
    for m in modules_all:
        exist_results = exist_results_dct[m]       
        new_results = new_results_dct[m]
        mpsp_dct[m] = [exist_results[0]] + new_results[:3]
        gwp_dct[m] = [exist_results[3]] + new_results[3:6]
        capex_dct[m] = [exist_results[6], new_results[6]]
        electricity_dct[m] = [exist_results[7], new_results[7]]
        ecr_dct[m] = [exist_results[8], new_results[8]]
        co2_tot_dct[m] = [exist_results[9], new_results[9]]
        co2_net_dct[m] = [exist_results[10], new_results[10]]
        
    def compile_exist_and_new(df_lst):
        df = pd.concat(df_lst, axis=1)
        df = df.droplevel(0, axis=1)
        old_col_names = df.columns.to_list()
        old_col_names = [i.split('[')[0][:-1] for i in old_col_names]
        col_names = ['Exist '+old_col_names[0], 'New '+old_col_names[1]]
        if len(old_col_names) > 2: col_names.extend(old_col_names[2:])
        df.columns = col_names
        return df
        
    compiled = [pd.concat([compile_exist_and_new(df_lst)
                           for df_lst in dct.values()])
                for dct in dct_lst]
    sheet_names = ['MPSP', 'GWP', 'CAPEX', 'Electricity', 'ECR', 'CO2tot', 'CO2net']
    writer = pd.ExcelWriter(os.path.join(folder, f'summary_uncertainty_{N}.xlsx'))
    for df, name in zip(compiled, sheet_names): df.to_excel(writer, sheet_name=name)
    writer.close()


# %%

def summarize_spearman(
        N=1000,
        p_sig=0.05,
        cutoff_val=0.2, # absolute value > this cutoff
        cutoff_rank=None, # select the top X
        ):
    get_path = lambda module, kind, N: os.path.join(ufolder, f'{module}_{kind}_{N}.xlsx')
    def read_df(path, stat):
        df = pd.read_excel(pd.ExcelFile(path), f'Spearman {stat}', header=[0], index_col=[0,1])
        df = df.iloc[:, :2].copy()
        df.columns = ('MPSP', 'GWP')
        return df
    kinds = ('exist', 'new')
    with pd.ExcelWriter(os.path.join(folder, f'summary_spearman_{N}.xlsx')) as writer:
        for module in modules_all:
            rhos = [read_df(get_path(module, kind, N), 'rho') for kind in kinds]
            ps = [read_df(get_path(module, kind, N), 'p') for kind in kinds]            
            
            tops = []
            for rho, p in zip(rhos, ps):
                df = rho[p<=p_sig].dropna(how='all')
                df['abs_MPSP'] = df['MPSP'].abs()
                df['abs_GWP'] = df['GWP'].abs()
                if cutoff_rank:
                    select = [df.sort_values(by=[key], ascending=False)[:cutoff_rank]
                            for key in ('abs_MPSP', 'abs_GWP')]
                else:
                    select = [df.sort_values(by=[key], ascending=False)
                            for key in ('abs_MPSP', 'abs_GWP')]
                top = pd.concat(select).drop_duplicates()
                top = top.iloc[:, :2]
                tops.append(top)
            
            module_dfs = [df[
                (df['MPSP']<=-cutoff_val)|
                (df['MPSP']>=cutoff_val)|
                (df['GWP']<=-cutoff_val)|
                (df['GWP']>=cutoff_val)
                ] for df in tops]
            compiled = pd.concat(module_dfs, axis=1, keys=kinds)
            compiled = compiled.where(compiled.abs()>=cutoff_val, other=np.nan).dropna(how='all')
            compiled.to_excel(writer, sheet_name=module)


# %%

def summarize_BMPs(
        lower=0.05, mid=0.5, upper=0.95,
        dir_path=os.path.join(folder, 'BMPs'),
        modules=modules_2G,
        ):
    BMPs = [int(i) for i in os.listdir(dir_path) if i.isnumeric()]
    BMPs.sort()
    MPSPs = {}
    for module in modules: MPSPs[module] = []
    GWPs = deepcopy(MPSPs)
    COD_prices = deepcopy(MPSPs)
    COD_GWPs = deepcopy(MPSPs)

    def get_vals(df, key, indices):
        vals = df[key].to_list()
        vals = [vals[i] for i in indices]
        return vals

    for BMP in BMPs:
        BMP_path = os.path.join(dir_path, str(BMP))
        files = list(os.walk(BMP_path))[0][-1]
        for i in files:
            abbr = i.split('_')[0]
            MPSP, GWP, COD_price, COD_GWP = MPSPs[abbr], GWPs[abbr], COD_prices[abbr], COD_GWPs[abbr]
            df = pd.read_excel(os.path.join(BMP_path, i), sheet_name='Percentiles',
                               index_col=(0), header=(0, 1))
            df = df.droplevel(level=0, axis=1)
            percentiles = df.index.to_list()
            indices = [percentiles.index(i) for i in (lower, mid, upper)]
            per = 'gal'
            try:
                MPSP.extend(get_vals(df, f'MPSP [$/{per}]', indices))
            except:
                per = 'kg'
                MPSP.extend(get_vals(df, f'MPSP [$/{per}]', indices))
            GWP.extend(get_vals(df, f'Product GWP disp [kg CO2/{per}]', indices))
            COD_price.extend(get_vals(df, 'COD price [$/tonne]', indices))
            COD_GWP.extend(get_vals(df, 'COD GWP disp [kg CO2/tonne]', indices))

    MPSP_df = pd.DataFrame.from_dict(MPSPs)
    MPSP_df.index = pd.MultiIndex.from_product(
        (BMPs, (lower, mid, upper)), names=('BMP', 'Percentile'))
    GWP_df = pd.DataFrame.from_dict(GWPs)
    COD_price_df = pd.DataFrame.from_dict(COD_prices)
    COD_GWP_df = pd.DataFrame.from_dict(COD_GWPs)
    new_index = pd.MultiIndex.from_product(
        ((lower, mid, upper), BMPs), names=('Percentile', 'BMP'))
    for df in (GWP_df, COD_price_df, COD_GWP_df, MPSP_df): # MPSP_df last for index
        if df is not MPSP_df: df.index = MPSP_df.index
        df.sort_index(level=1, inplace=True)
        df.index = new_index

    path = os.path.join(folder, 'summary_BMP.xlsx')
    with pd.ExcelWriter(path) as writer:
        MPSP_df.to_excel(writer, sheet_name='MPSP')
        GWP_df.to_excel(writer, sheet_name='GWP')
        COD_price_df.to_excel(writer, sheet_name='COD Price')
        COD_GWP_df.to_excel(writer, sheet_name='COD GWP')

    
# %%

if __name__ == '__main__':
    N = 1000
    summarize_baselines()
    summarize_uncertainties(N=N)
    summarize_spearman(N=N)
    summarize_BMPs()