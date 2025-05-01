import sys; sys.path.append("..")
from __init__ import *
# 
import altair as alt
import json
import numpy as np
import re
import os
import tidypolars4sci as tp
import tools4sci as t4
from tools4sci.report import models2tab
from tools4sci.io import save_table, save_figure
from scipy.stats import norm as dnorm
from statsmodels.formula.api import ols as lm
from statsmodels.formula.api import glm as glm
from statsmodels.api import families as family
from statsmodels.formula.api import mnlogit as mlogit
from pprint import pprint
from watermark import watermark as modules_used
# 
SAVE = False
SAVE = True
# 
FIGURES = {
        'main barplot' : {
            'fn': 'fig-1',
            'path': PATH_FIGURES, 
            'caption': ("Percentage of time (y-axis) voters who identify with the Democratic or Republican "+
                        "party (color code) chose candidates with conservative (top panels) or liberal  "+
                        "positions (bottom panels) in various policy areas (x-axis). The left panels show "+
                        "cases in which choices involved candidates from difference parties. "+
                        "Right panels show choices between two independent candiddates. "+
                        "Only status reassuring exposure included (see online supplement for other conditions). ")
        },
    'non-partisan marginal effects (prr)' :{
        'fn': 'fig-2',
        'path': PATH_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) on voters’ support for "+
                    "candidates due to their conservative policy position (y-axis). "+
                    "Estimates based on linear probability models "+
                    "using non-partisan candidate pairs only."+
                    "Panels show subsamples by voters' partisanship and "+
                    "using pooled data. SE clustered by subject."
                    )
    },
    'partisan marginal effects (prr)' :{
        'fn': 'fig-3',
        'path': PATH_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) on voters’ support for "+
                    "candidates due to their conservative policy position (y-axis). "+
                    "Estimates based on linear probability models "+
                    "using partisan candidate pairs (column panels)."+
                    "Row panels show subsamples by voters' partisanship. "+
                    "SE clustered by subject."
                    )
    },
    'number of conservative positions' : {
        'fn': 'fig-4',
        'path': PATH_FIGURES, 
        'caption': ("Predicted probability "+ 
                    "of voting for the candidate as a function "+
                    "of the number of conservative positions "+
                    "taken on different issues (x-axis) by status threat "+
                    "exposure (shapes), voters' partisanship (line types), "+
                    " and party profile of the candiates competing (panels)."
                    )
    },
    # online supplement 
    # -----------------
    'balance' : {
        'fn': 'fig-h1',
        'path': PATH_OS_FIGURES, 
        'caption' : ("Sample Balance. Estimates are "+
                     "coefficients  a regression of "+
                     "treatment condition on the pre-treatment covariates")
    },
    'barplot under racial threat' : {
        'fn': 'fig-l1',
        'path': PATH_OS_FIGURES, 
        'caption': ("Percentage of time (y-axis) voters who identify with the Democratic or Republican "+
                    "party (color code) chose candidates with conservative (top panels) or liberal  "+
                    "positions (bottom panels) in various policy areas (x-axis). The left panels show "+
                    "cases in which choices involved candidates from difference parties. "+
                    "Right panels show choices between two independent candiddates. "+
                    "Only racial threat exposure included. ")
    },
    'barplot under nationality threat' : {
        'fn': 'fig-l2',
        'path': PATH_OS_FIGURES, 
        'caption': ("Percentage of time (y-axis) voters who identify with the Democratic or Republican "+
                    "party (color code) chose candidates with conservative (top panels) or liberal  "+
                    "positions (bottom panels) in various policy areas (x-axis). The left panels show "+
                    "cases in which choices involved candidates from difference parties. "+
                    "Right panels show choices between two independent candiddates. "+
                    "Only nationality threat exposure included. ")
    },
    'barplot under racial and nationality threat' : {
        'fn': 'fig-l3',
        'path': PATH_OS_FIGURES, 
        'caption': ("Percentage of time (y-axis) voters who identify with the Democratic or Republican "+
                    "party (color code) chose candidates with conservative (top panels) or liberal  "+
                    "positions (bottom panels) in various policy areas (x-axis). The left panels show "+
                    "cases in which choices involved candidates from difference parties. "+
                    "Right panels show choices between two independent candiddates. "+
                    "Only joint racial and nationality threat exposure included. ")
    },
    'non-partisan marginal effects (all correct mc)' :{
        'fn': 'fig-k1',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) on voters’ support for "+
                    "candidates due to their conservative policy position (y-axis). "+
                    "Estimates based on linear probability models "+
                    "using non-partisan candidate pairs only."+
                    "Panels show subsamples by voters' partisanship and "+
                    "using pooled data. SE clustered by subject. Subsample: "+
                    "100\\perc correct answers in the manipulation check."
                    )
    },
    'partisan marginal effects (all correct mc)' :{
        'fn': 'fig-k2',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) on voters’ support for "+
                    "candidates due to their conservative policy position (y-axis). "+
                    "Estimates based on linear probability models "+
                    "using partisan candidate pairs (column panels):"+
                    "Democratic vs Democratic (DxD); Democratic vs Republican (DxR); "+
                    "Republican vs Republican (RxR). Subsample: "+
                    "100\\perc correct answers in the manipulation check."
                    )
    },
    'speeders' :{
        'fn': 'fig-k3',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) and conservative positions "+
                    " and their interaction with the conjoint task order. "+
                    "Estimates based on linear probability models. "+
                    "Each y-axis value (e.g., Rac. Threat) includes estimates "+
                    " from four models: Full sample and "+ 
                    "three subsamples with only participants who completed " +
                     "the survey 50\\%, 40\\%, and 30\\% faster than the median response time. "+
                    "SE clustered by subject."
                    )
    },
    'task order effect (non-partisan)' :{
        'fn': 'fig-m1',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) and conservative positions "+
                    " and their interaction with the conjoint task order. "+
                    "Estimates based on linear probability models "+
                    "using non-partisan candidate pairs."+
                    "Panels show subsamples by voters' partisanship. "+
                    "SE clustered by subject."
                    )
    },
    'task order effect (partisan)' :{
        'fn': 'fig-m2',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) and conservative positions "+
                    " and their interaction with the conjoint task order. "+
                    "Estimates based on linear probability models "+
                    "using partisan candidate pairs (column panels):"+
                    "Democratic vs Democratic (DxD); Democratic vs Republican (DxR); "+
                    "Republican vs Republican (RxR). "+
                    "Row panels show subsamples by voters' partisanship. "+
                    "SE clustered by subject."
                    )
    },
    'profile order effect (non-partisan)' :{
        'fn': 'fig-m3',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) and conservative positions "+
                    " and their interaction with the conjoint profile order. "+
                    "Estimates based on linear probability models "+
                    "using non-partisan candidate pairs."+
                    "Panels show subsamples by voters' partisanship. "+
                    "SE clustered by subject."
                    )
    },
    'profile order effect (partisan)' :{
        'fn': 'fig-m4',
        'path': PATH_OS_FIGURES, 
        'caption': ("Point estimates (shapes) and 95% confidence intervals "+
                    "(bars) capturing the causal effect (x-axis) of status "+
                    "threat (shapes and colors) and conservative positions "+
                    " and their interaction with the conjoint profile order. "+
                    "Estimates based on linear probability models "+
                    "using partisan candidate pairs (column panels):"+
                    "Democratic vs Democratic (DxD); Democratic vs Republican (DxR); "+
                    "Republican vs Republican (RxR). "+
                    "Row panels show subsamples by voters' partisanship. "+
                    "SE clustered by subject."
                    )
    },
    }
TABLES = {
        # main paper 
    # ----------
    # OS 
    # --
    'Aggregated by position (IxI and DxR)' : {
        'fn': 'tab-l1',
        'path': PATH_OS_TABLES, 
        'caption' : ("Causal effect of ideology position, candidates' "+
                     "party affiliation, and status threat exposure, "+
                     "aggregated across issues, "+
                     "on Democratic and Republican voters' probability "+
                     "of selecting the candidate (last two columns). "+
                     "Estimates use linear probability models "+
                     "estimated separately by voters' partisanship "+
                     "with clustered standard errors at the subject "+
                     "and issue levels (in parentheses)"),
    },
    'testing h5': {
        'fn': 'tab-l2',
        'path': PATH_OS_TABLES,
        'caption': ("Difference (last column) between the causal effect of "+
                    "the interaction between threat to "+
                    "social status of whites and Americans and "+
                    "candidates’ issue position in various areas "+
                    "on Democratic and Republican voters probability"+
                    "of selecting the candidate. Estimates from "+
                    "linear probability models with clustered "+
                    "SE by subject (in parenthesis). Candidate pair: "+
                    "CANDIDATE PAIR"
                    )
        
    },
     "educ" : {
         'fn': 'tab-g1',
         'path': PATH_OS_TABLES,
         'caption' : ("Relative Frequencies for Education: Census vs survey")
     },
    "inc" : {
        'fn': 'tab-g2',
        'path': PATH_OS_TABLES,
        'caption' : ("Relative Frequencies for Income: Census vs survey")
    },
    'age' : {
        'fn': 'tab-g3',
        'path': PATH_OS_TABLES,
        'caption' : ("Relative Frequencies for Age: Census vs survey")
    },
    "descriptive statistics" : {
        'fn': 'tab-h1',
        'path': PATH_OS_TABLES,
        'caption' : ("Descriptive statistics")
    },
    'balance' : {
        'fn': 'tab-h2',
        'path': PATH_OS_TABLES,
        'caption' : ("Sample Balance. Estimates are "+
                     "coefficients of a multinomial regression of "+
                     "treatment condition on the pre-treatment covariates")
    },
    'status threat sample' : {
        'fn': 'tab-h3',
        'path': PATH_OS_TABLES, 
        'caption': ('Exposure sample size.')
    },
    'conjoint sample' : {
        'fn': 'tab-h4',
        'path': PATH_OS_TABLES, 
        'caption': ('Conjoint groups sample size.')
    },
    'mc group' : {
        'fn': 'tab-j1',
        'path': PATH_OS_TABLES,
        'caption' : ("Factual manipulation check")
    },
    'mc score' : {
        'fn': 'tab-j2',
        'path': PATH_OS_TABLES,
        'caption' : ("Factual manipulation check: Scores distribution")
    },
    'mc break down' : {
        'fn': 'tab-j3',
        'path': PATH_OS_TABLES,
        'caption' : ("Factual manipulation check: Cases with 1 incorrect and 2 correct answers")
    },
    'mc: social stauts perception': {
        'fn': 'tab-j4',
        'path': PATH_OS_TABLES,
        'caption' : ("Effect of status threat exposure on "+
                     "social status perceptions")
    },
    'mc: social stauts anxiety': {
        'fn': 'tab-j5',
        'path': PATH_OS_TABLES,
        'caption' : ("Effect of status threat exposure on "+
                     "status anxiety")
    },
    'mc: prejudice': {
        'fn': 'tab-j6',
        'path': PATH_OS_TABLES,
        'caption' : ("Effect of status threat exposure on "+
                     "prejudice")
    },
    'status threat sample' : {
        'fn': 'tab-h3',
        'path': PATH_OS_TABLES, 
        'caption': ('Exposure sample size.')
    },
    'conjoint sample' : {
        'fn': 'tab-h4',
        'path': PATH_OS_TABLES, 
        'caption': ('Conjoint groups sample size.')
    },
    'conjoint sample by pair' : {
        'fn': 'tab-h5',
        'path': PATH_OS_TABLES, 
        'caption': ('Conjoint groups sample size.')
    },
    'LPM IxI' : {
        'fn': 'tab-i1',
        'path': PATH_OS_TABLES, 
        'caption': ('Linear probability model with IxI pairs.')
    },
    'LPM DxR' : {
        'fn': 'tab-i2',
        'path': PATH_OS_TABLES, 
        'caption': ('Linear probability model with DxR pairs.')
    },
    'LPM DxD' : {
        'fn': 'tab-i3',
        'path': PATH_OS_TABLES, 
        'caption': ('Linear probability model with DxD pairs.')
    },
    'LPM RxR' : {
        'fn': 'tab-i4',
        'path': PATH_OS_TABLES, 
        'caption': ('Linear probability model with RxR pairs.')
    },
    "LPM DxR pty-issue interaction" :{
        'fn': 'tab-i5',
        'path': PATH_OS_TABLES, 
        'caption': ('Linear probability model with DxR pairs and '+
                    'policy-party interactions.')
    },
    'number of conservative positions':{
        'fn': 'tab-i6',
        'path': PATH_OS_TABLES, 
        'caption': ('Predicted probabilities')
    },
    }

