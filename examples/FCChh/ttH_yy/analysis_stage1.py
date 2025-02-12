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
            'mgp8_pp_tth01j_5f_haa': {'chunks':25},
            # Backgrounds 
            'mgp8_pp_jjaa_5f': {'chunks':100}, #yy+jets
            'mgp8_pp_ttaa_semilep_5f_100TeV': {'chunks':5}, #ttyy tester
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
            # all selected photons (isolated, passing particle ID)
            .Define("gamma",  "FCCAnalyses::ReconstructedParticle::get(Photon_objIdx.index, ReconstructedParticles)")
            .Define("selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt({photon_pt})(gamma)".format(photon_pt=self.ana_args.photon_pt))
            .Define("sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_gamma)")
            .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)") #sort by pT
            .Define("n_photons",  "FCCAnalyses::ReconstructedParticle::get_n(sel_gamma)") 
            .Define("E_photons",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)")
            .Define("pT_photons",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)")
            .Define("eta_photons",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)")
            .Define("phi_photons",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)")

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
            # subleading photon
            .Define("E_y2", "(n_photons > 1) ? E_photons[1] : -999.")
            .Define("pT_y2", "(n_photons > 1) ? pT_photons[1] : -999.")
            .Define("eta_y2", "(n_photons > 1) ? eta_photons[1] : -999.")
            .Define("phi_y2", "(n_photons > 1) ? phi_photons[1] : -999.")
            .Define("rel_pT_y2", "(n_photons > 1) ? pT_y2/m_yy[0] : -999.")
            
            ########################################### ELECTRONS ########################################### 

            .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("n_electrons",  "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
            .Define("E_electrons",  "FCCAnalyses::ReconstructedParticle::get_e(electrons)")
            .Define("pT_electrons",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
            .Define("eta_electrons",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons)")
            .Define("phi_electrons",  "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
            # ee object
            .Define("ee_pairs_unmerged", "AnalysisFCChh::getPairs(electrons)") # retrieves the leading pT pair of all possible 
            .Define("ee_pairs", "AnalysisFCChh::merge_pairs(ee_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_ee", "FCCAnalyses::ReconstructedParticle::get_mass(ee_pairs)")

            ########################################### MUONS ########################################### 

            .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 
            .Define("n_muons",  "FCCAnalyses::ReconstructedParticle::get_n(muons)")
            .Define("E_muons",  "FCCAnalyses::ReconstructedParticle::get_e(muons)")
            .Define("pT_muons",  "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
            .Define("eta_muons",  "FCCAnalyses::ReconstructedParticle::get_eta(muons)")
            .Define("phi_muons",  "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
            # mumu object
            .Define("mumu_pairs_unmerged", "AnalysisFCChh::getPairs(muons)") # retrieves the leading pT pair of all possible 
            .Define("mumu_pairs", "AnalysisFCChh::merge_pairs(mumu_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_mumu", "FCCAnalyses::ReconstructedParticle::get_mass(mumu_pairs)")

            ########################################### JETS ########################################### 
            # selected jets above a pT threshold of 25 GeV
            .Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt({jet_pt})(Jet)".format(jet_pt=self.ana_args.jet_pt))
            .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(selpt_jets)") 
            .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
            .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)")
            .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)")
            .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)")
            .Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)")
            # b-tagging information
            .Define("pass_loose_btag_jets", "AnalysisFCChh::get_pass_tag(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("pass_medium_btag_jets", "AnalysisFCChh::get_pass_tag(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("pass_tight_btag_jets", "AnalysisFCChh::get_pass_tag(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 2)") #bit 2 = tight WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            # selected central jets (|eta| < 2.5)
            .Define("central_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(2.5)(selpt_jets)")
            .Define("central_jets", "AnalysisFCChh::SortParticleCollection(central_jets_unsort)") 
            .Define("n_central_jets",  "FCCAnalyses::ReconstructedParticle::get_n(central_jets)")
            # b-tagged jets at medium working point
            .Define("b_tagged_jets", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)")
            # select medium b-jets with pT > 25 GeV, |eta| < 4
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt({jet_pt})(b_tagged_jets)".format(jet_pt=self.ana_args.jet_pt))
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)") #sort by pT
            .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
            .Define("E_bjets",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)")
            .Define("pT_bjets",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
            .Define("eta_bjets",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)")
            .Define("phi_bjets",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)")
            # bb object
            .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(selpt_bjets)") # retrieves the leading pT pair of all possible 
            .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")
            .Define("pT_bb", "FCCAnalyses::ReconstructedParticle::get_pt(bb_pairs)")
            # scalar sum of all jet's momenta
            .Define("HT", "AnalysisFCChh::get_HT_jets(Jet)")

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
            'n_photons', 'E_photons', 'pT_photons', 'eta_photons', 'phi_photons', 
            'm_yy', "pT_yy", "rapidity_yy",
            "E_y1", "pT_y1", "eta_y1", "phi_y1", "rel_pT_y1",
            "E_y2", "pT_y2", "eta_y2", "phi_y2", "rel_pT_y2",
            # Leptons
            'n_electrons', 'E_electrons', 'pT_electrons', 'eta_electrons', 'phi_electrons', 
            "m_ee",
            'n_muons', 'E_muons', 'pT_muons', 'eta_muons', 'phi_muons',
            "m_mumu",
            # Jets and b-tagged jets:
            'n_jets', 'E_jets', 'pT_jets', 'eta_jets', 'phi_jets', 
            "pass_loose_btag_jets", "pass_medium_btag_jets", "pass_tight_btag_jets",
            "n_central_jets",
            'n_bjets', 'E_bjets', 'pT_bjets', 'eta_bjets', 'phi_bjets', 
            "m_bb", "pT_bb",
            "HT",
            # Missing transverse energy
            'MET', 'MET_x', 'MET_y', 'MET_phi'
        ]
        return branch_list