import os 

#Input directory where the files produced at the pre-selection level are
inputDir= '/eos/home-o/oarakji/tth/myAnalysis/'

#Input directory where the files produced at the pre-selection level are
outputDir  = '/eos/home-o/oarakji/tth/myFinalAnalyses/nc/'

processList = {
    #Signal
    #'mgp8_pp_tth01j_5f_haa':{}, #output file from analysis_stage1.py
    #'mgp8_pp_tth01j_5f_84TeV_haaexcl':{}, #output file from analysis_stage1.py
    # 'mgp8_pp_tth_5f_50TeV':{},
    # 'mgp8_pp_tth_5f_50TeV_backup10k':{},
    'mgp8_pp_tth01j_5f_50TeV' : {},

    #Backgrounds
    #'mgp8_pp_ttaa_semilep_5f_100TeV':{} #output file from analysis_stage1.py
    # 'mgp8_pp_ttyy_5f_50TeV':{},
    'mgp8_pp_ttaa01j_5f_50TeV':{},
    # 'mgp8_pp_vbf_h01j_5f_50TeV':{},
    'mgp8_pp_vh012j_5f_50TeV':{},
    'mgp8_pp_th12j_5f_50TeV':{},
    'mgp8_pp_vbf_h01j_5f_50TeV': {},
    'mgp8_pp_h01j_5f_50TeV' : {},
    'mgp8_pp_thw01j_5f_50TeV' : {},

    # 'mgp8_pp_ttyy_5f_50TeV_backup10k':{},
    #'mgp8_pp_Vaajj_HF_5f_84TeV' : {}, #output file from analysis_stage1.py
    #'mgp8_pp_ttaa01j_5f_84TeV':{}, #output file from analysis_stage1.py
    #'pwp8_pp_hh_lambda100_5f_hhbbaa' : {}, #output file from analysis_stage1.py

}

#Link to the dictionary that contains all the cross section informations etc...
procDict = "/eos/home-o/oarakji/tth/myFCCDict/FCChh_procDict_fcc_v07_II.json"
#Note the numbeOfEvents and sumOfWeights are placeholders that get overwritten with the correct values in the samples

#How to add a process that is not in the official dictionary:
# procDictAdd={"pwp8_pp_hh_5f_hhbbyy": {"numberOfEvents": 4980000, "sumOfWeights": 4980000.0, "crossSection": 0.0029844128399999998, "kfactor": 1.075363, "matchingEfficiency": 1.0}}

# Expected integrated luminosity
intLumi = 30e+06  # pb-1

# Whether to scale to expected integrated luminosity
doScale = True

#Number of CPUs to use
nCPUS = 8

#produces ROOT TTrees, default is False
doTree = True

saveTabular = True