# * functions

def recode(df):
    df = (df
          .mutate(rid = tp.as_character('rid'))
          .relevel('status_threat', 'Status reassuring')
          .relevel("c_aff_ac", "liberal")
          .relevel("c_trade", "liberal")
          .relevel("c_abortion", "liberal")
          .relevel("c_immig", "liberal")
          .relevel("c_lgbt", "liberal")
          .relevel("c_red", "liberal")
          )
    return df

def estimate(pty, pair, formula, data, ref, model='LPM', cluster='rid'):
    vars = t4.formulas.extract_variables(formula)['variables']
    data = set_reference_level(data, ref)
    data = data.select(vars, cluster).drop_null().to_pandas()

    if model == 'LPM':
        res = lm(formula, data=data)
    elif model == 'logit':
        res = glm(formula, data=data, family=family.Binomial())
    res = res.fit(cov_type="cluster", cov_kwds={"groups": data[cluster]})
    return res

def estimate_saturated(pty, formula, data, ref, model='LPM', cluster='rid'):
    vars = t4.formulas.extract_variables(formula)['variables']
    data = set_reference_level(data, ref)
    data = data.select(vars, cluster).drop_null().to_pandas()

    if model == 'LPM':
        res = lm(formula, data=data)
    elif model == 'logit':
        res = glm(formula, data=data, family=family.Binomial())
    res = res.fit(cov_type="cluster", cov_kwds={"groups": data[cluster]})
    return res

def predict_saturated(pty, fit, formula, data, at):
    at_final= {}
    for pred, value in at.items():
        if value is not None:
            at_final[pred] = value
    at = at_final
    vars = t4.formulas.extract_variables(formula)['variables']
    data = data.select(vars)
    newdata = t4.simulate.newdata(data, at=at)
    pred = fit.get_prediction(newdata.to_pandas()).summary_frame(alpha=0.05)
    pred = newdata.bind_cols(tp.tibble(pred))
    return pred

def set_reference_level(data, ref):
    if ref is not None:
        for var, level in ref.items():
            data = data.relevel(var, ref=level)
    return data

def get_summary(fit):
    res = fit.summary2().tables[1].reset_index(drop=False, names='term')
    return tp.from_pandas(res)

def predict(pty, pair, fit, formula, data, at):
    if pair == 'DxR' or pair == 'RxD':
        at['c_party_affiliation'] = ['Democratic Party', 'Republican Party']
    vars = t4.formulas.extract_variables(formula)['variables']
    data = data.select(vars)
    newdata = t4.simulate.newdata(data, at=at)
    pred = fit.get_prediction(newdata.to_pandas()).summary_frame(alpha=0.05)
    pred = newdata.bind_cols(tp.tibble(pred))
    return pred

def get_speeders(data, minutes_min):
    return data.filter(tp.col("duration_min")>=minutes_min)

def count_positions(pred, position):
    """This function counts the number of issues set to an ideology
    'position' (conservative or liberal) in the prediction of
    support using the fitted model.
    """
    pred = (pred
            .mutate(**{f"n_{position}_positions": tp.map(
                ISSUES, lambda row: row.count(position)
                       )}
                    )
            )
    return pred

def compute_difference(tabraw):
    res_diff = tp.tibble()
    for pair in tabraw.pull('pty_pair').unique():
        tab = tabraw.filter(tp.col("pty_pair")==pair)
        dem = tab.filter(tp.col("pid").str.contains('Democ')).pull('fit')[0]
        rep = tab.filter(tp.col("pid").str.contains('Repub')).pull('fit')[0]

        tmp = (compute_difference_ancillary(dem, rep)
               .mutate(pty_pair = pair)
               )
        res_diff = res_diff.bind_rows(tmp)
    return res_diff

def compute_difference_ancillary(dem, rep):
    vars = dem.params.index
    res = tp.tibble()
    for var in vars:
        b_dem = dem.params[var]
        s_dem = dem.bse[var]
        p_dem = dem.pvalues[var]
        b_rep = rep.params[var]
        s_rep = rep.bse[var]
        p_rep = rep.pvalues[var]

        diff = b_dem - b_rep
        s_diff = np.sqrt(s_dem**2 + s_rep**2)

        z = diff / s_diff
        p = 2 * (1 - dnorm.cdf(abs(z), loc=0, scale=1) )

        tmp = tp.tibble({
            'term'    : [var],
            'b_dem'   : [b_dem],
            'b_rep'   : [b_rep],
            'diff'    : [diff],
            's_dem'   : [s_dem],
            'p_dem'   : [p_dem],
            's_rep'   : [s_rep],
            'p_rep'   : [p_rep],
            'z'       : [z],
            'p-value' : [p]
        })
        res = res.bind_rows(tmp)
    return res

def census_vs_survey(df, var):
    fn = PATH_DATA_FINAL / 'us-census.xlsx'
    census = tp.read_data(fn=fn, sheet_name=f'{var}-census')
    survey = (df
              .distinct('rid')
              .freq(var).mutate(educ=tp.as_integer(var))
              .rename({'Freq':'Survey'}))
    tab = (census
           .mutate(freq = 100*tp.col("freq"))
           .rename({'freq':'Census',
                    'category':'Group'})
           .left_join(survey, left_on='code', right_on='educ')
           .select('Group', 'N', 'Census', 'Survey')
           .mutate(Difference = tp.col("Census") - tp.col("Survey"))
           )
    return tab

def show_figure(g):
    try: g.save(PDF_OUTPUT, scale=1)
    except: pass


# * loading

fn = PATH_DATA_FINAL / 'survey.csv'
df = recode(tp.read_data(fn=fn))
df.glimpse(".")
# df = tp.read_data(fn=fn)

# fn = PATH_DATA_FINAL / 'survey-labels.json'
# LABELS = json.load(fn)

# * overview

df.distinct('rid').freq('pty_pair_group').print()

var = 'pty_pair_ordered'
var = 'pty_pair'
df.distinct('rid').freq(var).print()
tab = (df
       .select('rid', 'status_threat', var)
       .distinct('rid')
       .freq('status_threat', var)
       .arrange(var)
       )
tab.print()

# * ----- Main Paper ----
# * Estimation
# ** Aggregated (across issues)

print(f"Estimating aggregated effect (across issues):")

y = 'chc_stack'
treat     = 'status_threat'
cand_pty  = 'c_party_affiliation'  
adj       = " + ".join(ADJ_VARS)
formulas = {'Not adjusted': f"{y} ~ position * {treat}",
            'Adjusted'    : f"{y} ~ position * {treat} + {adj}"}
formulas
# 
ref = {
    'status_threat'        : 'Status reassuring',
}
res_agg = (df
           .select(ISSUES, y, treat, 'rid', 'pty_pair', cand_pty, 'pid', ADJ_VARS)
           .pivot_longer(cols=ISSUES, names_to='issue', values_to='position')
           .mutate(cluster = tp.col("issue") + tp.as_character(tp.col("rid")))
           .nest(by=['pid', 'pty_pair'])
           .crossing(adj = list(formulas.keys()),
                     model = ['logit', 'LPM'])
           .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
                   ref = ref)
           .mutate(
               n       = tp.map(['data'], lambda row: row[0].nrow),
               formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                      tp.col('formula') + f" + position*{treat}*{cand_pty}",
                                      True, tp.col('formula')),
               fit     = tp.map(['pid', 'pty_pair',
                                 'formula', 'data', 'ref', 'model'], lambda row:
                                estimate(*row, cluster=['cluster'])),
               summ    = tp.map(["fit"], lambda fit: get_summary(fit[0])),
           )
           )
res_agg

# res_agg.pull('data')[0]
# res_agg.pull('data')[0].freq('position')
# res_agg.pull('fit')[15].summary()


# ** Disaggregated (threat x position by pid)

print('Estimating issue position effects: ')
# 
y            = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
# formulas
interactions = ' + '.join([f'{i}*{treat}' for i in ISSUES])
interactions_pty =  ' + '.join([f'{i}*{cand_pty}*{treat}' for i in ISSUES])
adj          = " + ".join(ADJ_VARS)
formulas = {
    'Not adjusted': f"{y} ~ {interactions}",
    'Adjusted'    : f"{y} ~ {interactions} + {adj}"
}
formulas
# prediction (candidate's party is during prediction for partisan profiles)
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'c_red': ['liberal', 'conservative'],
    'c_immig': ['liberal', 'conservative'],
    'c_lgbt': ['liberal', 'conservative'],
    'c_aff_ac': ['liberal', 'conservative'],
    'c_trade': ['liberal', 'conservative'],
    'c_abortion': ['liberal', 'conservative'],
}
# 
ref = {
    'status_threat'        : 'Status reassuring',
    'c_party_affiliation'  : 'Democratic Party',
    'c_abortion'           : 'liberal',
    'c_aff_ac'             : 'liberal',
    'c_trade'              : 'liberal',
    'c_immig'              : 'liberal',
    'c_lgbt'               : 'liberal',
    'c_red'                : 'liberal',
}
# estimate
pooled = (df
          .nest('pty_pair')
          .mutate(pid = 'Pooled')
          )
res = (df
       .nest(['pid', 'pty_pair'])
       .bind_rows(pooled)
       .crossing(adj = list(formulas.keys()),
                 model = ['logit', 'LPM'])
       .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
               ref=ref)
       .mutate(
           formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                  tp.col('formula') + f" + {cand_pty}*{treat}",
                                  # tp.col('formula') + f" + {interactions_pty}",
                                  True, tp.col('formula')),

           fit  = tp.map(['pid', 'pty_pair', 'formula', 'data', 'ref', 'model'],
                         lambda row: estimate(*row, cluster='rid')),
           summ = tp.map(["fit"], lambda fit: get_summary(fit[0])),
           pred = tp.map(['pid', 'pty_pair', 'fit','formula','data'],
                         lambda fit: predict(*fit, predict_at)),
           nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
       )
       # pred is done for all combinations of candidates ideology positions across issues
       # this counts the number of issues with conservative positions used for the predictions:
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'conservative')) )
       # same for liberal positions
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'liberal')) )
       )
res


# ** Partisan pairs (w/ cand pty interaction)

print('Estimating issue position effects: ')

y            = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
# formulas
interactions = ' + '.join([f'{i}*{treat}' for i in ISSUES])
interactions_pty =  ' + '.join([f'{i}*{cand_pty}*{treat}' for i in ISSUES])
adj          = " + ".join(ADJ_VARS)
formulas = {
    'Not adjusted': f"{y} ~ {interactions}",
    'Adjusted'    : f"{y} ~ {interactions} + {adj}"
}
# pprint(formulas)
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'pty_pair' : ['DxR', 'RxR', 'DxD'],
    'c_red': ['liberal', 'conservative'],
    'c_immig': ['liberal', 'conservative'],
    'c_lgbt': ['liberal', 'conservative'],
    'c_aff_ac': ['liberal', 'conservative'],
    'c_trade': ['liberal', 'conservative'],
    'c_abortion': ['liberal', 'conservative'],
}
predict_at_pty = {
    'c_party_affiliation' : ['Democratic Party',
                             'Republican Party'],
}
ref = {
    'status_threat'        : 'Status reassuring',
    'c_party_affiliation'  : 'Democratic Party',
    'c_abortion'           : 'liberal',
    'c_aff_ac'             : 'liberal',
    'c_trade'              : 'liberal',
    'c_immig'              : 'liberal',
    'c_lgbt'               : 'liberal',
    'c_red'                : 'liberal',
}
# estimate
res_pty_int = (df
           .filter(tp.col("pty_pair").is_in(['DxR', 'DxD', 'RxR']))
           .nest(['pid', "pty_pair"])
           .crossing(adj = list(formulas.keys()),
                     model = ['logit', 'LPM'])
           .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
                   ref=ref,
                   pred_at = tp.case_when(tp.col("pty_pair") == 'DxR', predict_at | predict_at_pty,
                                          True, predict_at 
                                          ))
           .mutate(
               formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                      tp.col('formula') + f" + {interactions_pty}",
                                      True, tp.col('formula')),
               # 
               fit  = tp.map(['pid', 'formula', 'data', 'ref', 'model'],
                             lambda row: estimate_saturated(*row, cluster='rid')),
               summ = tp.map(["fit"], lambda fit: get_summary(fit[0])),
               pred = tp.map(['pid', 'fit','formula','data', 'pred_at'],
                             lambda fit: predict_saturated(*fit)),
               nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
           )
           # pred is done for all combinations of candidates ideology positions across issues
           # this counts the number of issues with conservative positions used for the predictions:
           .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'conservative')) )
           # same for liberal positions
           .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'liberal')) )
           )
