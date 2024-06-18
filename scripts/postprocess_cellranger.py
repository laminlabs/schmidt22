import bionty as bt
import lamindb as ln

# Post-process 3 cellranger output files
ln.settings.transform.stem_uid = "piG5scNASXcc"
ln.settings.transform.version = "1"
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
run = ln.track(params={"project": "schmidt22"})
# label the transform
ulabel1 = ln.ULabel(name="use-case").save()
ulabel2 = ln.ULabel(name="schmidt22").save()
run.transform.ulabels.add(ulabel1, ulabel2)

# Download the input artifacts
input_artifacts = ln.Artifact.filter(
    key__startswith="schmidt22_perturbseq/filtered_feature_bc_matrix"
).all()
[f.cache() for f in input_artifacts]

# Register the output artifact
output_artifact = ln.Artifact(
    "s3://lamindata/schmidt22_perturbseq/schmidt22_perturbseq.h5ad",
    description="perturbseq counts",
)
output_artifact.save()

# Add labels to the output artifact
efo = bt.ExperimentalFactor.lookup()
features = ln.Feature.lookup()
output_artifact.labels.add(efo.perturb_seq, features.assay)
output_artifact.labels.add(efo.single_cell_rna_sequencing, features.readout)
is_experiment = ln.ULabel.filter(name="is_experiment").one()
is_biosample = ln.ULabel.filter(name="is_biosample").one()
exp2 = is_experiment.children.filter(description__contains="Perturb-seq").one()
biosample = is_biosample.children.get(name="S001")
output_artifact.labels.add(exp2, features.experiment)
output_artifact.labels.add(biosample, features.biosample)

ln.finish()
