import lamindb as ln

ln.settings.transform.stem_uid = "J5ZTmVxSch3U"
ln.settings.transform.version = "2"
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
ln.track()

# register output files of the sequencer
upload_dir = ln.core.datasets.dir_scrnaseq_cellranger(
    "perturbseq", basedir=ln.settings.storage, output_only=False
)
ln.Artifact(
    upload_dir.parent / "fastq/perturbseq_R1_001.fastq.gz",
    key="fastq/schmidt22_perturbseq_R1_001.fastq.gz",
).save()
ln.Artifact(
    upload_dir.parent / "fastq/perturbseq_R2_001.fastq.gz",
    key="fastq/schmidt22_perturbseq_R2_001.fastq.gz",
).save()

ln.finish()