# Optional: Use weighted events
do_weighted = True 

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
            # cutflow
            "all_events":                   "n_photons_nocut >=0",
            "nocuts":                       "n_photons >= 0", # all events
            "photons":                      "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. ", # 2 photons with pT > 25 GeV
            "photons_rel_pt":               "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25",
            "photons_myy_window_wide":      "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 && m_yy[0] > 105. && m_yy[0] <= 160.",
            "photons_myy_window":           "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 && m_yy[0] > 110. && m_yy[0] <= 140.",
            "preselection_wide":            "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 && m_yy[0] > 105. && m_yy[0] <= 160. && n_bjets > 1",
            "preselection":                 "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 && m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1",
            "lep_channel_wide":             "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 && m_yy[0] > 105. && m_yy[0] <= 160. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "lep_channel":                  "n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 && m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # pT(yy) bins
            "pT_yy_bin1": "pT_yy[0] >= 0. && pT_yy[0] < 60.     && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "pT_yy_bin2": "pT_yy[0] >= 60. && pT_yy[0] < 120.   && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "pT_yy_bin3": "pT_yy[0] >= 120. && pT_yy[0] < 200.  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "pT_yy_bin4": "pT_yy[0] >= 200. && pT_yy[0] < 300.  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "pT_yy_bin5": "pT_yy[0] >= 300.                     && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] > 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # truth bins for the signal
            # pT(H) < 60 GeV
            "TTH_CEN_PTH_0_60_pT_yy_bin1"    : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=0 && pT_higgs[0]<60)  && (pT_yy[0] >= 0. && pT_yy[0] < 60.)    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_0_60_pT_yy_bin2"    : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=0 && pT_higgs[0]<60)  && (pT_yy[0] >= 60. && pT_yy[0] < 120.)  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_0_60_pT_yy_bin3"    : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=0 && pT_higgs[0]<60)  && (pT_yy[0] >= 120. && pT_yy[0] < 200.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_0_60_pT_yy_bin4"    : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=0 && pT_higgs[0]<60)  && (pT_yy[0] >= 200. && pT_yy[0] < 300.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_0_60_pT_yy_bin5"    : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=0 && pT_higgs[0]<60)  && (pT_yy[0] >= 300.)                    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # 60 < pT(H) < 120 GeV
            "TTH_CEN_PTH_60_120_pT_yy_bin1"  : "(abs(rapidity_higgs[0])<6.0 &&  pT_higgs[0]>=60 && pT_higgs[0]<120) && (pT_yy[0] >= 0. && pT_yy[0] < 60.)    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_60_120_pT_yy_bin2"  : "(abs(rapidity_higgs[0])<6.0 &&  pT_higgs[0]>=60 && pT_higgs[0]<120) && (pT_yy[0] >= 60. && pT_yy[0] < 120.)  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_60_120_pT_yy_bin3"  : "(abs(rapidity_higgs[0])<6.0 &&  pT_higgs[0]>=60 && pT_higgs[0]<120) && (pT_yy[0] >= 120. && pT_yy[0] < 200.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_60_120_pT_yy_bin4"  : "(abs(rapidity_higgs[0])<6.0 &&  pT_higgs[0]>=60 && pT_higgs[0]<120) && (pT_yy[0] >= 200. && pT_yy[0] < 300.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_60_120_pT_yy_bin5"  : "(abs(rapidity_higgs[0])<6.0 &&  pT_higgs[0]>=60 && pT_higgs[0]<120) && (pT_yy[0] >= 300.)                    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # 120 < pT(H) < 200 GeV
            "TTH_CEN_PTH_120_200_pT_yy_bin1" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=120   && pT_higgs[0]<200) && (pT_yy[0] >= 0. && pT_yy[0] < 60.)    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_120_200_pT_yy_bin2" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=120   && pT_higgs[0]<200) && (pT_yy[0] >= 60. && pT_yy[0] < 120.)  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_120_200_pT_yy_bin3" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=120   && pT_higgs[0]<200) && (pT_yy[0] >= 120. && pT_yy[0] < 200.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_120_200_pT_yy_bin4" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=120   && pT_higgs[0]<200) && (pT_yy[0] >= 200. && pT_yy[0] < 300.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_120_200_pT_yy_bin5" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=120   && pT_higgs[0]<200) && (pT_yy[0] >= 300.)                    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # 200 < pT(H) < 300 GeV
            "TTH_CEN_PTH_200_300_pT_yy_bin1" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=200  && pT_higgs[0]<300) && (pT_yy[0] >= 0. && pT_yy[0] < 60.)    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_200_300_pT_yy_bin2" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=200  && pT_higgs[0]<300) && (pT_yy[0] >= 60. && pT_yy[0] < 120.)  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_200_300_pT_yy_bin3" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=200  && pT_higgs[0]<300) && (pT_yy[0] >= 120. && pT_yy[0] < 200.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_200_300_pT_yy_bin4" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=200  && pT_higgs[0]<300) && (pT_yy[0] >= 200. && pT_yy[0] < 300.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_200_300_pT_yy_bin5" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=200  && pT_higgs[0]<300) && (pT_yy[0] >= 300.)                    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # pT(H) > 300 GeV
            "TTH_CEN_PTH_300_inf_pT_yy_bin1" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=300 ) && (pT_yy[0] >= 0. && pT_yy[0] < 60.)    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_300_inf_pT_yy_bin2" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=300 ) && (pT_yy[0] >= 60. && pT_yy[0] < 120.)  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_300_inf_pT_yy_bin3" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=300 ) && (pT_yy[0] >= 120. && pT_yy[0] < 200.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_300_inf_pT_yy_bin4" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=300 ) && (pT_yy[0] >= 200. && pT_yy[0] < 300.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_CEN_PTH_300_inf_pT_yy_bin5" : "(abs(rapidity_higgs[0])<6.0 && pT_higgs[0]>=300 ) && (pT_yy[0] >= 300.)                    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # Forward Higgs
            "TTH_FWD_pT_yy_bin1" : "(abs(rapidity_higgs[0])>=6.0) && (pT_yy[0] >= 0. && pT_yy[0] < 60.)    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_FWD_pT_yy_bin2" : "(abs(rapidity_higgs[0])>=6.0) && (pT_yy[0] >= 60. && pT_yy[0] < 120.)  && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_FWD_pT_yy_bin3" : "(abs(rapidity_higgs[0])>=6.0) && (pT_yy[0] >= 120. && pT_yy[0] < 200.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_FWD_pT_yy_bin4" : "(abs(rapidity_higgs[0])>=6.0) && (pT_yy[0] >= 200. && pT_yy[0] < 300.) && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            "TTH_FWD_pT_yy_bin5" : "(abs(rapidity_higgs[0])>=6.0) && (pT_yy[0] >= 300.)                    && n_photons > 1 && pT_y1 > 25. && pT_y2 > 25. && rel_pT_y1 > 0.35 && rel_pT_y2 > 0.25 & m_yy[0] >= 110. && m_yy[0] <= 140. && n_bjets > 1 && (n_electrons > 0 || n_muons > 0)",
            # add more cuts here: note you need to && them, they are not sequential!
            }

