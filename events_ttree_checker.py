import ROOT
import glob
import os

directory = "/eos/home-o/oarakji/tth/myRoot/fcc_v07/II/mgp8_pp_vbf_h01j_5f_50TeV"
pattern = os.path.join(directory, "events_*.root")
files = glob.glob(pattern)

if not files:
    print("No matching root files found.")
    exit(1)

print("Checking root files for 'events' TTree...")
for fname in files:
    try:
        f = ROOT.TFile.Open(fname)
        if not f or f.IsZombie():
            print(f"{fname}: Could not open")
            continue
        obj = f.Get("events")  # lowercase
        has_tree = obj and obj.InheritsFrom("TTree")
        f.Close()
        print(f"{fname}: {'YES' if has_tree else 'NO'}")
    except Exception as e:
        print(f"{fname}: Error - {e}")