res_pty_int


# ** Compute differences Dem x Rep

res
adj = 'Not adjusted'
model='LPM'
res_diff = (res
            .filter(tp.col("model")==model)
            .filter(tp.col('adj')==adj)
            .filter(tp.col("pid")!='Pooled')
            # .select('pid', 'pty_pair', 'fit')
            # .arrange('pty_pair', 'pid', 'adh')
            )
res_diff
res_diff = compute_difference(res_diff)
res_diff


# ** Number of conservative positions

print(f"Estimating effect of number of conservative positions...")

y = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
adj          = " + ".join(ADJ_VARS)
formulas = {'Not adjusted': f"{y} ~ c_ncons * {treat}",
            'Adjusted'    : f"{y} ~ c_ncons * {treat} + {adj}"}
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'c_ncons': list(range(0, 7)),
}
# 
ref = {
    'status_threat'        : 'Status reassuring',
}
res_ncons = (df
             .select(ISSUES, y, treat, 'rid', 'pty_pair', cand_pty, 'pid', ADJ_VARS, 'c_ncons')
             .mutate(cluster = tp.as_character(tp.col("rid")))
             .nest(by=['pid', 'pty_pair'])
             .crossing(adj = list(formulas.keys()),
                       model = ['logit', 'LPM'])
             .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
                     ref = ref)
             .mutate(
                 n       = tp.map(['data'], lambda row: row[0].nrow),
                 formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                        tp.col('formula') + f" + {cand_pty}*c_ncons",
                                        True, tp.col('formula')),
                 fit     = tp.map(['pid', 'pty_pair', 'formula', 'data', 'ref', 'model'], lambda row:
                                  estimate(*row, cluster=['cluster'])),
                 summ    = tp.map(["fit"], lambda fit: get_summary(fit[0])),
                 pred = tp.map(['pid', 'pty_pair', 'fit','formula','data'],
                               lambda fit: predict(*fit, predict_at)),
                 nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
           )
           )
res_ncons

# * Table

# * Figures
# ** Figure 1

set_theme('sci', borders=False)
# 
figures = {
    'Status reassuring'             : 'main barplot',
    'Racial threat'                 : 'barplot under racial threat',
    'Nationality threat'            : 'barplot under nationality threat',
    'Racial and nationality threat' : 'barplot under racial and nationality threat',
}
# 
for status_threat, figure in figures.items():
    y = 'chc_stack'
    pair = 'pty_pair_group' 
    pairs = ['IxI', 'DxR']
    tab = (df
           .filter(tp.col('pty_pair').is_in(pairs))
           .filter(tp.col('status_threat')==status_threat)
           .select(y, 'pid', ISSUES, 'c_party_affiliation', pair)
           .pivot_longer(cols=tp.matches("c_"), names_to='issue', values_to='position')
           .replace({'position':{'Republican Party': 'Conservative',
                                 'Democratic Party': 'Liberal',
                                 }})
           .freq(y, [ 'pid', pair, 'issue', 'position'])
           .filter(tp.col(y)==1)
           .filter(~((tp.col('position')=='Independent') &
                     (tp.col('issue')=='c_party_affiliation')))
           .mutate(
               issue = tp.case_when(
                   (tp.col('issue')=='c_party_affiliation') &
                   (tp.col('position')=='Liberal'), ' Party: Dem.',

               (tp.col('issue')=='c_party_affiliation') &
                   (tp.col('position')=='Conservative'), ' Party: Rep.',

               True, tp.col('issue')
               ),
               facet = tp.case_when(tp.col(pair)=="Partisan",
                                    tp.col('position').str.to_titlecase() + ' candidates (with party affliation)',
                                    True, 
                                    tp.col('position').str.to_titlecase() +
                                    ' candidates (without party affiliation)',
                                    ),
               facet1 = tp.case_when(tp.col(pair)=="Partisan", ' Partisan pair: Democratic vs Republican candidates',
                                     tp.col(pair)!="Partisan", 'Non-partisan pair: Independents candidates',
                                     ),
               facet2 = tp.col('position').str.to_titlecase() + ' candidates'
           )
           .replace({'issue':{v:l for v, l in VARS.items() if v in ISSUES + ['c_party_affiliation']}})
           .mutate(
               Freq = tp.col('Freq')/100,
               # issue = tp.map(['issue'],  lambda row: row[0].split(' ')) 
           )
           .replace({'issue':{'Affirmative action':'Aff. Action',
                              'Immigration':'Immig.',
                              'Trade with China':"Trade",
                              # 'LGBT rights':'LGBT',
                          'Redistribution':'Redistr.'}})
           )
    tab
    print(tab)
    # 
    # tab.glimpse(".")
    # 
    x         = 'issue:N'
    y         = 'Freq'
    fill      = 'pid:N'
    color     = fill
    linetype  = None
    size      = None
    opacity   = None
    facet     = 'facet'
    row       = 'facet2'
    column    = 'facet1'
    # 
    leg_title = None
    title     = None
    subtitle  = None
    footnote  = None
    xlab      = None
    ylab     = ['Frequency the candidate was selected',
                 "("+status_threat+" condition)"]
    dodge     = 0.6
    digits    = 0
    # 
    base = (alt.Chart(tab.to_pandas()))
    bar = (base.mark_bar() # .transform_calculate(x="split(datum.x, ' ')")
           .encode(
               x       = alt.X(x,  title=xlab),
               y       = alt.Y(y, title=None).scale(domain=[0,.75]),
               fill    = alt.Fill(fill).title(leg_title),
               xOffset = alt.XOffset(fill),
           ))
    txt = (base.mark_text(dy=-5, size=8)
           .encode(
               x       = alt.X(x,  title=xlab),
               y       = alt.Y(y, title=None),
               text    = alt.Text(y).format(f'.{digits}%'),
               fill    = alt.Fill(fill),
               xOffset = alt.XOffset(fill),
           ))
    # 
    g = (alt.layer(txt, bar)
         .properties(width=300, height=100)
         .facet(facet=alt.Facet(facet,
                                header=alt.Header(title=ylab,
                                                  titlePadding=0,
                                                  titleOrient='left',
                                                  titleAnchor='middle',
                                                  titleAlign='center')),
                columns=2, spacing={"row": 12, "column": 10})
         .resolve_scale(#y='independent',
             x='independent',
             xOffset='independent'
         )
         .configure_range(category=COLORS.values())
         )
    show_figure(g)
    # 
    if SAVE:
        caption = FIGURES[figure]['caption']
        label = FIGURES[figure]['fn']
        fn = FIGURES[figure]['path'] / label
        save_figure(fn, g, tab, caption=caption, label=label)



# ** Figure 2

figure = 'non-partisan marginal effects (prr)'
set_theme('sci', borders=True)
# 
# 
model = 'LPM'
adj = 'Not adjusted'
pair = 'DxR'
pair = 'IxI'
short_names = {'Intercept': '  Intercept (liberal positions)',
               'Nationality threat': 'Status threat to Americans',
               'Racial threat': 'Status threat to whites',
               'Racial and nationality threat': 'Status threat to whites and Americans',
               }
tab = (res
       .filter(tp.col("model")==model)
       .filter(tp.col('pty_pair')==pair)
       .filter(tp.col('adj')==adj)
       .select('pid', 'summ', 'nobs')
       .unnest('summ')
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.|\\]', ''),)
       .separate('term', ['issue', 'threat'], sep=':')
       .mutate(threat = tp.case_when(tp.col("threat").is_null(), 'Control',
                                     True , tp.col("threat")),
               condition = tp.case_when((tp.col("issue").str.contains('^c_|Interc')) &
                                        (tp.col("threat")==''), 'Status reassuring',
                                        True, 'Status threat'),)
       .replace({'issue':VARS})
       .replace({'issue': short_names, 'threat':short_names})
       .rename({'[0.025':'lo', '0.975]':"hi", 'Coef.':'estimate'})
       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               #pvalue = tp.case_when(tp.col('P>|z|')<=0.05, '*', True,  ' '),
               # issue = tp.case_when(tp.col("threat")!='', tp.col("issue") + " x " + tp.col("threat"),
               #                      True, tp.col("issue")),
               pid = tp.as_factor('pid', ['Pooled', 'Democratic voter', 'Republican voter'])
               )
       #
       .filter(~tp.col("issue").str.contains('Intercept'))
       .filter(~tp.col("issue").str.contains('Status'))
       )
tab
tab.glimpse(".")
nobs = "; ".join( tab.select('pid', 'nobs').distinct()
                  .mutate(nobs=tp.col("pid")+": "+tp.col("nobs").cast(str))
                  .pull('nobs').to_list())
# 
x         = 'estimate'
y         = 'issue'
fill      = 'threat:N'
color     = fill
linetype  = None
shape     = 'threat:N'
size      = None
opacity   = None
facet1    = 'pid'
facet2    = None
# 
leg_title = 'Social Status Exposure Condition'
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Causal Effect of Candidate's Policy Position on Candidate Support"
ylab      = "Candidates's Conservative Policy Position"
dodge     = .7
olors = ['gray',  'white']
shapes = ['circle', 'triangle', 'triangle-down', 'square']
colors = ['black', 'darkgray',  'gray', 'white']
bold = " | ".join([f"datum.value == '{VARS[issue]}'" for issue in ISSUES])
# 
set_theme('sci', borders=True)
base = (alt.Chart(tab.to_polars())
        .encode(
            # color   = alt.Color(color),
        ))
pts = (base.mark_point()
       .encode(
           x       = alt.X(x, title=None),
           y         = (alt.Y(y, title=ylab).scale(padding=dodge)
                        # .axis(labelFontWeight=alt.condition(bold, alt.value(800), alt.value(300)))
                        ),
           size    = alt.value(60),
           color   = alt.value('black'),
           fill    = alt.Fill(fill).title(leg_title),
           # fill    = alt.value('black'),
           shape   = alt.Shape(shape).title(leg_title).scale(range=shapes),
           # # opacity = alt.Opacity(opacity)
           yOffset = alt.YOffset(fill),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x         = alt.X('lo', title=xlab),
          x2        = alt.X2('hi'),
          y         = alt.Y(y, title=ylab),
          # color   = alt.Color(color).legend(None),
          yOffset = alt.YOffset(fill),
      ))
txt = (base.mark_text(dy=-2, size=15)
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           text     =  alt.Text("pvalue"),
           yOffset = alt.YOffset(fill),
       ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=.7, color='black')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts, txt)
     .properties(width=150, height=250)
     .facet(facet=alt.Facet(facet1).header(title=xlab, titleOrient='bottom',
                                           titleAnchor='middle',
                                           titleAlign='center'),
            columns=4)
     .configure_legend(columns=2)
     # .resolve_scale(x='shared')
     # .resolve_scale(x='independent',
     #                #y='independent'
     #                )
     .configure_range(category=colors)
     )
show_figure(g)
# 
if SAVE:
    caption = FIGURES[figure]['caption']
    label = FIGURES[figure]['fn']
    fn = FIGURES[figure]['path'] / label
    save_figure(fn, g, tab, caption=caption, label=label)


# ** Figure 3

set_theme('sci', borders=True)
figure = 'partisan marginal effects (prr)'
# 
# 
model = 'LPM'
adj = 'Not adjusted'
pair = ['DxR', 'DxD', 'RxR']
short_names = {'Intercept': '  Intercept (liberal positions)',
               'Nationality threat': 'Status threat to Americans',
               'Racial threat': 'Status threat to whites',
               'Racial and nationality threat': 'Status threat to whites and Americans',
               }