# Dictionary for the output variable/histograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    # object multiplicity
    "n_photons_nocut":{"name":"n_photons_nocut","title":"Number of photons without cuts","bin":15,"xmin":-0.5,"xmax":14.5},
    "n_photons":{"name":"n_photons","title":"Number of photons","bin":15,"xmin":-0.5,"xmax":14.5},
    "n_bjets":{"name":"n_bjets","title":"Number of b-jets","bin":10,"xmin":-0.5,"xmax":9.5},
    "n_jets":{"name":"n_jets","title":"Number of jets","bin":20,"xmin":-0.5,"xmax":19.5},
    "n_electrons":{"name":"n_electrons","title":"Number of electrons","bin":10,"xmin":-0.5,"xmax":9.5},
    "n_muons":{"name":"n_muons","title":"Number of muons","bin":10,"xmin":-0.5,"xmax":9.5},
    "n_higgs":{"name":"n_higgs","title":"Number of Higgs bosons","bin":5,"xmin":-0.5,"xmax":4.5},
    # final discriminant
    "m_yy":{"name":"m_yy","title":"m_{#gamma#gamma} [GeV]","bin":100,"xmin":0.,"xmax":200., "latex":"$m_{\gamma\gamma}$ [GeV]"},

    # m_yy post cut
    "m_yy_cut":{"name":"m_yy","title":"m_{#gamma#gamma} [GeV]","bin":100,"xmin":105.,"xmax":145., "latex":"$m_{\gamma\gamma}$ [GeV]"},


    # add more variables here
    # photon variables
    "E_y1"  :{"name":"E_y1","title":"Leading photon energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_y1" :{"name":"pT_y1","title":"Leading photon p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400.,"latex":"Leading photon $p_{T}$ [GeV]"},
    "eta_y1":{"name":"eta_y1","title":"Leading photon #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Leading photon $\eta$"},
    "phi_y1":{"name":"phi_y1","title":"Leading photon #phi",  "bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Leading photon $\phi$"},
    "rel_pT_y1":{"name":"rel_pT_y1","title":"Leading photon p_{T} / m_{#gamma#gamma}","bin":50,"xmin":0.,"xmax":3.,"latex":"Leading photon $p_{T}/m_{\gamma\gamma}$"},
    #"iso_y1":{"name":"iso_y1","title":"Leading photon iso variable","bin":50,"xmin":0.,"xmax":0.5,"latex":"Leading photon iso variable"},
    "E_y2"  :{"name":"E_y2","title":"Subleading photon energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_y2" :{"name":"pT_y2","title":"Subleading photon p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400.,"latex":"Subleading photon $p_{T}$ [GeV]"},
    "eta_y2":{"name":"eta_y2","title":"Subleading photon #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Subleading photon $\eta$"},
    "phi_y2":{"name":"phi_y2","title":"Subleading photon #phi","bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Subleading photon $\phi$"},
    "rel_pT_y2":{"name":"rel_pT_y2","title":"Subleading photon p_{T} / m_{#gamma#gamma}","bin":50,"xmin":0.,"xmax":3.,"latex":"Subleading photon $p_{T}/m_{\gamma\gamma}$"},
    #"iso_y2":{"name":"iso_y2","title":"Subleading photon iso variable","bin":50,"xmin":0.,"xmax":0.5,"latex":"Subleading photon iso variable"},


    "pT_yy" :{"name":"pT_yy","title":"p_{T}^{#gamma#gamma} [GeV]","bin":60,"xmin":0.,"xmax":600.,"latex":"$p_{T}^{\gamma\gamma}$ [GeV]"},
    # redefining pT_yy ranges
    "pT_yy_b1" :{"name":"pT_yy","title":"p_{T}^{#gamma#gamma} [GeV]","bin":60,"xmin":0.,"xmax":60.,"latex":"$p_{T}^{\gamma\gamma}$ [GeV]"},
    "pT_yy_b2" :{"name":"pT_yy","title":"p_{T}^{#gamma#gamma} [GeV]","bin":12,"xmin":60.,"xmax":120.,"latex":"$p_{T}^{\gamma\gamma}$ [GeV]"},
    "pT_yy_b3" :{"name":"pT_yy","title":"p_{T}^{#gamma#gamma} [GeV]","bin":12,"xmin":120.,"xmax":200.,"latex":"$p_{T}^{\gamma\gamma}$ [GeV]"},
    "pT_yy_b4" :{"name":"pT_yy","title":"p_{T}^{#gamma#gamma} [GeV]","bin":12,"xmin":200.,"xmax":300.,"latex":"$p_{T}^{\gamma\gamma}$ [GeV]"},
    "pT_yy_b5" :{"name":"pT_yy","title":"p_{T}^{#gamma#gamma} [GeV]","bin":12,"xmin":300.,"xmax":600.,"latex":"$p_{T}^{\gamma\gamma}$ [GeV]"},

    # Truth photons from Higgs
    "HtoYY_n_truth_photons" : {"name":"HtoYY_n_truth_photons","title":"Number of truth photons from Higgs","bin":3,"xmin":-0.5,"xmax":2.5},
    "HtoYY_truth_m_yy" :{"name":"HtoYY_truth_m_yy","title":"Truth m_{#gamma#gamma} from Higgs [GeV]","bin":50,"xmin":105.,"xmax":160., "latex":"Truth $m_{\gamma\gamma}$ [GeV]"},
    "HtoYY_truth_E_y1" :{"name":"HtoYY_truth_E_y1","title":"Leading truth photon from Higgs energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "HtoYY_truth_pT_y1":{"name":"HtoYY_truth_pT_y1","title":"Leading truth photon from Higgs p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400.,"latex":"Leading truth photon from Higgs $p_{T}$ [GeV]"},
    "HtoYY_truth_eta_y1":{"name":"HtoYY_truth_eta_y1","title":"Leading truth photon from Higgs #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Leading truth photon from Higgs $\eta$"},
    "HtoYY_truth_phi_y1":{"name":"HtoYY_truth_phi_y1","title":"Leading truth photon from Higgs #phi",  "bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Leading truth photon from Higgs $\phi$"},
    "HtoYY_truth_E_y2" :{"name":"HtoYY_truth_E_y2","title":"Subleading truth photon from Higgs energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "HtoYY_truth_pT_y2":{"name":"HtoYY_truth_pT_y2","title":"Subleading truth photon from Higgs p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400.,"latex":"Subleading truth photon from Higgs $p_{T}$ [GeV]"},
    "HtoYY_truth_eta_y2":{"name":"HtoYY_truth_eta_y2","title":"Subleading truth photon from Higgs #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Subleading truth photon from Higgs $\eta$"},
    "HtoYY_truth_phi_y2":{"name":"HtoYY_truth_phi_y2","title":"Subleading truth photon from Higgs #phi","bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Subleading truth photon from Higgs $\phi$"},
    # b-jet variables
    "E_b1"  :{"name":"E_b1","title":"Leading b-jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_b1" :{"name":"pT_b1","title":"Leading b-jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Leading b-jet $p_{T}$ [GeV]"},
    "eta_b1":{"name":"eta_b1","title":"Leading b-jet #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Leading b-jet $\eta$"},
    "phi_b1":{"name":"phi_b1","title":"Leading b-jet #phi",  "bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Leading b-jet $\phi$"},
    "btag_score_b1":{"name":"btag_score_b1","title":"Leading b-jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "E_b2"  :{"name":"E_b2","title":"Subleading b-jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_b2" :{"name":"pT_b2","title":"Subleading b-jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Subleading b-jet $p_{T}$ [GeV]"},
    "eta_b2":{"name":"eta_b2","title":"Subleading b-jet #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Subleading b-jet $\eta$"},
    "phi_b2":{"name":"phi_b2","title":"Subleading b-jet #phi","bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Subleading b-jet $\phi$"},
    "btag_score_b2":{"name":"btag_score_b2","title":"Subleading b-jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "m_bb" :{"name":"m_bb","title":"m_{bb} [GeV]","bin":40,"xmin":0.,"xmax":800., "latex":"$m_{bb}$ [GeV]"},
    "pT_bb" :{"name":"pT_bb","title":"p_{T}^{bb} [GeV]","bin":50,"xmin":0.,"xmax":500., "latex":"$p_{T}^{bb}$ [GeV]"},
    # jet variables
    "E_j1"  :{"name":"E_j1","title":"Leading jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_j1" :{"name":"pT_j1","title":"Leading jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Leading jet $p_{T}$ [GeV]"},
    "eta_j1":{"name":"eta_j1","title":"Leading jet #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Leading jet $\eta$"},
    "phi_j1":{"name":"phi_j1","title":"Leading jet #phi",  "bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Leading jet $\phi$"},
    "btag_score_j1":{"name":"btag_score_j1","title":"Leading jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "E_j2"  :{"name":"E_j2","title":"Subleading jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_j2" :{"name":"pT_j2","title":"Subleading jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Subleading jet $p_{T}$ [GeV]"},
    "eta_j2":{"name":"eta_j2","title":"Subleading jet #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Subleading jet $\eta$"},
    "phi_j2":{"name":"phi_j2","title":"Subleading jet #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Subleading jet $\phi$"},
    "btag_score_j2":{"name":"btag_score_j2","title":"Subleading jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "E_j3"  :{"name":"E_j3","title":"Third jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_j3" :{"name":"pT_j3","title":"Third jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Third jet $p_{T}$ [GeV]"},
    "eta_j3":{"name":"eta_j3","title":"Third jet #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Third jet $\eta$"},
    "phi_j3":{"name":"phi_j3","title":"Third jet #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Third jet $\phi$"},
    "btag_score_j3":{"name":"btag_score_j3","title":"Third jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "E_j4"  :{"name":"E_j4","title":"Fourth jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_j4" :{"name":"pT_j4","title":"Fourth jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Fourth jet $p_{T}$ [GeV]"},
    "eta_j4":{"name":"eta_j4","title":"Fourth jet #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Fourth jet $\eta$"},
    "phi_j4":{"name":"phi_j4","title":"Fourth jet #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Fourth jet $\phi$"},
    "btag_score_j4":{"name":"btag_score_j4","title":"Fourth jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "E_j5"  :{"name":"E_j5","title":"Fifth jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_j5" :{"name":"pT_j5","title":"Fifth jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Fifth jet $p_{T}$ [GeV]"},
    "eta_j5":{"name":"eta_j5","title":"Fifth jet #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Fifth jet $\eta$"},
    "phi_j5":{"name":"phi_j5","title":"Fifth jet #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Fifth jet $\phi$"},
    "btag_score_j5":{"name":"btag_score_j5","title":"Fifth jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    "E_j6"  :{"name":"E_j6","title":"Sixth jet energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "pT_j6" :{"name":"pT_j6","title":"Sixth jet p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Sixth jet $p_{T}$ [GeV]"},
    "eta_j6":{"name":"eta_j6","title":"Sixth jet #eta","bin":50,"xmin":-6.0,"xmax":6.0, "latex":"Sixth jet $\eta$"},
    "phi_j6":{"name":"phi_j6","title":"Sixth jet #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Sixth jet $\phi$"},
    "btag_score_j6":{"name":"btag_score_j6","title":"Sixth jet b-tagging score","bin":4,"xmin":-0.5,"xmax":3.5},
    # high-level jet variables
    "HT" :{"name":"HT","title":"H_{T} [GeV]","bin":60,"xmin":0.,"xmax":1200., "latex":"$H_{T}$ [GeV]"},
    "topness" :{"name":"topness","title":"Topness","bin":30,"xmin":0.,"xmax":3.},
    "MET" :{"name":"MET","title":"E_{T}^{miss} [GeV]","bin":50,"xmin":0.,"xmax":500., "latex":"$E_{T}^{miss}$ [GeV]"},
    "MET_phi" :{"name":"MET_phi","title":"#phi(E_{T}^{miss})","bin":100,"xmin":-3.6,"xmax":3.6,"latex":"$\phi(E_{T}^{miss})$"},
    # lepton variables
    "E_e1"  :{"name":"E_e1","title":"Leading electron energy [GeV]","bin":40,"xmin":0.,"xmax":400.},
    "pT_e1" :{"name":"pT_e1","title":"Leading electron p_{T} [GeV]","bin":40,"xmin":0.,"xmax":200.,"latex":"Leading electron $p_{T}$ [GeV]"},
    "eta_e1":{"name":"eta_e1","title":"Leading electron #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Leading electron $\eta$"},
    "phi_e1":{"name":"phi_e1","title":"Leading electron #phi",  "bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Leading electron $\phi$"},
    "E_e2"  :{"name":"E_e2","title":"Subleading electron energy [GeV]","bin":40,"xmin":0.,"xmax":400.},
    "pT_e2" :{"name":"pT_e2","title":"Subleading electron p_{T} [GeV]","bin":40,"xmin":0.,"xmax":200., "latex":"Subleading electron $p_{T}$ [GeV]"},
    "eta_e2":{"name":"eta_e2","title":"Subleading electron #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Subleading electron $\eta$"},
    "phi_e2":{"name":"phi_e2","title":"Subleading electron #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Subleading electron $\phi$"},
    "E_mu1"  :{"name":"E_mu1","title":"Leading muon energy [GeV]","bin":40,"xmin":0.,"xmax":400.},
    "pT_mu1" :{"name":"pT_mu1","title":"Leading muon p_{T} [GeV]","bin":40,"xmin":0.,"xmax":200., "latex":"Leading muon $p_{T}$ [GeV]"},
    "eta_mu1":{"name":"eta_mu1","title":"Leading muon #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Leading muon $\eta$"},
    "phi_mu1":{"name":"phi_mu1","title":"Leading muon #phi",  "bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Leading muon $\phi$"},
    "E_mu2"  :{"name":"E_mu2","title":"Subleading muon energy [GeV]","bin":40,"xmin":0.,"xmax":400.},
    "pT_mu2" :{"name":"pT_mu2","title":"Subleading muon p_{T} [GeV]","bin":40,"xmin":0.,"xmax":200., "latex":"Subleading muon $p_{T}$ [GeV]"},
    "eta_mu2":{"name":"eta_mu2","title":"Subleading muon #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Subleading muon $\eta$"},
    "phi_mu2":{"name":"phi_mu2","title":"Subleading muon #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Subleading muon $\phi$"},
    "E_l1"  :{"name":"E_l1","title":"Leading lepton energy [GeV]","bin":40,"xmin":0.,"xmax":400.},
    "pT_l1" :{"name":"pT_l1","title":"Leading lepton p_{T} [GeV]","bin":40,"xmin":0.,"xmax":200., "latex":"Leading lepton $p_{T}$ [GeV]"},
    "eta_l1":{"name":"eta_l1","title":"Leading lepton #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Leading lepton $\eta$"},
    "phi_l1":{"name":"phi_l1","title":"Leading lepton #phi",  "bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Leading lepton $\phi$"},
    "E_l2"  :{"name":"E_l2","title":"Subleading lepton energy [GeV]","bin":40,"xmin":0.,"xmax":400.},
    "pT_l2" :{"name":"pT_l2","title":"Subleading lepton p_{T} [GeV]","bin":40,"xmin":0.,"xmax":200., "latex":"Subleading lepton $p_{T}$ [GeV]"},
    "eta_l2":{"name":"eta_l2","title":"Subleading lepton #eta","bin":60,"xmin":-6.0,"xmax":6.0,"latex":"Subleading lepton $\eta$"},
    "phi_l2":{"name":"phi_l2","title":"Subleading lepton #phi","bin":40,"xmin":-3.6,"xmax":3.6,"latex":"Subleading lepton $\phi$"},
    "true_E_y1" : {"name":"true_E_y1","title":"Leading photon true energy [GeV]","bin":50,"xmin":0.,"xmax":500.},
    "true_E_y2" : {"name":"true_E_y2","title":"Subleading photon true energy [GeV]","bin":50,"xmin":0.,"xmax":500},
    "true_pT_y1" : {"name":"true_pT_y1","title":"Leading photon true p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Leading lepton $p_T$ [GeV]"},
    "true_pT_y2" : {"name":"true_pT_y2","title":"Subleading photon true p_{T} [GeV]","bin":40,"xmin":0.,"xmax":400., "latex":"Subleading lepton $p_T$ [GeV]"},
    "true_eta_y1" : {"name":"true_eta_y1","title":"Leading photon true #eta","bin":40,"xmin":-6.0,"xmax":6.0, "latex":"Leading photon $\eta$"},
    "true_eta_y2" : {"name":"true_eta_y2","title":"Subleading photon true #eta","bin":40,"xmin":-6.0,"xmax":6.0, "latex":"Subleading photon $\eta$"},
    "true_phi_y1" : {"name":"true_phi_y1","title":"Leading photon true #phi","bin":50,"xmin":-3.6,"xmax":3.6, "latex":"Leading photon $\phi$"},
    "true_phi_y2" : {"name":"true_phi_y2","title":"Subleading photon true #phi","bin":50,"xmin":-3.6,"xmax":3.6, "latex":"Subleading photon $\phi$"},
    "true_m_yy" : {"name":"true_m_yy","title":"True m_{#gamma#gamma} [GeV]","bin":60,"xmin":0.,"xmax":600., "latex":"True $m_{\gamma\gamma}$ [GeV]"},
    'E_higgs' : {"name":"E_higgs","title":"Higgs energy [GeV]","bin":50,"xmin":0.,"xmax":5000.},
    'pT_higgs' : {"name":"pT_higgs","title":"Higgs p_{T} [GeV]","bin":40,"xmin":0.,"xmax":1000., "latex":"Higgs $p_{T}$ [GeV]"},
    'eta_higgs' : {"name":"eta_higgs","title":"Higgs #eta","bin":40,"xmin":-6.0,"xmax":6.0,"latex":"Higgs $\eta$"},
    'phi_higgs' : {"name":"phi_higgs","title":"Higgs #phi","bin":50,"xmin":-3.6,"xmax":3.6,"latex":"Higgs $\phi$"},
    'rapidity_higgs' : {"name":"phi_higgs","title":"Higgs rapidity","bin":50,"xmin":-10,"xmax":10,"latex":"Higgs rapidity"},
    # add more variables here
}