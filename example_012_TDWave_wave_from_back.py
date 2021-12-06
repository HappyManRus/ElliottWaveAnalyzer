#This module trying search "start wave 0-1-2".
#It's can help found Elliott wave in first three waves.

from __future__ import annotations
from models.WavePattern import WavePattern
from models.WaveRules import Impulse, LeadingDiagonal, TDWave
from models.WaveAnalyzer import WaveAnalyzer
from models.WaveOptions import WaveOptionsGenerator3
from models.helpers import plot_pattern
import pandas as pd
import numpy as np

df = pd.read_csv(r'data\btc-usd_1d.csv')
idx_start = np.argmin(np.array(list(df['Low'])))

wa = WaveAnalyzer(df=df, verbose=False)
wave_options_impulse = WaveOptionsGenerator3(up_to=7)  # generates WaveOptions up to [15, 15, 15, 15, 15]

impulse = TDWave('tdwave')
leading_diagonal = LeadingDiagonal('leading diagonal')
rules_to_check = [impulse]

print(f'Start at idx: {idx_start}')
print(f"will run up to {wave_options_impulse.number / 1e6}M combinations.")

wavepatterns_up = set()

# loop from back of data. "From now to past"
for i in range(len(df)-1, 0, -1):
    idx_start = i
    # loop over all combinations of wave options [i,j,k,l,m] for impulsive waves sorted from small, e.g.  [0,1,...] to
    # large e.g. [3,2, ...]
    for new_option_impulse in wave_options_impulse.options_sorted:

        waves_up = wa.find_td_wave(idx_start=idx_start, wave_config=new_option_impulse.values)

        if waves_up:
            wavepattern_up = WavePattern(waves_up, verbose=True)

            for rule in rules_to_check:

                if wavepattern_up.check_rule(rule):
                    if wavepattern_up in wavepatterns_up:
                        continue
                    else:

                        indx_dif_wayv_0_1 = df[(df['Date'] == wavepattern_up.dates[1])].index - df[(df['Date'] == wavepattern_up.dates[0])].index
                        df_check_min_wayv_0_1 = df[(df.index> df[(df['Date'] == wavepattern_up.dates[0])].index[0]-indx_dif_wayv_0_1[0])  & (df.index<df[(df['Date'] == wavepattern_up.dates[1])].index[0]+1)].copy()

                        if min(list(df_check_min_wayv_0_1['Low']))/wavepattern_up.values[0]>0.95:
                            wavepatterns_up.add(wavepattern_up)
                            print(f'{rule.name} found: {new_option_impulse.values}')
                            plot_pattern(df=df, wave_pattern=wavepattern_up, title=str(new_option_impulse))