tab = (res
       .filter(tp.col("model")==model)
       .filter(tp.col("pid")!='Pooled')
       .filter(tp.col('pty_pair').is_in(pair))
       .filter(tp.col('adj')==adj)
       .select('pid', {'pty_pair':'pair'}, 'summ', 'nobs')
       .unnest('summ')
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.|\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'c_party_affiliation\\[T.|]', ' '),)
       .separate('term', ['issue', 'threat'], sep=':')
       .mutate(threat = tp.case_when(tp.col("threat").is_null(), 'Control',
                                     True , tp.col("threat")),
               condition = tp.case_when((tp.col("issue").str.contains('^c_|Interc|Party$')) &
                                        (tp.col("threat")==''), 'Status reassuring',
                                        True, 'Status threat'),
               pair = tp.case_when(tp.col("pair")=='DxD', ' Democratic caniddates',
                                   tp.col("pair")=="DxR", 'Democratic (Ref.) vs Republican',
                                   tp.col("pair")=='RxR', 'Republican caniddates',
                                   True, tp.col("pair")
                                   ),
               )
       .replace({'issue':VARS})
       .replace({'issue': short_names, 'threat':short_names})
       .rename({'[0.025':'lo', '0.975]':"hi"})
       .rename({'Coef.':'estimate'})

       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               #pvalue = tp.case_when(tp.col('P>|z|')<=0.05, '*', True,  ' '),
               # issue = tp.case_when(tp.col("threat")!='', tp.col("issue") + " x " + tp.col("threat"),
               #                      True, tp.col("issue")),
               pid = tp.as_factor('pid', ['Pooled', 'Democratic voter', 'Republican voter'])
               )
       #
       .filter(~tp.col("issue").str.contains('Intercept'))
       .filter(~tp.col("issue").str.contains('Status'))
       )
tab
tab.glimpse(".")
# 
nobs = "; ".join( tab.select('pid', 'nobs').distinct()
                  .mutate(nobs=tp.col("pid")+": "+tp.col("nobs").cast(str))
                  .pull('nobs').to_list())
# 
x         = 'estimate'
y         = 'issue'
fill      = 'threat:N'
color     = fill
linetype  = None
shape     = 'threat:N'
size      = None
opacity   = None
facet1    = 'pair'
facet2    = 'pid'
# 
leg_title = 'Social Status Exposure Condition'
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Causal Effectof Candidate's Policy Position on Candidate Support"
ylab      = "Candidate's Conservative Policy Position"
dodge     = 0.6
shapes = ['circle', 'triangle', 'triangle-down', 'square']
colors = ['black', 'darkgray',  'gray', 'white']
bold = " | ".join([f"datum.value == '{VARS[issue]}'" for issue in ISSUES])
bold += " | datum.value == ' Republican Party'"
bold
tab.pull('issue').to_list()
# 
set_theme('sci', borders=True)
base = (alt.Chart(tab.to_polars())
        .encode(
            # color   = alt.Color(color),
        ))
pts = (base.mark_point()
       .encode(
           x       = alt.X(x, title=None),
           y         = (alt.Y(y, title=ylab).scale(padding=dodge)
                        # .axis(labelFontWeight=alt.condition(bold, alt.value(800), alt.value(300)))
                        ),
           size    = alt.value(60),
           color   = alt.value('black'),
           fill    = alt.Fill(fill).title(leg_title),
           # fill    = alt.value('black'),
           shape   = alt.Shape(shape).title(leg_title).scale(range=shapes),
           # # opacity = alt.Opacity(opacity)
           yOffset = alt.YOffset(fill),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x         = alt.X('lo', title=xlab),
          x2        = alt.X2('hi'),
          y         = alt.Y(y, title=ylab),
          # color   = alt.Color(color).legend(None),
          yOffset = alt.YOffset(fill),
      ))
txt = (base.mark_text(dy=-4.5, size=15)
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           text     =  alt.Text("pvalue"),
           yOffset = alt.YOffset(fill),
       ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=.7, color='black')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts, txt)
     .properties(width=150, height=250)
     .facet(row=alt.Facet(facet2).header(title=xlab, titleOrient='bottom',
                                           titleAnchor='middle',
                                           titleAlign='center'),
            column=alt.Column(facet1),
            columns=4)
     .configure_legend(columns=2)
     # .resolve_scale(x='shared')
     # .resolve_scale(x='independent',
     #                #y='independent'
     #                )
     .configure_range(category=colors)
     )
show_figure(g)
# 
if SAVE:
    caption = FIGURES[figure]['caption']
    label = FIGURES[figure]['fn']
    fn = FIGURES[figure]['path'] / label
    save_figure(fn, g, tab, caption=caption, label=label)

# report
print('Report for Figure conservative-on-redistribution plot:')
(tab
 .filter(tp.col("pair").str.contains('DxR'))
 .filter(tp.col("issue").str.contains('Republican|Intercept'))
 .filter(tp.col("threat")=='')
 .select('pid', 'issue', 'threat', 'condition', 'estimate')
).print()
print('Report for Figure conservative-on-redistribution plot:')
(tab
 .filter(tp.col("pair").str.contains('DxR'))
 .filter(tp.col("issue").str.contains('Abortion|Intercept'))
 .filter(tp.col("threat")=='')
 .select('pid', 'issue', 'threat', 'condition', 'estimate')
).print()


# ** Figure 4

figure = 'number of conservative positions'
set_theme('sci', borders=True)
# 
model = 'logit'
adj = 'Not adjusted'
threat_order = [
    'Status reassuring',
    'Racial threat',
    'Nationality threat',
    "Racial and nationality threat"
]
tab = (res_ncons
       .filter(tp.col("model")==model)
       .filter(tp.col("adj")==adj)
       .select('pid', 'pty_pair',  'pred', 'model')
       .unnest('pred')
       .mutate(
           pty_pair = tp.case_when(
               tp.col("pty_pair")=='DxR',
               tp.col("pty_pair") + " (Candidate from the "+tp.col("c_party_affiliation")+")",
               True, tp.col("pty_pair")),
           # status_threat = tp.as_factor('status_threat', threat_order)
              )
       .mutate(status_threat = tp.str_replace_all('status_threat', 'Status', '  Status'))
       .mutate(status_threat = tp.str_replace_all('status_threat', 'Racial', ' Racial'),)
       )
x         = 'c_ncons'
y         = 'mean'
fill      = 'status_threat:N'
color     = fill
linetype  = 'pid:N'
shape     = fill
size      = None
opacity   = None
facet1    = 'pty_pair'
facet2    = None
# 
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = None
xlab_shared = 'Number of conservative positions across issues'
ylab      = ["Predicted probability of ", 'voting for the candidate']
dodge     = 1
# 
shapes = ['circle', 'triangle', 'triangle-down', 'square']
base = (alt.Chart(tab.to_polars()))
pts = (base.mark_point()
       .encode(
           x         = alt.X(x, title=xlab).scale(padding=dodge),
           y         = alt.Y(y, title=ylab),
           fill    = alt.Fill(fill).legend(columns=2, title=None),
           shape   = alt.Color(shape).legend(columns=2, title=None),
           # color   = alt.Color(color),
           # size    = alt.Size(size),
           # opacity = alt.Opacity(opacity)
           # yOffset = alt.YOffset(fill),
           xOffset = alt.XOffset(fill),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x       = alt.X(x, title=xlab),
          y       = alt.Y('mean_ci_lower', title=ylab),
          y2      = alt.Y2('mean_ci_upper'),
          # color   = alt.Color(color)
          # yOffset = alt.YOffset(fill),
          xOffset = alt.XOffset(fill),
      ))
lns = (base.mark_line()
       .encode(
           x           = alt.X(x, title=xlab),
           y           = alt.Y(y, title=ylab),
           color       = alt.Color(color).legend(None),
           strokeDash  = alt.StrokeDash(linetype).legend(symbolSize=100, columns=1, title=None),
           xOffset = alt.XOffset(fill),
       ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=1.2, color='black')
         .encode(
             y = alt.datum(0.5)
         ))
g = (alt.layer(vline, lns, pts)
     .properties(width=200, height=150)
     .facet(facet=alt.Facet(facet1,
                            header = alt.Header(title=xlab_shared,
                                                titleAnchor='middle',
                                                titleAlign='center',
                                                titleOrient='bottom')), columns=3)
     .resolve_scale(
         # shape='shared',
         # color='shared'
         # x='independent',
         # y='independent'
     )
     # .add_params(selection)
     # .configure_legend(orient='top')
     )
show_figure(g)
# 
if SAVE:
    caption = FIGURES[figure]['caption']
    label = FIGURES[figure]['fn']
    fn = FIGURES[figure]['path'] / label
    save_figure(fn, g, tab, caption=caption, label=label)

# * -------  OS  --------
# * Estimation
# ** Robustness
# *** Partisanship strenght
# *** PSID
# *** speeders


print('Estimating issue position effects for w/o speeders... ', end="")
# 
y            = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
# formulas
interactions = ' + '.join([f'{i}*{treat}' for i in ISSUES])
interactions_pty =  ' + '.join([f'{i}*{cand_pty}*{treat}' for i in ISSUES])
adj          = " + ".join(ADJ_VARS)
formulas = {
    'Not adjusted': f"{y} ~ {interactions}",
    # 'Adjusted'    : f"{y} ~ {interactions} + {adj}"
}
formulas
# prediction (candidate's party is during prediction for partisan profiles)
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'c_red': ['liberal', 'conservative'],
    'c_immig': ['liberal', 'conservative'],
    'c_lgbt': ['liberal', 'conservative'],
    'c_aff_ac': ['liberal', 'conservative'],
    'c_trade': ['liberal', 'conservative'],
    'c_abortion': ['liberal', 'conservative'],
}
# 
ref = {
    'status_threat'        : 'Status reassuring',
    'c_party_affiliation'  : 'Democratic Party',
    'c_abortion'           : 'liberal',
    'c_aff_ac'             : 'liberal',
    'c_trade'              : 'liberal',
    'c_immig'              : 'liberal',
    'c_lgbt'               : 'liberal',
    'c_red'                : 'liberal',
}
# estimate
median = df.pull('duration_min').median()
res_speeders = (df
       # .mutate(speeders50 = tp.ifelse(tp.col("duration_min")<=med*.5, 1, 0)
       #         speeders50 = tp.col("duration_min")<=med*.5,
       #         )
       .nest(['pid', 'pty_pair'])
       .crossing(speeder_min = [0.0, .5*median, .4*median, .3*median], 
                 adj = list(formulas.keys()),
                 model = ['LPM']
                 )
       .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
               ref=ref)
       .mutate(
           data = tp.map(['data', 'speeder_min'], lambda row: get_speeders(*row)),
           n    = tp.map(['data'], lambda row: row[0].nrow),
           formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                  tp.col('formula') + f" + {cand_pty}*{treat}",
                                  # tp.col('formula') + f" + {interactions_pty}",
                                  True, tp.col('formula')),

           fit  = tp.map(['pid', 'pty_pair', 'formula', 'data', 'ref', 'model'],
                         lambda row: estimate(*row, cluster='rid')),
           summ = tp.map(["fit"], lambda fit: get_summary(fit[0])),
           pred = tp.map(['pid', 'pty_pair', 'fit','formula','data'],
                         lambda fit: predict(*fit, predict_at)),
           nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
       )
       # pred is done for all combinations of candidates ideology positions across issues
       # this counts the number of issues with conservative positions used for the predictions:
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'conservative')) )
       # same for liberal positions
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'liberal')) )
       )
res_speeders 
print('done!')




# ** Balance

print(f"Checking pre-treatment covariate balance...", end="")

df.pull('status_threat').unique().to_list()

st_code ={"Status reassuring"             : 1,
          "Racial threat"                 : 2,
          "Nationality threat"            : 3,
          "Racial and nationality threat" : 4,
          }
dat = (df
       .distinct('rid')
       .select('status_threat', ADJ_VARS, 'rid')
       .mutate(st_num = tp.col("status_threat"))
       .replace({"st_num" : st_code})
       .to_pandas()
       )
# 
# estimate propensity score
f = f"st_num ~ {' + '.join(ADJ_VARS)}"
res_bal_fit =  mlogit(f, data=dat).fit(disp=False, method='lbfgs')
# 
# collect
res_bal = tp.tibble()
for st in range(1, len(st_code)):
    st_label = [l for l, v in st_code.items() if v== st+1][0]
    summ = (tp.from_pandas(res_bal_fit
                           .summary2()
                           .tables[st].iloc[:,1:]
                           .reset_index(drop=False)
                           )
            .mutate(status_threat=st_label)
            )
    res_bal = res_bal.bind_rows(summ)

print('done!')


# ** Manipulation checks
# ** Disaggregated (threat x position by pid: MC subset)

