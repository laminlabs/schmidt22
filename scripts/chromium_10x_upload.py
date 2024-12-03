import bionty as bt
import lamindb as ln
import wetlab as wl

# track the current python script
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
ln.track("J5ZTmVxSch3U0002", params={"project": "schmidt22"})
# label the transform
ulabel1 = ln.ULabel.get(name="use-case")
ulabel2 = ln.ULabel.get(name="schmidt22")
ln.context.transform.ulabels.add(ulabel1, ulabel2)

# label with instrument
features = ln.Feature.lookup()
perturbseq = bt.ExperimentalFactor.get(name="Perturb-Seq")
novaseq6000 = bt.ExperimentalFactor.get(name="Illumina NovaSeq 6000")
exp001 = wl.Experiment.get(name="EXP002")
s001 = wl.Biosample.get(name="S001")

# register output files of the sequencer
raw_files = [
    "s3://lamindata/fastq/schmidt22_perturbseq_R1_001.fastq.gz",
    "s3://lamindata/fastq/schmidt22_perturbseq_R2_001.fastq.gz",
]
for raw_file in raw_files:
    artifact = ln.Artifact(raw_file).save()
    artifact.labels.add(novaseq6000, feature=features.instrument)
    artifact.labels.add(perturbseq, feature=features.technology)
    artifact.labels.add(exp001, feature=features.experiment)
    artifact.labels.add(s001, feature=features.biosample)

ln.finish()
