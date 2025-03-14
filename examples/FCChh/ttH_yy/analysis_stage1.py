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
            'mgp8_pp_tth01j_5f_84TeV_haaexcl' : {'chunks': 100},
            # Backgrounds 
           # 'mgp8_pp_ttaa01j_5f_84TeV': {'chunks':100}, #ttyy+jets
           # 'mgp8_pp_Vaajj_HF_5f_84TeV' : {'chunks': 100}, #V+yy+bb/cc
            # HH->bbyy test
           # 'pwp8_pp_hh_lambda100_5f_hhbbaa' : {'chunks': 100},
        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/'
        #self.input_dir =  '/eos/user/b/bistapf/FCChh_sample_testers/'

        # Optional: output directory, default is local running directory
        self.output_dir = '/eos/user/e/elmazzeo/ttH@FCC-hh/results/2025-03-10' + '/ntuples/'

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
                         'generation/DelphesEvents/fcc_v07/II/mgp8_pp_tth01j_5f_84TeV_haaexcl/' \
                         'events_119603512.root'


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
            .Define("gamma",  "FCCAnalyses::ReconstructedParticle::get(Photon_objIdx.index, ReconstructedParticles)")
            .Define("idx_gamma",  "FCCAnalyses::ReconstructedParticle::get_idx(gamma)")
            # apply pT selection
            .Define("selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt({photon_pt})(gamma)".format(photon_pt=self.ana_args.photon_pt))
            .Define("idx_selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt({photon_pt})(gamma, idx_gamma)".format(photon_pt=self.ana_args.photon_pt))
            .Define("idx_selpt_gamma1", "FCCAnalyses::ReconstructedParticle::sel_pt({photon_pt})(gamma, Photon_objIdx.index)".format(photon_pt=self.ana_args.photon_pt))
            # apply |eta| selection
            .Define("sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(6.)(selpt_gamma)")
            .Define("idx_sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(6.)(selpt_gamma, idx_selpt_gamma)")
            .Define("idx_sel_gamma_unsort1", "FCCAnalyses::ReconstructedParticle::sel_eta(6.)(selpt_gamma, idx_selpt_gamma1)")
            # sort photons by pT
            .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)") 
            .Define("idx_sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort, idx_sel_gamma_unsort)")
            .Define("idx_sel_gamma1", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort, idx_sel_gamma_unsort1)")
            # output branches
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
            # theta between the two photons
            .Define("theta_y_y", "(n_photons > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).Vect().Angle(FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).Vect()) : -999.")
            .Define("cos_theta_y_y", "(n_photons > 1) ? TMath::Cos(theta_y_y) : -999.")
            # leading photon
            .Define("E_y1", "(n_photons > 0) ? E_photons[0] : -999.")
            .Define("pT_y1", "(n_photons > 0) ? pT_photons[0] : -999.")
            .Define("eta_y1", "(n_photons > 0) ? eta_photons[0] : -999.")
            .Define("phi_y1", "(n_photons > 0) ? phi_photons[0] : -999.")
            .Define("rel_pT_y1", "(n_photons > 0) ? pT_y1/m_yy[0] : -999.")
            .Define("idx_y1", "(n_photons > 0) ? idx_sel_gamma1[0] : -999.")
            # subleading photon
            .Define("E_y2", "(n_photons > 1) ? E_photons[1] : -999.")
            .Define("pT_y2", "(n_photons > 1) ? pT_photons[1] : -999.")
            .Define("eta_y2", "(n_photons > 1) ? eta_photons[1] : -999.")
            .Define("phi_y2", "(n_photons > 1) ? phi_photons[1] : -999.")
            .Define("rel_pT_y2", "(n_photons > 1) ? pT_y2/m_yy[0] : -999.")
            .Define("idx_y2", "(n_photons > 1) ? idx_sel_gamma1[1] : -999.")
            .Define("DR_y_y", "(n_photons > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1])) : -999.")
            # reco-to-MC particle association
            .Alias("MCRecoAssociations0", "_MCRecoAssociations_from.index")
            .Alias("MCRecoAssociations1", "_MCRecoAssociations_to.index")
            .Define("true_TLV", "ReconstructedParticle2MC::getRP2MC_tlv(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
            .Define("pdgID_y1", "(idx_y1 >= 0 ) ? ReconstructedParticles.PDG.at(idx_y1) : -999")
            .Define("pdgID_y2", "(idx_y2 >= 0 ) ? ReconstructedParticles.PDG.at(idx_y2) : -999")
            .Define("true_TLV_y1", "(idx_y1 >= 0) ? true_TLV[idx_y1] : TLorentzVector(0.,0.,0.,0.)")
            .Define("true_TLV_y2", "(idx_y2 >= 0) ? true_TLV[idx_y2] : TLorentzVector(0.,0.,0.,0.)")
            .Define('true_E_y1',"(idx_y1 >= 0) ? true_TLV_y1.E() : -999.")
            .Define('true_pT_y1',"(idx_y1 >= 0) ? true_TLV_y1.Pt() : -999.")
            .Define('true_eta_y1',"(idx_y1 >= 0) ? true_TLV_y1.Eta() : -999.")
            .Define('true_phi_y1',"(idx_y1 >= 0) ? true_TLV_y1.Phi() : -999.")
            .Define('true_E_y2',"(idx_y2 >= 0) ? true_TLV_y2.E() : -999.")
            .Define('true_pT_y2',"(idx_y2 >= 0) ? true_TLV_y2.Pt() : -999.")
            .Define('true_eta_y2',"(idx_y2 >= 0) ? true_TLV_y2.Eta() : -999.")
            .Define('true_phi_y2',"(idx_y2 >= 0) ? true_TLV_y2.Phi() : -999.")
            .Define('true_m_yy',"(idx_y1 >= 0 && idx_y2 >=0) ? (true_TLV_y1 + true_TLV_y2).M() : -999.")
            .Define('true_DR_y_y',"(idx_y1 >= 0 && idx_y2 >=0) ? true_TLV_y1.DeltaR(true_TLV_y2) : -999.")
            .Define('true_pT_yy',"(idx_y1 >= 0 && idx_y2 >=0) ? (true_TLV_y1 + true_TLV_y2).Pt() : -999.")
            .Define("true_theta_y_y", "(idx_y1 >= 0 && idx_y2 >=0) ? true_TLV_y1.Vect().Angle(true_TLV_y2.Vect()) : -999.")
            .Define("true_cos_theta_y_y", "(idx_y1 >= 0 && idx_y2 >=0) ? TMath::Cos(true_theta_y_y) : -999.")
            # check if the selected reco photons have Higgs parents
            .Define("RP2MC_index", "FCCAnalyses::ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles)")
            .Define("has_higgs_parent_y1", "(idx_y1 >= 0) ? AnalysisFCChh::hasHiggsParent(Particle.at(RP2MC_index[idx_y1]), _Particle_parents, Particle) : false")
            .Define("has_higgs_parent_y2", "(idx_y2 >= 0) ? AnalysisFCChh::hasHiggsParent(Particle.at(RP2MC_index[idx_y2]), _Particle_parents, Particle) : false")       
            # get truth photons from Higgs
            .Define("HtoYY_truth_photons", "AnalysisFCChh::getPhotonsFromH(Particle, _Particle_parents)")
            .Define("HtoYY_truth_photons_TLV", "FCCAnalyses::MCParticle::get_tlv(HtoYY_truth_photons)")
            .Define("HtoYY_n_truth_photons", "FCCAnalyses::MCParticle::get_n(HtoYY_truth_photons)")
            .Define("HtoYY_E_truth_photons", "FCCAnalyses::MCParticle::get_e(HtoYY_truth_photons)")
            .Define("HtoYY_pT_truth_photons", "FCCAnalyses::MCParticle::get_pt(HtoYY_truth_photons)")
            .Define("HtoYY_eta_truth_photons", "FCCAnalyses::MCParticle::get_eta(HtoYY_truth_photons)")
            .Define("HtoYY_phi_truth_photons", "FCCAnalyses::MCParticle::get_phi(HtoYY_truth_photons)")
            .Define("HtoYY_truth_E_y1", "(HtoYY_n_truth_photons > 0) ? HtoYY_E_truth_photons[0] : -999.")
            .Define("HtoYY_truth_pT_y1", "(HtoYY_n_truth_photons > 0) ? HtoYY_pT_truth_photons[0] : -999.")
            .Define("HtoYY_truth_eta_y1", "(HtoYY_n_truth_photons > 0) ? HtoYY_eta_truth_photons[0] : -999.")
            .Define("HtoYY_truth_phi_y1", "(HtoYY_n_truth_photons > 0) ? HtoYY_phi_truth_photons[0] : -999.")
            .Define("HtoYY_truth_E_y2", "(HtoYY_n_truth_photons > 1) ? HtoYY_E_truth_photons[1] : -999.")
            .Define("HtoYY_truth_pT_y2", "(HtoYY_n_truth_photons > 1) ? HtoYY_pT_truth_photons[1] : -999.")
            .Define("HtoYY_truth_eta_y2", "(HtoYY_n_truth_photons > 1) ? HtoYY_eta_truth_photons[1] : -999.")
            .Define("HtoYY_truth_phi_y2", "(HtoYY_n_truth_photons > 1) ? HtoYY_phi_truth_photons[1] : -999.")
            .Define("HtoYY_truth_m_yy", "(HtoYY_n_truth_photons > 1) ? (HtoYY_truth_photons_TLV[0] + HtoYY_truth_photons_TLV[1]).M() : -999.")  
            # TLV test for myy resolution
            .Define("TLV_y1", "(n_photons > 0) ? AnalysisFCChh::getTLV(E_y1/TMath::CosH(true_eta_y1), true_eta_y1, true_phi_y1, E_y1) : TLorentzVector(0.,0.,0.,0.)")
            .Define("TLV_y2", "(n_photons > 1) ? AnalysisFCChh::getTLV(E_y2/TMath::CosH(true_eta_y2), true_eta_y2, true_phi_y2, E_y2) : TLorentzVector(0.,0.,0.,0.)")
            .Define("test_m_yy", "(n_photons > 1) ? (TLV_y1 + TLV_y2).M() : -999.")
            .Define("test_pT_yy", "(n_photons > 1) ? (TLV_y1 + TLV_y2).Pt() : -999.")
            .Define("test_theta_y_y", "(n_photons > 1) ? TLV_y1.Vect().Angle(TLV_y2.Vect()) : -999.")
            .Define("test_cos_theta_y_y", "(n_photons > 1) ? TMath::Cos(test_theta_y_y) : -999.")
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

            ########################################### LEPTONS ########################################### 
            .Define("idx_leptons",  "AnalysisFCChh::concatenate(Muon_objIdx.index, Electron_objIdx.index)")
            .Define("leptons", "FCCAnalyses::ReconstructedParticle::get(idx_leptons, ReconstructedParticles)") 
            .Define("n_all_leptons",  "FCCAnalyses::ReconstructedParticle::get_n(leptons)")
            .Define("E_leptons",  "FCCAnalyses::ReconstructedParticle::get_e(leptons)")
            .Define("pT_leptons",  "FCCAnalyses::ReconstructedParticle::get_pt(leptons)")
            .Define("eta_leptons",  "FCCAnalyses::ReconstructedParticle::get_eta(leptons)")
            .Define("phi_leptons",  "FCCAnalyses::ReconstructedParticle::get_phi(leptons)")
            # ll object
            .Define("ll_pairs_unmerged", "AnalysisFCChh::getPairs(leptons)") # retrieves the leading pT pair of all possible 
            .Define("ll_pairs", "AnalysisFCChh::merge_pairs(ll_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_ll", "FCCAnalyses::ReconstructedParticle::get_mass(ll_pairs)")
            # select electrons at 15 GeV
            .Define("sel_leptons", "FCCAnalyses::ReconstructedParticle::sel_pt(15.)(leptons)")
            .Define("n_leptons",  "FCCAnalyses::ReconstructedParticle::get_n(sel_leptons)")
            # first two electrons
            # leading electron
            .Define("E_l1", "(n_leptons > 0) ? E_leptons[0] : -999.")
            .Define("pT_l1", "(n_leptons > 0) ? pT_leptons[0] : -999.")
            .Define("eta_l1", "(n_leptons > 0) ? eta_leptons[0] : -999.")
            .Define("phi_l1", "(n_leptons > 0) ? phi_leptons[0] : -999.")
            # subleading electron
            .Define("E_l2", "(n_leptons > 1) ? E_leptons[1] : -999.")
            .Define("pT_l2", "(n_leptons > 1) ? pT_leptons[1] : -999.")
            .Define("eta_l2", "(n_leptons > 1) ? eta_leptons[1] : -999.")
            .Define("phi_l2", "(n_leptons > 1) ? phi_leptons[1] : -999.")
            # delta R between photons and leptons
            .Define("DR_y1_l1", "(n_photons > 0 && n_leptons > 0) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_leptons[0])) : -999.")
            .Define("DR_y1_l2", "(n_photons > 0 && n_leptons > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_leptons[1])) : -999.")
            .Define("DR_y2_l1", "(n_photons > 1 && n_leptons > 0) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_leptons[0])) : -999.")
            .Define("DR_y2_l2", "(n_photons > 1 && n_leptons > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_leptons[1])) : -999.")
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
            .Define("pass_loose_btag_jets", "AnalysisFCChh::get_pass_tag(Jet, idx_sel_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("pass_medium_btag_jets", "AnalysisFCChh::get_pass_tag(Jet, idx_sel_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("pass_tight_btag_jets", "AnalysisFCChh::get_pass_tag(Jet, idx_sel_jets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 2)") #bit 2 = tight WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
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
            .Define("pass_loose_btag_bjets", "AnalysisFCChh::get_pass_tag(Jet, idx_sel_bjets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)")
            .Define("pass_medium_btag_bjets", "AnalysisFCChh::get_pass_tag(Jet, idx_sel_bjets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") 
            .Define("pass_tight_btag_bjets", "AnalysisFCChh::get_pass_tag(Jet, idx_sel_bjets, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 2)") 
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
            # delta R between photons and jets
            .Define("DR_y1_j1", "(n_photons > 0 && n_jets > 0) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_jets[0])) : -999.")
            .Define("DR_y1_j2", "(n_photons > 0 && n_jets > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_jets[1])) : -999.")
            .Define("DR_y2_j1", "(n_photons > 1 && n_jets > 0) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_jets[0])) : -999.")
            .Define("DR_y2_j2", "(n_photons > 1 && n_jets > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_jets[1])) : -999.")
            # delta R between photons and b-jets
            .Define("DR_y1_b1", "(n_photons > 0 && n_bjets > 0) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_bjets[0])) : -999.")
            .Define("DR_y1_b2", "(n_photons > 0 && n_bjets > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_bjets[1])) : -999.")
            .Define("DR_y2_b1", "(n_photons > 1 && n_bjets > 0) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_bjets[0])) : -999.")
            .Define("DR_y2_b2", "(n_photons > 1 && n_bjets > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_gamma[1]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_bjets[1])) : -999.")
            # delta R between the two b-jets
            .Define("DR_b_b", "(n_bjets > 1) ? FCCAnalyses::ReconstructedParticle::get_tlv(sel_bjets[0]).DeltaR(FCCAnalyses::ReconstructedParticle::get_tlv(sel_bjets[1])) : -999.")
            ########################################### MET ########################################### 
            .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
            .Define("MET_x", "FCCAnalyses::ReconstructedParticle::get_px(MissingET)")
            .Define("MET_y", "FCCAnalyses::ReconstructedParticle::get_py(MissingET)")
            .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")
            ########################################### TRUTH HIGGS  ########################################### 
            .Define("higgs",  "AnalysisFCChh::get_final_Higgs(Particle, _Particle_daughters)")
            .Define("n_higgs",  "FCCAnalyses::MCParticle::get_n(higgs)")
            .Define("pT_higgs",  "FCCAnalyses::MCParticle::get_pt(higgs)")
            .Define("E_higgs",  "FCCAnalyses::MCParticle::get_e(higgs)")
            .Define("eta_higgs",  "FCCAnalyses::MCParticle::get_eta(higgs)")
            .Define("phi_higgs",  "FCCAnalyses::MCParticle::get_phi(higgs)")
            .Define("rapidity_higgs",  "FCCAnalyses::MCParticle::get_y(higgs)")
            .Define("higgs_decay_type",  "AnalysisFCChh::findHiggsDecayChannel(Particle, _Particle_daughters)")
            .Define("higgs_children",  "(n_higgs > 0) ? AnalysisFCChh::get_immediate_children(higgs.at(0), Particle, _Particle_daughters) : ROOT::VecOps::RVec<edm4hep::MCParticleData>()")
            .Define("n_higgs_children",  "FCCAnalyses::MCParticle::get_n(higgs_children)")
            .Define("higgs_child_pdgId",  "FCCAnalyses::MCParticle::get_pdg(higgs_children)")
            .Define("higgs_child1_pdgId",  "(n_higgs_children > 0) ? higgs_child_pdgId[0] : -999")
            .Define("higgs_child2_pdgId",  "(n_higgs_children > 1) ? higgs_child_pdgId[1] : -999")
            ########################################### TRUTH TOP  ########################################### 
            .Define("tops",  "AnalysisFCChh::get_final_top(Particle, _Particle_daughters)")
            .Define("n_tops",  "FCCAnalyses::MCParticle::get_n(tops)")
            .Define("pT_tops",  "FCCAnalyses::MCParticle::get_pt(tops)")
            .Define("E_tops",  "FCCAnalyses::MCParticle::get_e(tops)")
            .Define("eta_tops",  "FCCAnalyses::MCParticle::get_eta(tops)")
            .Define("phi_tops",  "FCCAnalyses::MCParticle::get_phi(tops)")
            .Define("rapidity_tops",  "FCCAnalyses::MCParticle::get_y(tops)")
            .Define("E_top1", "(n_tops > 0) ? E_tops[0] : -999.")
            .Define("pT_top1", "(n_tops > 0) ? pT_tops[0] : -999.")
            .Define("eta_top1", "(n_tops > 0) ? eta_tops[0] : -999.")
            .Define("phi_top1", "(n_tops > 0) ? phi_tops[0] : -999.")
            .Define("rapidity_top1", "(n_tops > 0) ? rapidity_tops[0] : -999.")
            .Define("E_top2", "(n_tops > 1) ? E_tops[1] : -999.")
            .Define("pT_top2", "(n_tops > 1) ? pT_tops[1] : -999.")
            .Define("eta_top2", "(n_tops > 1) ? eta_tops[1] : -999.")
            .Define("phi_top2", "(n_tops > 1) ? phi_tops[1] : -999.")
            .Define("rapidity_top2", "(n_tops > 1) ? rapidity_tops[1] : -999.")
            ########################################### TRUTH PHOTONS ########################################### 
            .Define("truth_photons", "AnalysisFCChh::get_final_photons(Particle)")
            # diphoton pair
            .Define("truth_yy_pairs_unmerged", "AnalysisFCChh::getPairs(truth_photons)") # retrieves the leading pT pair of all possible 
            .Define("truth_yy_pairs", "AnalysisFCChh::merge_pairs(truth_yy_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("truth_m_yy", "FCCAnalyses::MCParticle::get_mass(truth_yy_pairs)")
            # truth photons
            .Define("n_truth_photons",  "FCCAnalyses::MCParticle::get_n(truth_photons)")
            .Define("E_truth_photons",  "FCCAnalyses::MCParticle::get_e(truth_photons)")
            .Define("pT_truth_photons",  "FCCAnalyses::MCParticle::get_pt(truth_photons)")
            .Define("eta_truth_photons",  "FCCAnalyses::MCParticle::get_eta(truth_photons)")
            .Define("phi_truth_photons",  "FCCAnalyses::MCParticle::get_phi(truth_photons)")
            .Define("E_truth_y1", "(n_truth_photons > 0) ? E_truth_photons[0] : -999.")
            .Define("pT_truth_y1", "(n_truth_photons > 0) ? pT_truth_photons[0] : -999.")
            .Define("eta_truth_y1", "(n_truth_photons > 0) ? eta_truth_photons[0] : -999.")
            .Define("phi_truth_y1", "(n_truth_photons > 0) ? phi_truth_photons[0] : -999.")
            .Define("E_truth_y2", "(n_truth_photons > 1) ? E_truth_photons[1] : -999.")
            .Define("pT_truth_y2", "(n_truth_photons > 1) ? pT_truth_photons[1] : -999.")
            .Define("eta_truth_y2", "(n_truth_photons > 1) ? eta_truth_photons[1] : -999.")
            .Define("phi_truth_y2", "(n_truth_photons > 1) ? phi_truth_photons[1] : -999.")
            ########################################### APPLY PRE-SELECTION ########################################### 
            # require H->yy decay for signal sample
#            .Filter("higgs_decay_type==7")
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
            "E_y1", "pT_y1", "eta_y1", "phi_y1", "rel_pT_y1", "idx_y1", "has_higgs_parent_y1",
            "E_y2", "pT_y2", "eta_y2", "phi_y2", "rel_pT_y2", "idx_y2", "has_higgs_parent_y2",
            "DR_y_y",  
            'theta_y_y', 'cos_theta_y_y',
            "DR_y1_b1", "DR_y1_b2", "DR_y1_j1", "DR_y1_j2",
            "DR_y2_b1", "DR_y2_b2", "DR_y2_j1", "DR_y2_j2",
            "DR_y1_l1", "DR_y1_l2", "DR_y2_l1", "DR_y2_l2",
            "DR_b_b",
            # reco-to-truth association for photons
            "true_E_y1", "true_pT_y1", "true_eta_y1", "true_phi_y1",
            "true_E_y2", "true_pT_y2", "true_eta_y2", "true_phi_y2",
            "pdgID_y1", "pdgID_y2",
            "true_m_yy", 'true_pT_yy', 'true_DR_y_y',
            'true_theta_y_y', 'true_cos_theta_y_y',
            # truth photons from Higgs
             "HtoYY_n_truth_photons", "HtoYY_truth_m_yy",
             "HtoYY_E_truth_photons", "HtoYY_pT_truth_photons", "HtoYY_eta_truth_photons", "HtoYY_phi_truth_photons",
             "HtoYY_truth_E_y1", "HtoYY_truth_pT_y1", "HtoYY_truth_eta_y1", "HtoYY_truth_phi_y1",
             "HtoYY_truth_E_y2", "HtoYY_truth_pT_y2", "HtoYY_truth_eta_y2", "HtoYY_truth_phi_y2",
            # test for the myy resolution
             "test_m_yy", "test_theta_y_y", "test_pT_yy", "test_cos_theta_y_y",
            # Leptons
            'n_electrons', 'n_all_electrons', 'E_electrons', 'pT_electrons', 'eta_electrons', 'phi_electrons', 
            "m_ee",
            "E_e1", "pT_e1", "eta_e1", "phi_e1",
            "E_e2", "pT_e2", "eta_e2", "phi_e2",
            'n_muons', 'n_all_muons', 'E_muons', 'pT_muons', 'eta_muons', 'phi_muons',
            "m_mumu",
            "E_mu1", "pT_mu1", "eta_mu1", "phi_mu1",
            "E_mu2", "pT_mu2", "eta_mu2", "phi_mu2",
            "n_leptons", "n_all_leptons", "E_leptons", "pT_leptons", "eta_leptons", "phi_leptons",
            "m_ll",
            "E_l1", "pT_l1", "eta_l1", "phi_l1",
            "E_l2", "pT_l2", "eta_l2", "phi_l2",
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
            'MET', 'MET_x', 'MET_y', 'MET_phi',
            # truth Higgs
            'n_higgs', 'E_higgs', 'pT_higgs', 'eta_higgs', 'phi_higgs', 'rapidity_higgs',
            "higgs_decay_type", "n_higgs_children", 
            "higgs_child_pdgId", "higgs_child1_pdgId", "higgs_child2_pdgId",
            # truth top
            'n_tops', 'E_tops', 'pT_tops', 'eta_tops', 'phi_tops', 'rapidity_tops',
            'E_top1', 'pT_top1', 'eta_top1', 'phi_top1',
            'E_top2', 'pT_top2', 'eta_top2', 'phi_top2',
            # truth photons
            'n_truth_photons', #'E_truth_photons', 'pT_truth_photons', 'eta_truth_photons', 'phi_truth_photons',
            'truth_m_yy',
            'E_truth_y1', 'pT_truth_y1', 'eta_truth_y1', 'phi_truth_y1',
            'E_truth_y2', 'pT_truth_y2', 'eta_truth_y2', 'phi_truth_y2',
        ]
        return branch_list