print('Estimating issue position effects: ')
# 
y            = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
# formulas
interactions = ' + '.join([f'{i}*{treat}' for i in ISSUES])
interactions_pty =  ' + '.join([f'{i}*{cand_pty}*{treat}' for i in ISSUES])
adj          = " + ".join(ADJ_VARS)
formulas = {
    'Not adjusted': f"{y} ~ {interactions}",
    'Adjusted'    : f"{y} ~ {interactions} + {adj}"
}
formulas
# prediction (candidate's party is during prediction for partisan profiles)
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'c_red': ['liberal', 'conservative'],
    'c_immig': ['liberal', 'conservative'],
    'c_lgbt': ['liberal', 'conservative'],
    'c_aff_ac': ['liberal', 'conservative'],
    'c_trade': ['liberal', 'conservative'],
    'c_abortion': ['liberal', 'conservative'],
}
# 
ref = {
    'status_threat'        : 'Status reassuring',
    'c_party_affiliation'  : 'Democratic Party',
    'c_abortion'           : 'liberal',
    'c_aff_ac'             : 'liberal',
    'c_trade'              : 'liberal',
    'c_immig'              : 'liberal',
    'c_lgbt'               : 'liberal',
    'c_red'                : 'liberal',
}
# estimate
pooled = (df
          .nest('pty_pair')
          .mutate(pid = 'Pooled')
          )
res_mc_all_correct = (df
       .filter(tp.col("mc_group")=='All correct')
       .nest(['pid', 'pty_pair'])
       .bind_rows(pooled)
       .crossing(adj = list(formulas.keys()),
                 model = ['logit', 'LPM'])
       .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
               ref=ref)
       .mutate(
           formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                  tp.col('formula') + f" + {cand_pty}*{treat}",
                                  # tp.col('formula') + f" + {interactions_pty}",
                                  True, tp.col('formula')),

           fit  = tp.map(['pid', 'pty_pair', 'formula', 'data', 'ref', 'model'],
                         lambda row: estimate(*row, cluster='rid')),
           summ = tp.map(["fit"], lambda fit: get_summary(fit[0])),
           pred = tp.map(['pid', 'pty_pair', 'fit','formula','data'],
                         lambda fit: predict(*fit, predict_at)),
           nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
       )
       # pred is done for all combinations of candidates ideology positions across issues
       # this counts the number of issues with conservative positions used for the predictions:
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'conservative')) )
       # same for liberal positions
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'liberal')) )
       )
res_mc_all_correct


# ** Effect on social status perception (ssp)

ssp = df.select(tp.matches("^ssp")).names
vars = {v:VARS[v].replace("Perception: ", '') for v in ssp}
res_mc_ssp = {}
for var, label in vars.items():
    print(f'MC: Estimating treatment effect on {var}...', end='')
    res_mc_ssp[label] = lm(f"{var} ~ status_threat",
                           data=df.distinct('rid').to_pandas()).fit()
    print('done!')

# ** Effect on social status axiety (SA)

# 
sa = df.select(tp.matches("^sa")).names
vars = {v:VARS[v] for v in sa }
res_mc_sa = {}
for var, label in vars.items():
    print(f'Estimating treatment effect on {label} ({var})...', end='')
    res_mc_sa[label] = lm(f"{var} ~ status_threat",
                          data=df.distinct('rid').to_pandas()).fit()
    print('done!')

# ** Effect on generalized prejudice (GP)

gps = df.select(tp.matches("^gp")).names
vars = {gp:VARS[gp] for gp in gps}
# 
res_mc_gp = {}
for var, label in vars.items():
    print(f"Estimating treatment effect on {label} ({var})...", end='')
    res_mc_gp[label] = lm(f"{var} ~ status_threat", data=df.distinct('rid').to_pandas()).fit()
    print('done!')

# ** Diagnostics: task order effects

df.glimpse(".")

print('Estimating issue position effects: ')
# 
y            = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
# formulas
interactions = ' + '.join([f'{i}*{treat}*task' for i in ISSUES])
interactions_pty =  ' + '.join([f'{i}*{cand_pty}*{treat}*task' for i in ISSUES])
adj          = " + ".join(ADJ_VARS)
formulas = {
    'Not adjusted': f"{y} ~ {interactions}",
    'Adjusted'    : f"{y} ~ {interactions} + {adj}"
}
formulas
# prediction (candidate's party is during prediction for partisan profiles)
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'c_red': ['liberal', 'conservative'],
    'c_immig': ['liberal', 'conservative'],
    'c_lgbt': ['liberal', 'conservative'],
    'c_aff_ac': ['liberal', 'conservative'],
    'c_trade': ['liberal', 'conservative'],
    'c_abortion': ['liberal', 'conservative'],
}
# 
ref = {
    'status_threat'        : 'Status reassuring',
    'c_party_affiliation'  : 'Democratic Party',
    'c_abortion'           : 'liberal',
    'c_aff_ac'             : 'liberal',
    'c_trade'              : 'liberal',
    'c_immig'              : 'liberal',
    'c_lgbt'               : 'liberal',
    'c_red'                : 'liberal',
}
# estimate
pooled = (df
          .nest('pty_pair')
          .mutate(pid = 'Pooled')
          )
res_order_effect = (df
       .nest(['pid', 'pty_pair'])
       .bind_rows(pooled)
       .crossing(adj = list(formulas.keys()),
                 model = ['logit', 'LPM'])
       .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
               ref=ref)
       .mutate(
           formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                  tp.col('formula') + f" + {cand_pty}*{treat}",
                                  # tp.col('formula') + f" + {interactions_pty}",
                                  True, tp.col('formula')),

           fit  = tp.map(['pid', 'pty_pair', 'formula', 'data', 'ref', 'model'],
                         lambda row: estimate(*row, cluster='rid')),
           summ = tp.map(["fit"], lambda fit: get_summary(fit[0])),
           pred = tp.map(['pid', 'pty_pair', 'fit','formula','data'],
                         lambda fit: predict(*fit, predict_at)),
           nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
       )
       # pred is done for all combinations of candidates ideology positions across issues
       # this counts the number of issues with conservative positions used for the predictions:
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'conservative')) )
       # same for liberal positions
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'liberal')) )
       )
res_order_effect


# ** Diagnostics: profile order effects

print('Estimating issue position effects: ')
# 
y            = 'chc_stack'
treat        = 'status_threat'
cand_pty     = 'c_party_affiliation'  
# formulas
interactions = ' + '.join([f'{i}*{treat}*cand' for i in ISSUES])
interactions_pty =  ' + '.join([f'{i}*{cand_pty}*{treat}*cand' for i in ISSUES])
adj          = " + ".join(ADJ_VARS)
formulas = {
    'Not adjusted': f"{y} ~ {interactions}",
    'Adjusted'    : f"{y} ~ {interactions} + {adj}"
}
formulas
# prediction (candidate's party is during prediction for partisan profiles)
predict_at = {
    'status_threat':df.pull('status_threat').unique().to_list(),
    'c_red': ['liberal', 'conservative'],
    'c_immig': ['liberal', 'conservative'],
    'c_lgbt': ['liberal', 'conservative'],
    'c_aff_ac': ['liberal', 'conservative'],
    'c_trade': ['liberal', 'conservative'],
    'c_abortion': ['liberal', 'conservative'],
}
# 
ref = {
    'status_threat'        : 'Status reassuring',
    'c_party_affiliation'  : 'Democratic Party',
    'c_abortion'           : 'liberal',
    'c_aff_ac'             : 'liberal',
    'c_trade'              : 'liberal',
    'c_immig'              : 'liberal',
    'c_lgbt'               : 'liberal',
    'c_red'                : 'liberal',
}
# estimate
pooled = (df
          .nest('pty_pair')
          .mutate(pid = 'Pooled')
          )
res_cand_order_effect = (df
       .nest(['pid', 'pty_pair'])
       .bind_rows(pooled)
       .crossing(adj = list(formulas.keys()),
                 model = ['logit', 'LPM'])
       .mutate(formula = tp.map(['adj'], lambda adj: formulas[adj[0]]),
               ref=ref)
       .mutate(
           formula = tp.case_when(tp.col("pty_pair") == 'DxR',
                                  tp.col('formula') + f" + {cand_pty}*{treat}",
                                  # tp.col('formula') + f" + {interactions_pty}",
                                  True, tp.col('formula')),

           fit  = tp.map(['pid', 'pty_pair', 'formula', 'data', 'ref', 'model'],
                         lambda row: estimate(*row, cluster='rid')),
           summ = tp.map(["fit"], lambda fit: get_summary(fit[0])),
           pred = tp.map(['pid', 'pty_pair', 'fit','formula','data'],
                         lambda fit: predict(*fit, predict_at)),
           nobs = tp.map(['fit'], lambda fit: int(fit[0].nobs))
       )
       # pred is done for all combinations of candidates ideology positions across issues
       # this counts the number of issues with conservative positions used for the predictions:
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'conservative')) )
       # same for liberal positions
       .mutate(pred = tp.map(['pred'], lambda pred: count_positions(*pred, 'liberal')) )
       )
res_cand_order_effect


# * Tables
# ** DONE Table G1-3: Demographics vs Census

tables = ['educ', 'inc', 'age']
for table in tables:
    tab = census_vs_survey(df, var=table)
    tab.print()
    # latex table 
    # -----------
    caption = TABLES[table]['caption']
    label = TABLES[table]['fn']
    tabl = tab.to_latex(caption = caption,
                        label = label,
                        align = 'lcccc',
                        footnotes = None)
    print(tabl)
    if SAVE:
        fn = TABLES[table]['path'] / TABLES[table]['fn']
        save_table(fn, tab, tabl)

# ** DONE Table H1: Descriptive Statistics

table = 'descriptive statistics'
vars = ['wi', 'ni', 'gp', 'sa', 'pids', 'psid',
        'pid', 'chc', 'conlib_std', 'ideo_std',
        'mc_perc_corr', 'chk2_passed'] + ADJ_VARS
vars_labels = {v:l for v, l in VARS.items() if v in vars}
# vars_labels = VARS
tab = (
    df
    .distinct('rid')
    .select(vars_labels.keys())
    .descriptive_statistics(vars_labels)
)
tab
tab.print()
# 
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    escape=True,
                    digits=2,
                    align = "l"+'c'*9)
print(tabl)
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)



# ** DONE Table H2: Balance

table = 'balance'

digits=4
tab = (res_bal
       .replace({'index':VARS})
       .rename({
           'index':"Pre-treatment covariate",
           'status_threat':'Exposure',
           'P>|t|':"$P>\\mid t \\mid$"
       })
       .mutate(stars=tp.map(["$P>\\mid t \\mid$"], lambda pvalue: t4.stats.sig_marks(pvalue)[0]))
       .mutate(**{'Coef.': tp.col("Coef.").round(digits).cast(str) + tp.col("stars")})
       .drop('stars')
       )
tab
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
pvalues = t4.stats.sig_marks(output='marks')
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = None,
                    footnotes = {'r':pvalues})
print(tabl)
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)

    
# ** DONE Table H3: Status threat sample

table = 'status threat sample'
# 
var = {'status_threat':'Exposure'}
tab = (df
       .distinct('rid')
       .freq(var)
       .drop(tp.matches("Std|lo|hi"))
       )
tab
# 
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = None,
                    footnotes = None)
print(tabl)
# 
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)




# ** DONE Table H4: Conjoint sample

df = tp.from_polars(df.to_polars())
table = 'conjoint sample'
# 
var = {'pty_pair' : 'Conjoint pair'}
tab = (df
       .distinct('rid')
       .freq(var)
       .drop(tp.matches("Std|lo|hi"))
       )
tab
# 
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = 'lcc',
                    footnotes = None)
print(tabl)
# 
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)




# ** DONE Table H5: Conjoint sample (by partisan pair)

df = tp.from_polars(df.to_polars())
table = 'conjoint sample by pair'
# 
var = {'pty_pair_group' : 'Conjoint pair'}
tab = (df
       .distinct('rid')
       .freq(var)
       .drop(tp.matches("Std|lo|hi"))
       )
tab
# 
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = 'lcc',
                    footnotes = None)
print(tabl)
# 
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)




# ** DONE Table I1-I4: from Figure 2


res
model = 'LPM'
tables = { 'LPM IxI': 'IxI',
           "LPM DxR": "DxR",
           'LPM RxR': "RxR",
           'LPM DxD': "DxD"}
