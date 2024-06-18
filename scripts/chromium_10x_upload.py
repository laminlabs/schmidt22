import lamindb as ln

# track the current python script
ln.settings.transform.stem_uid = "J5ZTmVxSch3U"
ln.settings.transform.version = "1"
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
run = ln.track(params={"project": "schmidt22"})
# label the transform
ulabel1 = ln.ULabel(name="use-case").save()
ulabel2 = ln.ULabel(name="schmidt22").save()
run.transform.ulabels.add(ulabel1, ulabel2)

# register output files of the sequencer
ln.Artifact("s3://lamindata/fastq/schmidt22_perturbseq_R1_001.fastq.gz").save()
ln.Artifact("s3://lamindata/fastq/schmidt22_perturbseq_R2_001.fastq.gz").save()

ln.finish()
