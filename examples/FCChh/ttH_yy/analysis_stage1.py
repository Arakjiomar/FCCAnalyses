'''
Ntuple production for FCC-hh analysis of ttH(yy)
'''
from argparse import ArgumentParser
import os


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    FCC-hh ttH(yy) analysis
    '''
    def __init__(self, cmdline_args):
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provide additional arguments after analysis script path')
        parser.add_argument('--photon-pt', default='10.', type=float,
                             help='Minimal pT of the selected photons.')
        parser.add_argument('--jet-pt', default='25.', type=float,
                             help='Minimal pT of the selected jets.')
        # Parse additional arguments not known to the FCCAnalyses parsers
        # All command line arguments know to fccanalysis are provided in the
        # `cmdline_arg` dictionary.
        self.ana_args, _ = parser.parse_known_args(cmdline_args['unknown'])

        # Mandatory: List of processes to run over
        self.process_list = {
            # # Add your processes like this: 
            ## '<name of process>':{'fraction':<fraction of events to run over>, 'chunks':<number of chunks to split the output into>, 'output':<name of the output file> }, 
            # # - <name of process> needs to correspond either the name of the input .root file, or the name of a directory containing root files 
            # # If you want to process only part of the events, split the output into chunks or give a different name to the output use the optional arguments
            # # or leave blank to use defaults = run the full statistics in one output file named the same as the process:
            # ttH(yy) signal
            #'mgp8_pp_tth01j_5f_haa': {'chunks':25},
            # Backgrounds 
            'mgp8_pp_jjaa_5f': {'chunks':50}, #yy+jets
            #'mgp8_pp_ttaa_semilep_5f_100TeV': {'chunks':5}, #ttyy tester
        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v06/II/'

        # Optional: output directory, default is local running directory
        self.output_dir = '/eos/user/e/elmazzeo/ttH@FCC-hh/results/2025-02-11' + '/ntuples/'

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh ttH(yy) analysis'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        self.run_batch = True

        # Optional: Use weighted events
        self.do_weighted = True 

        # Optional: read the input files with podio::DataSource 
        self.use_data_source = False # explicitly use old way in this version 

        # Optional: test file that is used if you run with the --test argument 
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'generation/DelphesEvents/fcc_v06/II/mgp8_pp_tth01j_5f_haa/' \
                         'events_000000001.root'


    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''

        dframe2 = (
            dframe

            ########################################### DEFINITION OF VARIABLES ########################################### 

            # generator event weight
            .Define("weight",  "EventHeader.weight")

            ########################################### PHOTONS ########################################### 
            # all photons passing particle ID
            .Define("gamma",  "FCCAnalyses::ReconstructedParticle::get(PhotonNoIso_objIdx.index, ReconstructedParticles)")
            .Define("idx_gamma",  "FCCAnalyses::ReconstructedParticle::get_idx(gamma)")
            # apply pT selection
            .Define("selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt({photon_pt})(gamma)".format(photon_pt=self.ana_args.photon_pt))
            .Define("idx_selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt({photon_pt})(gamma, idx_gamma)".format(photon_pt=self.ana_args.photon_pt))
            # apply |eta| selection
            .Define("sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4.)(selpt_gamma)")
            .Define("idx_sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4.)(selpt_gamma, idx_selpt_gamma)")
            # sort photons by pT
            .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)") 
            .Define("idx_sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort, idx_sel_gamma_unsort)")
            # output branches
            .Define("n_photons",  "FCCAnalyses::ReconstructedParticle::get_n(sel_gamma)") 
            .Define("E_photons",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)")
            .Define("pT_photons",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)")
            .Define("eta_photons",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)")
            .Define("phi_photons",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)")
            .Define("iso_photons",  "FCCAnalyses::ReconstructedParticle::get(idx_sel_gamma, PhotonNoIso_IsolationVar)")
            # H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
            .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(sel_gamma)") # retrieves the leading pT pair of all possible 
            .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")
            .Define("pT_yy", "FCCAnalyses::ReconstructedParticle::get_pt(yy_pairs)")
            .Define("rapidity_yy", "FCCAnalyses::ReconstructedParticle::get_y(yy_pairs)")
            # leading photon
            .Define("E_y1", "(n_photons > 0) ? E_photons[0] : -999.")
            .Define("pT_y1", "(n_photons > 0) ? pT_photons[0] : -999.")
            .Define("eta_y1", "(n_photons > 0) ? eta_photons[0] : -999.")
            .Define("phi_y1", "(n_photons > 0) ? phi_photons[0] : -999.")
            .Define("rel_pT_y1", "(n_photons > 0) ? pT_y1/m_yy[0] : -999.")
            .Define("iso_y1", "(n_photons > 0) ? iso_photons[0] : -999.")
            # subleading photon
            .Define("E_y2", "(n_photons > 1) ? E_photons[1] : -999.")
            .Define("pT_y2", "(n_photons > 1) ? pT_photons[1] : -999.")
            .Define("eta_y2", "(n_photons > 1) ? eta_photons[1] : -999.")
            .Define("phi_y2", "(n_photons > 1) ? phi_photons[1] : -999.")
            .Define("rel_pT_y2", "(n_photons > 1) ? pT_y2/m_yy[0] : -999.")
            .Define("iso_y2", "(n_photons > 1) ? iso_photons[1] : -999.")

            ########################################### ELECTRONS ########################################### 

            .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("n_all_electrons",  "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
            .Define("E_electrons",  "FCCAnalyses::ReconstructedParticle::get_e(electrons)")
            .Define("pT_electrons",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
            .Define("eta_electrons",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons)")
            .Define("phi_electrons",  "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
            # ee object
            .Define("ee_pairs_unmerged", "AnalysisFCChh::getPairs(electrons)") # retrieves the leading pT pair of all possible 
            .Define("ee_pairs", "AnalysisFCChh::merge_pairs(ee_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_ee", "FCCAnalyses::ReconstructedParticle::get_mass(ee_pairs)")
            # select electrons at 15 GeV
            .Define("sel_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(15.)(electrons)")
            .Define("n_electrons",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
            # first two electrons
            # leading electron
            .Define("E_e1", "(n_electrons > 0) ? E_electrons[0] : -999.")
            .Define("pT_e1", "(n_electrons > 0) ? pT_electrons[0] : -999.")
            .Define("eta_e1", "(n_electrons > 0) ? eta_electrons[0] : -999.")
            .Define("phi_e1", "(n_electrons > 0) ? phi_electrons[0] : -999.")
            # subleading electron
            .Define("E_e2", "(n_electrons > 1) ? E_electrons[1] : -999.")
            .Define("pT_e2", "(n_electrons > 1) ? pT_electrons[1] : -999.")
            .Define("eta_e2", "(n_electrons > 1) ? eta_electrons[1] : -999.")
            .Define("phi_e2", "(n_electrons > 1) ? phi_electrons[1] : -999.")

            ########################################### MUONS ########################################### 

            .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 
            .Define("n_all_muons",  "FCCAnalyses::ReconstructedParticle::get_n(muons)")
            .Define("E_muons",  "FCCAnalyses::ReconstructedParticle::get_e(muons)")
            .Define("pT_muons",  "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
            .Define("eta_muons",  "FCCAnalyses::ReconstructedParticle::get_eta(muons)")
            .Define("phi_muons",  "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
            # select muons at 15 GeV
            .Define("sel_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(15.)(muons)")
            .Define("n_muons",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)")
            # mumu object
            .Define("mumu_pairs_unmerged", "AnalysisFCChh::getPairs(muons)") # retrieves the leading pT pair of all possible 
            .Define("mumu_pairs", "AnalysisFCChh::merge_pairs(mumu_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_mumu", "FCCAnalyses::ReconstructedParticle::get_mass(mumu_pairs)")
            # first two muons
            # leading muon
            .Define("E_mu1", "(n_muons > 0) ? E_muons[0] : -999.")
            .Define("pT_mu1", "(n_muons > 0) ? pT_muons[0] : -999.")
            .Define("eta_mu1", "(n_muons > 0) ? eta_muons[0] : -999.")
            .Define("phi_mu1", "(n_muons > 0) ? phi_muons[0] : -999.")
            # subleading muon
            .Define("E_mu2", "(n_muons > 1) ? E_muons[1] : -999.")
            .Define("pT_mu2", "(n_muons > 1) ? pT_muons[1] : -999.")
            .Define("eta_mu2", "(n_muons > 1) ? eta_muons[1] : -999.")
            .Define("phi_mu2", "(n_muons > 1) ? phi_muons[1] : -999.")

            ########################################### JETS ########################################### 

            # get jets and their indices
            .Define("idx_jets", "FCCAnalyses::ReconstructedParticle::get_idx(Jet)")
            # select jets with pT > 25 GeV
            .Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt({jet_pt})(Jet)".format(jet_pt=self.ana_args.jet_pt))
            .Define("idx_selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt({jet_pt})(Jet,idx_jets)".format(jet_pt=self.ana_args.jet_pt))
            # sort jets by pT
            .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(selpt_jets)") 
            .Define("idx_sel_jets", "AnalysisFCChh::SortParticleCollection(selpt_jets, idx_selpt_jets)")
            # output branches
            .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
            .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)")
            .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)")
            .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)")
            .Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)")
            # b-tagging information
            .Define("pass_loose_btag_jets", "AnalysisFCChh::get_pass_tag(idx_sel_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("pass_medium_btag_jets", "AnalysisFCChh::get_pass_tag(idx_sel_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("pass_tight_btag_jets", "AnalysisFCChh::get_pass_tag(idx_sel_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 2)") #bit 2 = tight WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("btag_score_jets", "AnalysisFCChh::get_btagging_score(pass_loose_btag_jets, pass_medium_btag_jets, pass_tight_btag_jets)") 
            # first six jets
            # leading jet
            .Define("E_j1", "(n_jets > 0) ? E_jets[0] : -999.")
            .Define("pT_j1", "(n_jets > 0) ? pT_jets[0] : -999.")
            .Define("eta_j1", "(n_jets > 0) ? eta_jets[0] : -999.")
            .Define("phi_j1", "(n_jets > 0) ? phi_jets[0] : -999.")
            .Define("pass_loose_btag_j1", "(n_jets > 0) ? pass_loose_btag_jets[0] : -999.")
            .Define("pass_medium_btag_j1", "(n_jets > 0) ? pass_medium_btag_jets[0] : -999.")
            .Define("pass_tight_btag_j1", "(n_jets > 0) ? pass_tight_btag_jets[0] : -999.")
            .Define("btag_score_j1", "(n_jets > 0) ? btag_score_jets[0] : -999.")
            # subleading jet
            .Define("E_j2", "(n_jets > 1) ? E_jets[1] : -999.")
            .Define("pT_j2", "(n_jets > 1) ? pT_jets[1] : -999.")
            .Define("eta_j2", "(n_jets > 1) ? eta_jets[1] : -999.")
            .Define("phi_j2", "(n_jets > 1) ? phi_jets[1] : -999.")
            .Define("pass_loose_btag_j2", "(n_jets > 1) ? pass_loose_btag_jets[1] : -999.")
            .Define("pass_medium_btag_j2", "(n_jets > 1) ? pass_medium_btag_jets[1] : -999.")
            .Define("pass_tight_btag_j2", "(n_jets > 1) ? pass_tight_btag_jets[1] : -999.")
            .Define("btag_score_j2", "(n_jets > 1) ? btag_score_jets[1] : -999.")
            # 3-rd jet
            .Define("E_j3", "(n_jets > 2) ? E_jets[2] : -999.")
            .Define("pT_j3", "(n_jets > 2) ? pT_jets[2] : -999.")
            .Define("eta_j3", "(n_jets > 2) ? eta_jets[2] : -999.")
            .Define("phi_j3", "(n_jets > 2) ? phi_jets[2] : -999.")
            .Define("pass_loose_btag_j3", "(n_jets > 2) ? pass_loose_btag_jets[2] : -999.")
            .Define("pass_medium_btag_j3", "(n_jets > 2) ? pass_medium_btag_jets[2] : -999.")
            .Define("pass_tight_btag_j3", "(n_jets > 2) ? pass_tight_btag_jets[2] : -999.")
            .Define("btag_score_j3", "(n_jets > 2) ? btag_score_jets[2] : -999.")
            # 4-th jet
            .Define("E_j4", "(n_jets > 3) ? E_jets[3] : -999.")
            .Define("pT_j4", "(n_jets > 3) ? pT_jets[3] : -999.")
            .Define("eta_j4", "(n_jets > 3) ? eta_jets[3] : -999.")
            .Define("phi_j4", "(n_jets > 3) ? phi_jets[3] : -999.")
            .Define("pass_loose_btag_j4", "(n_jets > 3) ? pass_loose_btag_jets[3] : -999.")
            .Define("pass_medium_btag_j4", "(n_jets > 3) ? pass_medium_btag_jets[3] : -999.")
            .Define("pass_tight_btag_j4", "(n_jets > 3) ? pass_tight_btag_jets[3] : -999.")
            .Define("btag_score_j4", "(n_jets > 3) ? btag_score_jets[3] : -999.")
            # 5-th jet
            .Define("E_j5", "(n_jets > 4) ? E_jets[4] : -999.")
            .Define("pT_j5", "(n_jets > 4) ? pT_jets[4] : -999.")
            .Define("eta_j5", "(n_jets > 4) ? eta_jets[4] : -999.")
            .Define("phi_j5", "(n_jets > 4) ? phi_jets[4] : -999.")
            .Define("pass_loose_btag_j5", "(n_jets > 4) ? pass_loose_btag_jets[4] : -999.")
            .Define("pass_medium_btag_j5", "(n_jets > 4) ? pass_medium_btag_jets[4] : -999.")
            .Define("pass_tight_btag_j5", "(n_jets > 4) ? pass_tight_btag_jets[4] : -999.")
            .Define("btag_score_j5", "(n_jets > 4) ? btag_score_jets[4] : -999.")
            # 6-th jet
            .Define("E_j6", "(n_jets > 5) ? E_jets[5] : -999.")
            .Define("pT_j6", "(n_jets > 5) ? pT_jets[5] : -999.")
            .Define("eta_j6", "(n_jets > 5) ? eta_jets[5] : -999.")
            .Define("phi_j6", "(n_jets > 5) ? phi_jets[5] : -999.")
            .Define("pass_loose_btag_j6", "(n_jets > 5) ? pass_loose_btag_jets[5] : -999.")
            .Define("pass_medium_btag_j6", "(n_jets > 5) ? pass_medium_btag_jets[5] : -999.")
            .Define("pass_tight_btag_j6", "(n_jets > 5) ? pass_tight_btag_jets[5] : -999.")
            .Define("btag_score_j6", "(n_jets > 5) ? btag_score_jets[5] : -999.")
            # selected central jets (|eta| < 2.5)
            .Define("central_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(2.5)(selpt_jets)")
            .Define("central_jets", "AnalysisFCChh::SortParticleCollection(central_jets_unsort)") 
            .Define("n_central_jets",  "FCCAnalyses::ReconstructedParticle::get_n(central_jets)")
            # b-tagged jets at medium working point
            .Define("b_tagged_jets", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)")
            .Define("idx_b_tagged_jets", "AnalysisFCChh::get_tagged_jets_idx(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)")
            # select medium b-jets with pT > 25 GeV
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt({jet_pt})(b_tagged_jets)".format(jet_pt=self.ana_args.jet_pt))
            .Define("idx_selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt({jet_pt})(b_tagged_jets, idx_b_tagged_jets)".format(jet_pt=self.ana_args.jet_pt))
            # select mediumd b-jets with pT > 25 GeV and with |eta| < 4
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("idx_sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets, idx_selpt_bjets)")
            # sort selected b-jets by pT
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)") 
            .Define("idx_sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort, idx_sel_bjets_unsort)")
            # save output branches
            .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
            .Define("E_bjets",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)")
            .Define("pT_bjets",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
            .Define("eta_bjets",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)")
            .Define("phi_bjets",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)")
            .Define("pass_loose_btag_bjets", "AnalysisFCChh::get_pass_tag(idx_sel_bjets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)")
            .Define("pass_medium_btag_bjets", "AnalysisFCChh::get_pass_tag(idx_sel_bjets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") 
            .Define("pass_tight_btag_bjets", "AnalysisFCChh::get_pass_tag(idx_sel_bjets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 2)") 
            .Define("btag_score_bjets", "AnalysisFCChh::get_btagging_score(pass_loose_btag_bjets, pass_medium_btag_bjets, pass_tight_btag_bjets)") 
            # bb object
            .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(selpt_bjets)") # retrieves the leading pT pair of all possible 
            .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")
            .Define("pT_bb", "FCCAnalyses::ReconstructedParticle::get_pt(bb_pairs)")
            # first two b-jets
            # leading b-jet
            .Define("E_b1", "(n_bjets > 0) ? E_bjets[0] : -999.")
            .Define("pT_b1", "(n_bjets > 0) ? pT_bjets[0] : -999.")
            .Define("eta_b1", "(n_bjets > 0) ? eta_bjets[0] : -999.")
            .Define("phi_b1", "(n_bjets > 0) ? phi_bjets[0] : -999.")
            .Define("pass_loose_btag_b1", "(n_bjets > 0) ? pass_loose_btag_bjets[0] : -999.")
            .Define("pass_medium_btag_b1", "(n_bjets > 0) ? pass_medium_btag_bjets[0] : -999.")
            .Define("pass_tight_btag_b1", "(n_bjets > 0) ? pass_tight_btag_bjets[0] : -999.")
            .Define("btag_score_b1", "(n_bjets > 0) ? btag_score_bjets[0] : -999.")
            # subleading b-jet
            .Define("E_b2", "n_bjets > 1 ? E_bjets[1] : -999.")
            .Define("pT_b2", "n_bjets > 1 ? pT_bjets[1] : -999.")
            .Define("eta_b2", "n_bjets > 1 ? eta_bjets[1] : -999.")
            .Define("phi_b2", "n_bjets > 1 ? phi_bjets[1] : -999.")
            .Define("pass_loose_btag_b2", "(n_bjets > 1) ? pass_loose_btag_bjets[1] : -999.")
            .Define("pass_medium_btag_b2", "(n_bjets > 1) ? pass_medium_btag_bjets[1] : -999.")
            .Define("pass_tight_btag_b2", "(n_bjets > 1) ? pass_tight_btag_bjets[1] : -999.")
            .Define("btag_score_b2", "(n_bjets > 1) ? btag_score_bjets[1] : -999.")
            # scalar sum of all jet's momenta
            .Define("HT", "AnalysisFCChh::get_HT_jets(Jet)")
            # topness
            .Define("topness", "AnalysisFCChh::get_topness(sel_jets)")
            ########################################### MET ########################################### 
            .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
            .Define("MET_x", "FCCAnalyses::ReconstructedParticle::get_px(MissingET)")
            .Define("MET_y", "FCCAnalyses::ReconstructedParticle::get_py(MissingET)")
            .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")


        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'weight',
            # Photons
            'n_photons', 'E_photons', 'pT_photons', 'eta_photons', 'phi_photons', 'iso_photons',
            'm_yy', "pT_yy", "rapidity_yy",
            "E_y1", "pT_y1", "eta_y1", "phi_y1", "rel_pT_y1", "iso_y1",
            "E_y2", "pT_y2", "eta_y2", "phi_y2", "rel_pT_y2", "iso_y2",
            # Leptons
            'n_electrons', 'n_all_electrons', 'E_electrons', 'pT_electrons', 'eta_electrons', 'phi_electrons', 
            "m_ee",
            "E_e1", "pT_e1", "eta_e1", "phi_e1",
            "E_e2", "pT_e2", "eta_e2", "phi_e2",
            'n_muons', 'n_all_muons', 'E_muons', 'pT_muons', 'eta_muons', 'phi_muons',
            "m_mumu",
            "E_mu1", "pT_mu1", "eta_mu1", "phi_mu1",
            "E_mu2", "pT_mu2", "eta_mu2", "phi_mu2",
            # Jets and b-tagged jets:
            'n_jets', 'E_jets', 'pT_jets', 'eta_jets', 'phi_jets', 
            "pass_loose_btag_jets", "pass_medium_btag_jets", "pass_tight_btag_jets",
            "btag_score_jets",
             "E_j1", "pT_j1", "eta_j1", "phi_j1", "pass_loose_btag_j1", "pass_medium_btag_j1", "pass_tight_btag_j1", "btag_score_j1",
             "E_j2", "pT_j2", "eta_j2", "phi_j2", "pass_loose_btag_j2", "pass_medium_btag_j2", "pass_tight_btag_j2", "btag_score_j2",
             "E_j3", "pT_j3", "eta_j3", "phi_j3", "pass_loose_btag_j3", "pass_medium_btag_j3", "pass_tight_btag_j3", "btag_score_j3",
             "E_j4", "pT_j4", "eta_j4", "phi_j4", "pass_loose_btag_j4", "pass_medium_btag_j4", "pass_tight_btag_j4", "btag_score_j4",
             "E_j5", "pT_j5", "eta_j5", "phi_j5", "pass_loose_btag_j5", "pass_medium_btag_j5", "pass_tight_btag_j5", "btag_score_j5",
             "E_j6", "pT_j6", "eta_j6", "phi_j6", "pass_loose_btag_j6", "pass_medium_btag_j6", "pass_tight_btag_j6", "btag_score_j6",
            "n_central_jets",
            'n_bjets', 'E_bjets', 'pT_bjets', 'eta_bjets', 'phi_bjets', 
            "pass_loose_btag_bjets", "pass_medium_btag_bjets", "pass_tight_btag_bjets",
            "btag_score_bjets",
            "E_b1", "pT_b1", "eta_b1", "phi_b1", "pass_loose_btag_b1", "pass_medium_btag_b1", "pass_tight_btag_b1", "btag_score_b1",
            "E_b2", "pT_b2", "eta_b2", "phi_b2", "pass_loose_btag_b2", "pass_medium_btag_b2", "pass_tight_btag_b2", "btag_score_b2",
            "m_bb", "pT_bb",
            "HT", "topness",
            # Missing transverse energy
            'MET', 'MET_x', 'MET_y', 'MET_phi'
        ]
        return branch_list