for table, pair in tables.items():
    tab = (res
           .filter(tp.col("pid")!='Pooled')
           .filter(tp.col("model")==model)
           .filter(tp.col('pty_pair')==pair)
           # .filter(tp.col('adj')==adj)
           .select('adj', 'pid', 'fit')
           .mutate(label = tp.col("pid") + "\n (" + tp.col("adj")+")")
           )
    mods = {label:fit for label, fit in zip(tab.pull("label"),
                                            tab.pull("fit"))}

    # latex table 
    # -----------
    caption = TABLES[table]['caption']
    label = TABLES[table]['fn']
    tab, tabl = t4.report.models2tab(mods,
                           latex=True,
                           covar_labels=VARS | {'_std':" (std)"},
                           kws_latex={'caption': caption,
                                      'label': label,
                                      'header':None,
                                      'align':'p{8cm}'+"x{3cm}"*4,
                                      'escape':True,
                                      'longtable':True,
                                      'rotate':True
                                      },
                           sanitize='partial'
                           )
    if SAVE:
        fn = TABLES[table]['path'] / TABLES[table]['fn']
        save_table(fn, tab, tabl)



# ** DONE Table I5: from Figure 3


model = 'LPM'
tables = {"LPM DxR pty-issue interaction": "DxR",}
for table, pair in tables.items():
    tab = (res_pty_int
           .filter(tp.col("pid")!='Pooled')
           .filter(tp.col("model")==model)
           .filter(tp.col('pty_pair')==pair)
           # .filter(tp.col('adj')==adj)
           .select('adj', 'pid', 'fit')
           .mutate(label = tp.col("pid") + "\n (" + tp.col("adj")+")")
           )
    mods = {label:fit for label, fit in zip(tab.pull("label"),
                                            tab.pull("fit"))}

    # latex table 
    # -----------
    caption = TABLES[table]['caption']
    label = TABLES[table]['fn']
    tab, tabl = t4.report.models2tab(mods,
                           latex=True,
                           covar_labels=VARS | {'_std':" (std)"},
                           kws_latex={'caption': caption,
                                      'label': label,
                                      'header':None,
                                      'align':'p{8cm}'+"x{3cm}"*4,
                                      'escape':True,
                                      'longtable':True,
                                      'rotate':True
                                      },
                           sanitize='partial'
                           )
    if SAVE:
        fn = TABLES[table]['path'] / TABLES[table]['fn']
        save_table(fn, tab, tabl)



# ** DONE FMC (report)


tab = df.distinct('rid')
# tab.freq('mc_group').print()
n = tab.nrow
all_correct_n = tab.freq('mc_group').filter(tp.col("mc_group")=='All correct').pull("N")[0]
all_correct_p = tab.freq('mc_group').filter(tp.col("mc_group")=='All correct').pull("Freq")[0]
none_incorrect_n = tab.freq('mc_group').filter(tp.col("mc_group").str.contains('^Corr.*')).pull("N").sum()
none_incorrect_p = tab.freq('mc_group').filter(tp.col("mc_group").str.contains('^Corr.*')).pull("Freq").sum()
positive_score =  tab.filter(tp.col("mc_score")>0).nrow
# 
print(f"""
Manipulation checks:
All correct: {all_correct_n} cases or {all_correct_p:.0f}%
None incorrect: {none_incorrect_n} cases or {none_incorrect_p:.0f}%
Positive score: {positive_score} cases or {100*positive_score/n:.2f}%)
""")

# ** DONE Table J1: FMC groups

table = 'mc group'
tab = (df
       .distinct('rid')
       .freq('mc_group')
       .select('mc_group', "N", 'Freq')
       .rename(VARS)
       )
tab.print()
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = 'lcc',
                    digits=2,
                    footnotes = None)
print(tabl)
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)


# ** DONE Table J2: FMC scores

table = 'mc score'
# 
tab = (df
       .distinct('rid')
       .freq('mc_score')
       .select('mc_score', "N", 'Freq')
       .rename(VARS)
       )
tab.print()
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = 'ccc',
                    escape=True,
                    digits=2,
                    footnotes = None)
print(tabl)
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)
    
# ** DONE Table J3: FMC (break down)

table = 'mc break down'
# 
tab = (df
       .distinct('rid')
       .filter(tp.col("mc_group").str.contains('^Incorrect.*1.*correct 2 of 2'))
       # .freq('mc_group', 'status_threat', 'pid')
       .freq(['mc', 'mc_group', 'status_threat'])
       .arrange('status_threat', "N")
       .drop('Std.Dev.', 'low', 'high')
       .rename({'mc':'Answer',
                'status_threat':'Exposure'})
       )
tab.print()
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = 'llcr',
                    group_rows_by = 'mc_group',
                    footnotes = None)
print(tabl)

if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)



# ** DONE Table J4: Effect on social status perception (ssp)

table = 'mc: social stauts perception'
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tab, tabl = models2tab(res_mc_ssp,
                       sanitize_option='full',
                       kws_latex={'caption': caption,
                                  'label': label,
                                  'header':None,
                                  'align':'p{3cm}'+'x{2cm}'*len(res_mc_ssp),
                                  })
tab
# tab.print()
print(tabl)

# 
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)

# ** DONE Table J5: Effect on social status axiety (SA)

table = 'mc: social stauts anxiety'
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tab, tabl = models2tab(res_mc_sa,
                       sanitize_option='full',
                       kws_latex={'caption': caption,
                                  'label': label,
                                  'header':None,
                                  'align':'l'+'x{2cm}'*4,
                                  })
tab
# tab.print()
# print(tabl)
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)

    

# ** DONE Table J6: Effect on social prejudice (GP)

table = 'mc: prejudice'
# latex table 
# -----------
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tab, tabl = models2tab(res_mc_gp,
                       sanitize_option='full',
                       kws_latex={'caption': caption,
                                  'label': label,
                                  'header':None,
                                  'rotate':True,
                                  'align':'l'+'x{2.5cm}'*9,
                                  })
tab
# tab.print()
# print(tabl)
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)

# ** DONE Table L1: Aggregated across issues

table = 'Aggregated by position (IxI and DxR)'
# 
digits=4
res_agg
adj = 'Not adjusted'
model = 'LPM'
exposure = ['Status reassuring (Ref.)',
            'Status reassuring',
            'Racial threat',
            'Nationality threat',
            'Racial and nationality threat'
            ]
tab = (res_agg
       .filter(tp.col("model")==model)
       .filter(tp.col('adj')==adj)
       .filter(tp.col("pty_pair").is_in(['IxI', 'DxR']))
       .select('pid', 'summ', 'pty_pair')
       .unnest('summ')
       .mutate(term = tp.str_replace_all('term', 'position\\[T.|]', ''))
       .mutate(term = tp.str_replace_all('term', 'c_party_affiliation\\[T.', ''))
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.', ''))
       .mutate(term=  tp.str_replace_all('term', 'cons', 'Cons'))
       .mutate(term = tp.case_when(tp.col("term").str.contains('^Conservative$'), 'Conservative:Status reassuring',
                                   ~tp.col("term").str.contains('^Conservative'), "Liberal:"+tp.col("term"),
                                   True, tp.col("term")
                                   ))
       .replace({'term': {"Liberal:Intercept":
                          'Liberal:Status reassuring (Ref.)'}})
       .separate('term', into=['Candidate', 'Exposure', 'Party'], sep=':')
       .mutate(stars = tp.map(["P>|z|"], lambda pvalue: t4.stats.sig_marks(pvalue)[0]) ,
               Effect = (tp.col("Coef.").round(digits).cast(str) + 
                         tp.col("stars") +
                         " ("+ tp.col("Std.Err.").round(digits).cast(str)+")")
               )
       .rename({'pty_pair':"Pair"})
       .select('Pair', 'pid', 'Candidate', 'Exposure', 'Party', 'Effect')
       .pivot_wider(names_from='pid', values_from='Effect')
       .mutate(Party = tp.case_when(
           tp.col("Pair")=='IxI', 'Independent',
           (tp.col("Pair")=='DxR') & (tp.col("Exposure")=="Republican Party"), 'Rep',
           (tp.col("Pair")=='DxR') & (tp.col("Party").is_null()), 'Dem',
           True, tp.col("Party")
       ),)
       .replace({'Exposure': {"Republican Party":
                              'Status reassuring'},
                 "Party": {'Independent':"Ind",
                           'Democratic Party':'Dem',
                           'Republican Party':'Rep',
                           },
                'Pair':{"IxI": "Non-partisan candidates pair (Independent x Independent)",
                        "DxR": "Partisan candidates pair (Democratic x Republican)",
                        # "RxD": "Partisan candidates pair (Democratic x Republican)",
                        "DxD": "Partisan candidates pair (Democratic x Democratic)",
                        "RxR": "Partisan candidates pair (Republican x Republican)",
                        }
                 })
       .mutate(Exposure = tp.as_factor('Exposure', exposure),
               Candidate = tp.as_factor('Candidate', ['Liberal', 'Conservative'])
               )

       .rename({"Candidate":'Position'})
       .select('Pair', 'Position', 'Party', 'Exposure', tp.contains("voter"))
       .arrange(tp.desc('Pair'), 'Exposure', 'Position')
       )
tab
tab.print()
# 
# latex table 
# -----------
header = [('Candidate'     , 'Position')        ,
          ('Candidate'     , 'Party')           ,
          (''              , 'Exposure')        ,
          ('Causal Effects', 'Republican voter'),
          ('Causal Effects', 'Democratic voter'),
          ]
pvalues = t4.stats.sig_marks(output='marks')
caption = TABLES[table]['caption']
label = TABLES[table]['fn']
tabl = tab.to_latex(header = header,
                    caption = caption,
                    label = label,
                    align = 'lllcc',
                    group_rows_by='Pair',
                    # rotate=True,
                    # longtable=True,
                    footnotes={'r': pvalues})
# print(tabl)
# 
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)




# ** DONE Table L2: Dem-Rep voter effect differences 

table = 'testing h5'
# 
pair = 'DxR'
pair = 'RxR'
pair = 'DxD'
pair = 'IxI'
threat = 'Racial threat'
round = 4
tab = (res_diff
       .filter(tp.col("pty_pair")==pair)
       # .filter(tp.col("term").str.contains(threat))
       .mutate(stars_diff=tp.map(['p-value'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               stars_dem=tp.map(['p_dem'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               stars_rep=tp.map(['p_rep'], lambda pvalue: t4.stats.sig_marks(pvalue)[0])
               )
       .mutate(diff = tp.col("diff").round(round).cast(str) + tp.col("stars_diff"),
               b_dem = tp.col("b_dem").round(round).cast(str) +
               tp.col("stars_dem") + 
               " ("+tp.col("s_dem").round(round).cast(str)+")",
               b_rep = tp.col("b_rep").round(round).cast(str) +
               tp.col("stars_rep") + 
               " ("+tp.col("s_rep").round(round).cast(str)+")"
               )
       .mutate(term = tp.str_replace_all('term', '\\[.*:', ' x '),)
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.|]', ''),)
       .separate('term', into=['issue', 'threat'], sep=" x ")
       .replace({'issue':VARS})
       .drop_null()
       .select( 'issue', 'threat', tp.matches("b_"), 'diff')
       .arrange('issue', 'threat')
       .rename({'issue':"Issue",
                'threat': 'Exposure',
                "b_rep":'Republican voter',
                'b_dem':'Democratic voter',
                'diff' : "Difference"
                })
       )
tab.print()
# tab.print()
# 
# latex table 
# -----------
caption = TABLES[table]['caption'].replace('CANDIDATE PAIR', pair)
label = TABLES[table]['fn']
pvalues  =t4.stats.sig_marks(output='marks')
tabl = tab.to_latex(caption = caption,
                    label = label,
                    align = 'llccc',
                    footnotes = {'r':pvalues})
print(tabl)
# 
if SAVE:
    fn = TABLES[table]['path'] / TABLES[table]['fn']
    save_table(fn, tab, tabl)


# * Figures
# ** DONE Figure H1: Balance

figure = 'balance'
set_theme('sci', borders=True)
# 
tab = (res_bal
       .replace({'index':VARS | {'Intercept':' Intercept'}})
       .rename({'[0.025':'lo',
                '0.975]':'hi'})
       )
tab
# 
x         = 'Coef\\.'
y         = 'index'
fill      = 'status_threat'
color     = fill
linetype  = None
size      = None
opacity   = None
facet1    = None
facet2    = None
# 
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = 'Effect on treatment exposure'
ylab      = 'Pre-treatment covariates'
dodge     = 0.6
# 
base = (alt.Chart(tab.to_pandas()))
pts = (base.mark_point()
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           fill    = alt.Fill(fill).title(None),
           yOffset= alt.YOffset(fill),
           # color   = alt.value('white'),
           size    = alt.value(30),
           # opacity = alt.Opacity(opacity)
       ))
eb = (base.mark_errorbar(thickness=1)
      .encode(
          x       = alt.X('lo', title=xlab),
          x2      = alt.X2('hi'),
          y       = alt.Y(y, title=ylab),
          color   = alt.Color(color).legend(None),
          yOffset = alt.YOffset(fill),
      ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=1.2, color='black')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts)
     .properties(width=250, height=180)
     .configure_axis(
         labelFontSize=7,   # Tick labels
         titleFontSize=8   # Axis titles
     ).configure_legend(
         labelFontSize=7,   # Legend labels
         titleFontSize=8   # Legend title
     ).configure_title(
         fontSize=8        # Chart title
     )
     )
show_figure(g)
if SAVE:
    fn = FIGURES[figure]['path'] / FIGURES[figure]['fn']
    save_figure(fn, g, tab)
    print(f"#+NAME: {FIGURES[figure]['fn']}")
    print(f"#+CAPTION: {FIGURES[figure]['caption']}")

    
# ** DONE Figure K1: subset by MC (non-partisan)

figure = 'non-partisan marginal effects (all correct mc)'
set_theme('sci', borders=True)
# 
model = 'LPM'
adj = 'Not adjusted'
pair = 'DxR'
pair = 'IxI'
short_names = {'Intercept': '  Intercept (only liberal positions)',
               'Nationality threat': ' Nat. Threat',
               'Racial threat': '  Rac. Threat',
               'Racial and nationality threat': ' R&N Threat',
               }
tab = (res_mc_all_correct
       .filter(tp.col("model")==model)
       .filter(tp.col('pty_pair')==pair)
       .filter(tp.col('adj')==adj)
       .select('pid', 'summ', 'nobs')
       .unnest('summ')
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.|\\]', ''),)
       .separate('term', ['issue', 'threat'], sep=':')
       .mutate(threat = tp.case_when(tp.col("threat").is_null(), '',
                                     True , tp.col("threat")),
               condition = tp.case_when((tp.col("issue").str.contains('^c_|Interc')) &
                                        (tp.col("threat")==''), 'Status reassuring',
                                        True, 'Status threat'),)
       .replace({'issue':VARS})
       .replace({'issue': short_names, 'threat':short_names})
       .rename({'[0.025':'lo', '0.975]':"hi"})
       .rename({'Coef.':'estimate'})

       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               #pvalue = tp.case_when(tp.col('P>|z|')<=0.05, '*', True,  ' '),
               issue = tp.case_when(tp.col("threat")!='', tp.col("issue") + " x " + tp.col("threat"),
                                    True, tp.col("issue")),
               pid = tp.as_factor('pid', ['Pooled', 'Democratic voter', 'Republican voter'])
               )
       )
