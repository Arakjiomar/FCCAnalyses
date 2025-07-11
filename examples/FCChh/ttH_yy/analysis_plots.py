import ROOT
import os 

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow ttH(#rightarrow #gamma#gamma)'
delphesVersion = '3.4.2'
energy         = 50
collider       = 'FCC-hh'
inputDir       = '/eos/home-o/oarakji/tth/myFinalAnalyses/'
formats        = ['pdf'] #['png','pdf']
yaxis          = ['lin','log']
# stacksig       = ['nostack']
stacksig       = ['stack','nostack']
outdir         = '/eos/home-o/oarakji/tth/myHist/ttH_single_process'
plotStatUnc    = True


variables = ['n_photons','n_bjets', 'm_yy', 'pT_yy', 'pT_yy_b1', 'pT_yy_b2', 'pT_yy_b3', 'pT_yy_b4', 'pT_yy_b5', 'm_yy_cut']



# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ttHyy_analysis'] = ["nocuts", "photons", "pT_yy_bin1", "pT_yy_bin2", "pT_yy_bin3", "pT_yy_bin4", "pT_yy_bin5"]

extralabel = {}
extralabel['nocuts'] = "all events"
extralabel['photons'] = "photon pair, pT_y1 & pT_y2 > 25 GeV"
extralabel['pT_yy_bin1'] = "Diphoton pT [0 to 60 GeV]"
extralabel['pT_yy_bin2'] = "Diphoton pT [60 to 120 GeV]"
extralabel['pT_yy_bin3'] = "Diphoton pT [120 to 200 GeV]"
extralabel['pT_yy_bin4'] = "Diphoton pT [200 to 300 GeV]"
extralabel['pT_yy_bin5'] = "Diphoton pT [>= 300 GeV]"
# extralabel['TTH_CEN_PTH_0_60_pT_yy_bin1'] = "Higgs truth pT  [0 to 60 GeV], Diphoton pT  [0 to 60 GeV]"
# extralabel['TTH_CEN_PTH_0_60_pT_yy_bin2'] = "Higgs truth pT [0 to 60 GeV], Diphoton pT [60 to 120 GeV]"
# extralabel['TTH_CEN_PTH_0_60_pT_yy_bin3'] = "Higgs truth pT [0 to 60 GeV], Diphoton pT [120 to 200 GeV]"
# extralabel['TTH_CEN_PTH_0_60_pT_yy_bin4'] = "Higgs truth pT  0 to 60 GeV], Diphoton pT [200 to 300 GeV]"
# extralabel['TTH_CEN_PTH_0_60_pT_yy_bin5'] = "Higgs truth pT [0 to 60 GeV], Diphoton pT [>= 300 GeV]"


colors = {}
colors['ttHyy_signal'] = ROOT.kBlack
# colors['yy_jets'] = ROOT.kGreen
colors['ttyy'] = ROOT.kCyan
colors['vh'] = ROOT.kGreen
colors['th'] = ROOT.kRed
colors['vbf'] = ROOT.kOrange
colors['ggF'] = ROOT.kYellow
colors['thw'] = ROOT.kMagenta

plots = {}
plots['ttHyy_analysis'] = {
                            'signal':{'ttHyy_signal':[ 'mgp8_pp_tth01j_5f_50TeV']},
                            'backgrounds':{
                                'ttyy':[ 'mgp8_pp_ttaa01j_5f_50TeV'],
                                'vh':['mgp8_pp_vh012j_5f_50TeV'],
                                'th':['mgp8_pp_th12j_5f_50TeV'],
                                'vbf':['mgp8_pp_vbf_h01j_5f_50TeV'],
                                'ggF':['mgp8_pp_h01j_5f_50TeV'],
                                'thw':['mgp8_pp_thw01j_5f_50TeV'],
                            },
           }


legend = {}
legend['ttHyy_signal'] = 'ttH(#rightarrow #gamma#gamma)'
legend['yy_jets'] = '#gamma#gamma+jets'
legend['ttyy'] = 'tt#gamma#gamma'
legend['vh'] = 'VH'
legend['th'] = 'tH'
legend['vbf'] = 'VBF'
legend['ggF'] = 'ggF'
legend['thw'] = 'tHW'