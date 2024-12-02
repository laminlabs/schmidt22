import lamindb as ln
import bionty as bt

# track the current python script
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
ln.track("J5ZTmVxSch3U5zKv", params={"project": "schmidt22"})
# label the transform
ulabel1 = ln.ULabel.get(name="use-case")
ulabel2 = ln.ULabel.get(name="schmidt22")
ln.context.transform.ulabels.add(ulabel1, ulabel2)

# label with instrument
features = ln.Feature.lookup()
novaseq6000 = bt.ExperimentalFactor.get(name="Illumina NovaSeq 6000")
efo_10x = bt.ExperimentalFactor.get(name="10X 3' v1")
exp001 = ln.ULabel.get(name="EXP002")
s001 = ln.ULabel.get(name="S001")

# register output files of the sequencer
raw_files = [
    "s3://lamindata/fastq/schmidt22_perturbseq_R1_001.fastq.gz",
    "s3://lamindata/fastq/schmidt22_perturbseq_R2_001.fastq.gz",
]
for raw_file in raw_files:
    artifact = ln.Artifact(raw_file).save()
    artifact.labels.add(novaseq6000, feature=features.instrument)
    artifact.labels.add(efo_10x, feature=features.technology)
    artifact.labels.add(exp001, feature=features.experiment)
    artifact.labels.add(s001, feature=features.biosample)

ln.finish()