tab
nobs = "; ".join( tab.select('pid', 'nobs').distinct()
                  .mutate(nobs=tp.col("pid")+": "+tp.col("nobs").cast(str))
                  .pull('nobs').to_list())
# 
x         = 'estimate'
y         = 'issue'
fill      = 'condition:N'
color     = fill
linetype  = None
shape     = 'condition:N'
size      = None
opacity   = None
facet1    = 'pid'
facet2    = None
# 
leg_title = 'Social Status Exposure Condition'
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Marginal Causal Effect of Candidate's Conservative Policy Position on Candidate Support"
ylab      = ['Conservative policy position',
             '(Non-partisan candidates)']
dodge     = 0.6
shapes = ['circle', 'triangle', 'triangle-down', 'circle']
colors = ['gray',  'white']
bold = " | ".join([f"datum.value == '{VARS[issue]}'" for issue in ISSUES])
# 
set_theme('sci', borders=True)
base = (alt.Chart(tab.to_polars())
        .encode(
            # color   = alt.Color(color),
        ))
pts = (base.mark_point()
       .encode(
           x       = alt.X(x, title=None),
           y         = (alt.Y(y, title=ylab).scale(padding=dodge)
                        .axis(labelFontWeight=alt.condition(bold, alt.value(800), alt.value(300)))
                        ),
           size    = alt.value(40),
           color   = alt.value('black'),
           fill    = alt.Fill(fill).title(leg_title),
           # fill    = alt.value('black'),
           shape   = alt.Shape(shape).title(leg_title).scale(range=shapes),
           # # opacity = alt.Opacity(opacity)
           # yOffset = alt.YOffset(fill),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x         = alt.X('lo', title=xlab),
          x2        = alt.X2('hi'),
          y         = alt.Y(y, title=ylab),
          # color   = alt.Color(color).legend(None),
          # yOffset = alt.YOffset(fill),
      ))
txt = (base.mark_text(dy=-2, size=15)
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           text     =  alt.Text("pvalue"),
           yOffset = alt.YOffset(fill),
       ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=.7, color='black')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts, txt)
     .properties(width=150, height=250)
     .facet(facet=alt.Facet(facet1).header(title=xlab, titleOrient='bottom',
                                           titleAnchor='middle',
                                           titleAlign='center'),
            columns=4)
     # .configure_legend(columns=4)
     # .resolve_scale(x='shared')
     # .resolve_scale(x='independent',
     #                #y='independent'
     #                )
     .configure_range(category=colors)
     )
show_figure(g)
# 
if SAVE:
    caption = FIGURES[figure]['caption']
    label = FIGURES[figure]['fn']
    fn = FIGURES[figure]['path'] / label
    save_figure(fn, g, tab, caption=caption, label=label)




# ** DONE Figure K2: subset by MC (partisan)

set_theme('sci', borders=True)
figure = 'partisan marginal effects (all correct mc)'
# 
# 
model = 'LPM'
adj = 'Not adjusted'
pair = ['DxR', 'DxD', 'RxR']
short_names = {'Intercept': '  Intercept (liberal positions)',
               'Nationality threat': ' Nat. Threat',
               'Racial threat': '  Rac. Threat',
               'Racial and nationality threat': ' R&N Threat',
               }
tab = (res_mc_all_correct
       .filter(tp.col("model")==model)
       .filter(tp.col("pid")!='Pooled')
       .filter(tp.col('pty_pair').is_in(pair))
       .filter(tp.col('adj')==adj)
       .select('pid', {'pty_pair':'pair'}, 'summ', 'nobs')
       .unnest('summ')
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.|\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'c_party_affiliation\\[T.|]', ' '),)
       .separate('term', ['issue', 'threat'], sep=':')
       .mutate(threat = tp.case_when(tp.col("threat").is_null(), '',
                                     True , tp.col("threat")),
               condition = tp.case_when((tp.col("issue").str.contains('^c_|Interc|Party$')) &
                                        (tp.col("threat")==''), 'Status reassuring',
                                        True, 'Status threat'),
               pair = tp.case_when(tp.col("pair")=='DxR', 'DxR (Ref.: Democratic Party)',
                                   True, tp.col("pair")),
               )
       .replace({'issue':VARS})
       .replace({'issue': short_names, 'threat':short_names})
       .rename({'[0.025':'lo', '0.975]':"hi"})
       .rename({'Coef.':'estimate'})

       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               #pvalue = tp.case_when(tp.col('P>|z|')<=0.05, '*', True,  ' '),
               issue = tp.case_when(tp.col("threat")!='', tp.col("issue") + " x " + tp.col("threat"),
                                    True, tp.col("issue")),
               pid = tp.as_factor('pid', ['Pooled', 'Democratic voter', 'Republican voter'])
               )
       )
tab
# 
nobs = "; ".join( tab.select('pid', 'nobs').distinct()
                  .mutate(nobs=tp.col("pid")+": "+tp.col("nobs").cast(str))
                  .pull('nobs').to_list())
# 
x         = 'estimate'
y         = 'issue'
fill      = 'condition:N'
color     = fill
linetype  = None
shape     = 'condition:N'
size      = None
opacity   = None
facet1    = 'pair'
facet2    = 'pid'
# 
leg_title = 'Social Status Exposure Condition'
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = ["Marginal Causal Effect of Candidate's Conservative Policy Position",
             "or Party Affiliationon Candidate Support"]
ylab      = ['Conservative Policy Position or Party Affiliation',
             '(Partisan candidates)']
dodge     = 0.6
shapes = ['circle', 'triangle', 'triangle-down', 'circle']
colors = ['gray',  'white']
bold = " | ".join([f"datum.value == '{VARS[issue]}'" for issue in ISSUES])
bold += " | datum.value == ' Republican Party'"
bold
tab.pull('issue').to_list()
# 
set_theme('sci', borders=True)
base = (alt.Chart(tab.to_polars())
        .encode(
            # color   = alt.Color(color),
        ))
pts = (base.mark_point()
       .encode(
           x       = alt.X(x, title=None),
           y         = (alt.Y(y, title=ylab).scale(padding=dodge)
                        .axis(labelFontWeight=alt.condition(bold, alt.value(800), alt.value(300)))
                        ),
           size    = alt.value(40),
           color   = alt.value('black'),
           fill    = alt.Fill(fill).title(leg_title),
           # fill    = alt.value('black'),
           shape   = alt.Shape(shape).title(leg_title).scale(range=shapes),
           # # opacity = alt.Opacity(opacity)
           # yOffset = alt.YOffset(fill),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x         = alt.X('lo', title=xlab),
          x2        = alt.X2('hi'),
          y         = alt.Y(y, title=ylab),
          # color   = alt.Color(color).legend(None),
          # yOffset = alt.YOffset(fill),
      ))
txt = (base.mark_text(dy=-2, size=15)
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           text     =  alt.Text("pvalue"),
           yOffset = alt.YOffset(fill),
       ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=.7, color='black')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts, txt)
     .properties(width=150, height=250)
     .facet(row=alt.Facet(facet2).header(title=xlab, titleOrient='bottom',
                                           titleAnchor='middle',
                                           titleAlign='center'),
            column=alt.Column(facet1),
            columns=4)
     # .configure_legend(columns=4)
     # .resolve_scale(x='shared')
     # .resolve_scale(x='independent',
     #                #y='independent'
     #                )
     .configure_range(category=colors)
     )
show_figure(g)
# 
if SAVE:
    caption = FIGURES[figure]['caption']
    label = FIGURES[figure]['fn']
    fn = FIGURES[figure]['path'] / label
    save_figure(fn, g, tab, caption=caption, label=label)




# ** DONE Figure K3: subset by speeders

set_theme('sci', borders=True)
figure = 'speeders'
# 
short_names = {'Intercept': '  Intercept (liberal positions)',
               'Nationality threat': ' Nat. Threat',
               'Racial threat': '  Rac. Threat',
               'Racial and nationality threat': ' R&N Threat',
               }
tab = (res_speeders
       # .filter(tp.col("model")==model)
       # .filter(tp.col("pid")!='Pooled')
       # .filter(tp.col('pty_pair').is_in(pair))
       # .filter(tp.col('adj')==adj)
       .select('pid', 'speeder_min', {'pty_pair':'pair'}, 'summ', 'nobs')
       .unnest('summ')
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'status_threat\\[T.|\\]', ''),)
       .mutate(term = tp.str_replace_all('term', 'c_party_affiliation\\[T.|]', ' '),)
       .separate('term', ['issue', 'threat'], sep=':')
       .mutate(threat = tp.case_when(tp.col("threat").is_null(), '',
                                     True , tp.col("threat")),
               condition = tp.case_when((tp.col("issue").str.contains('^c_|Interc|Party$')) &
                                        (tp.col("threat")==''), 'Status reassuring',
                                        True, 'Status threat'),
               pair = tp.case_when(tp.col("pair")=='DxR', 'DxR (Ref.: Democratic Party)',
                                   True, tp.col("pair")),
               )
       .replace({'issue':VARS})
       .replace({'issue': short_names, 'threat':short_names})
       .rename({'[0.025':'lo', '0.975]':"hi"})
       .rename({'Coef.':'estimate'})

       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]),
               #pvalue = tp.case_when(tp.col('P>|z|')<=0.05, '*', True,  ' '),
               issue = tp.case_when(tp.col("threat")!='', tp.col("issue") + " x " + tp.col("threat"),
                                    True, tp.col("issue")),
               pid = tp.as_factor('pid', ['Pooled', 'Democratic voter', 'Republican voter'])
               )
       )
tab
# 
nobs = "; ".join( tab.select('pid', 'nobs').distinct()
                  .mutate(nobs=tp.col("pid")+": "+tp.col("nobs").cast(str))
                  .pull('nobs').to_list())
# 
x         = 'estimate'
y         = 'issue'
fill      = 'condition:N'
color     = fill
linetype  = None
shape     = 'condition:N'
size      = None
opacity   = None
facet1    = 'pair'
facet2    = 'pid'
# 
leg_title = 'Social Status Exposure Condition'
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = ["Marginal Causal Effect of Candidate's Conservative Policy Position",
             "or Party Affiliationon Candidate Support"]
ylab      = ['Conservative Policy Position or Party Affiliation',
             '(Partisan candidates)']
dodge     = 0.6
shapes = ['circle', 'triangle', 'triangle-down', 'circle']
colors = ['gray',  'white']
bold = " | ".join([f"datum.value == '{VARS[issue]}'" for issue in ISSUES])
bold += " | datum.value == ' Republican Party'"
bold
tab.pull('issue').to_list()
# 
set_theme('sci', borders=True)
base = (alt.Chart(tab.to_polars())
        .encode(
            # color   = alt.Color(color),
        ))
pts = (base.mark_point()
       .encode(
           x       = alt.X(x, title=None),
           y         = (alt.Y(y, title=ylab).scale(padding=dodge)
                        .axis(labelFontWeight=alt.condition(bold, alt.value(800), alt.value(300)))
                        ),
           size    = alt.value(40),
           color   = alt.value('black'),
           fill    = alt.Fill(fill).title(leg_title),
           # fill    = alt.value('black'),
           shape   = alt.Shape(shape).title(leg_title).scale(range=shapes),
           # # opacity = alt.Opacity(opacity)
           # yOffset = alt.YOffset(fill),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x         = alt.X('lo', title=xlab),
          x2        = alt.X2('hi'),
          y         = alt.Y(y, title=ylab),
          # color   = alt.Color(color).legend(None),
          # yOffset = alt.YOffset(fill),
      ))
txt = (base.mark_text(dy=-2, size=15)
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           text     =  alt.Text("pvalue"),
           yOffset = alt.YOffset(fill),
       ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=.7, color='black')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts, txt)
     .properties(width=150, height=250)
     .facet(row=alt.Facet(facet2).header(title=xlab, titleOrient='bottom',
                                           titleAnchor='middle',
                                           titleAlign='center'),
            column=alt.Column(facet1),
            columns=4)
     # .configure_legend(columns=4)
     # .resolve_scale(x='shared')
     # .resolve_scale(x='independent',
     #                #y='independent'
     #                )
     .configure_range(category=colors)
     )
show_figure(g)
# 
if SAVE:
    caption = FIGURES[figure]['caption']
    label = FIGURES[figure]['fn']
    fn = FIGURES[figure]['path'] / label
    save_figure(fn, g, tab, caption=caption, label=label)


# ** DONE Figure M1: task order effects (non-partisan)

figure = 'task order effect (non-partisan)'
# 
model = 'LPM'
adj = 'Not adjusted'
pair = 'IxI'
tab = (res_order_effect
       .filter(tp.col("model")==model)
       .filter(tp.col("adj")==adj)
       .filter(tp.col("pty_pair")==pair)
       .select('pid', 'summ')
       .unnest('summ')
       .filter(tp.col("term").str.contains('task'))
       .rename({'[0.025':'lo', '0.975]':"hi", 'Coef.':'estimate'})
       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]))
       .replace({"term":VARS}, regex=True)
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''))
       .mutate(term = tp.str_replace_all('term', 'Status threat exposure\\[T\\.|]', ''))
       .mutate(term = tp.str_replace_all('term', ':Task', ''))
       .mutate(term = tp.str_replace_all('term', 'Task', ' Task'))
       .mutate(term = tp.str_replace_all('term', ':', ' x '))
       )
tab
# 
x         = 'estimate'
y         = 'term'
fill      = None
color     = fill
linetype  = None
shape     = None
size      = None
opacity   = None
facet1    = 'pid'
facet2    = None
# 
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Effect of taks"
ylab      = ['Interaction between task order, ', 'conservative position and exposure']
dodge     = 0.6
# 
base = (alt.Chart(tab.to_polars()))
pts = (base.mark_point()
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           fill    = alt.value('black'),
           color    = alt.value('white'),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x       = alt.X('lo', title=xlab),
          x2      = alt.X2('hi'),
          y       = alt.Y(y, title=ylab),
      ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=1.2, color='red')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts)
     .properties(width=180, height=250)
     .facet(facet=alt.Facet(facet1), columns=3)
     )
show_figure(g)
if SAVE:
    label = FIGURES[figure]['fn']
    caption = FIGURES[figure]['caption']
    fn = FIGURES[figure]['path'] / FIGURES[figure]['fn']
    save_figure(fn, g, tab, caption=caption, label=label)
    # print(f"#+NAME: {FIGURES[figure]['fn']}")
    # print(f"#+CAPTION: {FIGURES[figure]['caption']}")


# ** DONE Figure M2: task order effects (partisan)

figure = 'task order effect (partisan)'
# 
model = 'LPM'
adj = 'Not adjusted'
pair = 'IxI'
short_names = {'Intercept': '  Intercept (liberal positions)',
               'Nationality threat': ' Nat. Threat',
               'Racial threat': '  Rac. Threat',
               'Racial and nationality threat': ' R&N Threat',
               }
tab = (res_order_effect
       .filter(tp.col("pid")!='Pooled')
       .filter(tp.col("model")==model)
       .filter(tp.col("adj")==adj)
       .filter(tp.col("pty_pair")!=pair)
       .select('pid', {'pty_pair':'pair'}, 'summ')
       .unnest('summ')
       .filter(tp.col("term").str.contains('task'))
       .rename({'[0.025':'lo', '0.975]':"hi", 'Coef.':'estimate'})
       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]))
       .replace({"term":VARS}, regex=True)
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''))
       .mutate(term = tp.str_replace_all('term', 'Status threat exposure\\[T\\.|]', ''))
       .mutate(term = tp.str_replace_all('term', ':Task', ''))
       .mutate(term = tp.str_replace_all('term', 'Task', ' Task'))
       .mutate(term = tp.str_replace_all('term', ':', ' x '))
       .replace({'term':short_names})
       )
tab
# 
x         = 'estimate'
y         = 'term'
fill      = None
color     = fill
linetype  = None
shape     = None
size      = None
opacity   = None
facet1    = 'pid'
facet2    = 'pair'
# 
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Effect of taks"
ylab      = ['Interaction between task order, ', 'conservative position and exposure']
dodge     = 0.6
# 
base = (alt.Chart(tab.to_polars()))
pts = (base.mark_point()
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           fill    = alt.value('black'),
           color    = alt.value('white'),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x       = alt.X('lo', title=xlab),
          x2      = alt.X2('hi'),
          y       = alt.Y(y, title=ylab),
      ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=1.2, color='red')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts)
     .properties(width=180, height=250)
     .facet(row=alt.Row(facet1),
            column=alt.Column(facet2) # must come before the title
            )
     )
show_figure(g)
if SAVE:
    label = FIGURES[figure]['fn']
    caption = FIGURES[figure]['caption']
    fn = FIGURES[figure]['path'] / FIGURES[figure]['fn']
    save_figure(fn, g, tab, caption=caption, label=label)
    # print(f"#+NAME: {FIGURES[figure]['fn']}")
    # print(f"#+CAPTION: {FIGURES[figure]['caption']}")


# ** DONE Figure M3: profile order effects (non-partisan)

figure = 'profile order effect (non-partisan)'
# 
model = 'LPM'
adj = 'Not adjusted'
pair = 'IxI'
tab = (res_cand_order_effect
       .filter(tp.col("model")==model)
       .filter(tp.col("adj")==adj)
       .filter(tp.col("pty_pair")==pair)
       .select('pid', 'summ')
       .unnest('summ')
       .filter(tp.col("term").str.contains('cand'))
       .rename({'[0.025':'lo', '0.975]':"hi", 'Coef.':'estimate'})
       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]))
       .replace({"term":VARS}, regex=True)
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''))
       .mutate(term = tp.str_replace_all('term', 'Status threat exposure\\[T\\.|]', ''))
       # .mutate(term = tp.str_replace_all('term', ':Task', ''))
       .mutate(term = tp.str_replace_all('term', 'Candidate\\[T.', ' Profile '))
       .mutate(term = tp.str_replace_all('term', ':', ' x '))
       )
tab
# 
x         = 'estimate'
y         = 'term'
fill      = None
color     = fill
linetype  = None
shape     = None
size      = None
opacity   = None
facet1    = 'pid'
facet2    = None
# 
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Effect of taks"
ylab      = ['Interaction between task order, ', 'conservative position and exposure']
dodge     = 0.6
# 
base = (alt.Chart(tab.to_polars()))
pts = (base.mark_point()
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           fill    = alt.value('black'),
           color    = alt.value('white'),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x       = alt.X('lo', title=xlab),
          x2      = alt.X2('hi'),
          y       = alt.Y(y, title=ylab),
      ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=1.2, color='red')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts)
     .properties(width=180, height=250)
     .facet(facet=alt.Facet(facet1), columns=3)
     )
show_figure(g)
# 
if SAVE:
    label = FIGURES[figure]['fn']
    caption = FIGURES[figure]['caption']
    fn = FIGURES[figure]['path'] / FIGURES[figure]['fn']
    save_figure(fn, g, tab, caption=caption, label=label)


# ** DONE Figure M4: profile order effects (partisan)

figure = 'profile order effect (partisan)'
# 
model = 'LPM'
adj = 'Not adjusted'
pair = 'IxI'
short_names = {'Intercept': '  Intercept (liberal positions)',
               'Nationality threat': ' Nat. Threat',
               'Racial threat': '  Rac. Threat',
               'Racial and nationality threat': ' R&N Threat',
               }
tab = (res_cand_order_effect
       .filter(tp.col("pid")!='Pooled')
       .filter(tp.col("model")==model)
       .filter(tp.col("adj")==adj)
       .filter(tp.col("pty_pair")!=pair)
       .select('pid', {'pty_pair':'pair'}, 'summ')
       .unnest('summ')
       .filter(tp.col("term").str.contains('cand'))
       .rename({'[0.025':'lo', '0.975]':"hi", 'Coef.':'estimate'})
       .mutate(pvalue = tp.map(['P>|z|'], lambda pvalue: t4.stats.sig_marks(pvalue)[0]))
       .replace({"term":VARS}, regex=True)
       .mutate(term = tp.str_replace_all('term', '\\[T.conservative\\]', ''))
       .mutate(term = tp.str_replace_all('term', 'Status threat exposure\\[T\\.|]', ''))
       .mutate(term = tp.str_replace_all('term', 'Candidate\\[T.', ' Profile '))
       .mutate(term = tp.str_replace_all('term', ':', ' x '))
       .replace({'term':short_names})
       )
tab
# 
x         = 'estimate'
y         = 'term'
fill      = None
color     = fill
linetype  = None
shape     = None
size      = None
opacity   = None
facet1    = 'pid'
facet2    = 'pair'
# 
leg_title = None
title     = None
subtitle  = None
footnote  = None
xlab      = "Effect of taks"
ylab      = ['Interaction between task order, ', 'conservative position and exposure']
dodge     = 0.6
# 
base = (alt.Chart(tab.to_polars()))
pts = (base.mark_point()
       .encode(
           x         = alt.X(x, title=xlab),
           y         = alt.Y(y, title=ylab).scale(padding=dodge),
           fill    = alt.value('black'),
           color    = alt.value('white'),
       ))
eb = (base.mark_errorbar(thickness=1.2)
      .encode(
          x       = alt.X('lo', title=xlab),
          x2      = alt.X2('hi'),
          y       = alt.Y(y, title=ylab),
      ))
vline = (base.mark_rule(strokeDash=[6, 3], strokeWidth=1.2, color='red')
         .encode(
             x = alt.datum(0)
         ))
# 
g = (alt.layer(vline, eb, pts)
     .properties(width=180, height=250)
     .facet(row=alt.Row(facet1),
            column=alt.Column(facet2) # must come before the title
            )
     )
show_figure(g)
if SAVE:
    label = FIGURES[figure]['fn']
    caption = FIGURES[figure]['caption']
    fn = FIGURES[figure]['path'] / FIGURES[figure]['fn']
    save_figure(fn, g, tab, caption=caption, label=label)
    # print(f"#+NAME: {FIGURES[figure]['fn']}")
    # print(f"#+CAPTION: {FIGURES[figure]['caption']}")

# * done

print_system_info(os.path.basename(__file__))
print(modules_used(iversions=True, watermark=True, globals_=globals()))




