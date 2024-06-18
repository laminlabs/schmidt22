import lamindb as ln
import bionty as bt

# Post-process 3 cellranger output files
ln.settings.transform.stem_uid = "piG5scNASXcc"
ln.settings.transform.version = "2"
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
ln.track()

output_artifacts = ln.Artifact.filter(
    key__startswith="schmidt22_perturbseq/filtered_feature_bc_matrix"
).all()
input_artifacts = [f.cache() for f in output_artifacts]
output_path = ln.core.datasets.schmidt22_perturbseq(basedir=ln.settings.storage)
output_file = ln.Artifact(output_path, description="perturbseq counts")
output_file.save()

efo = bt.ExperimentalFactor.lookup()
features = ln.Feature.lookup()

output_file.labels.add(efo.perturb_seq, features.assay)
output_file.labels.add(efo.single_cell_rna_sequencing, features.readout)

is_experiment = ln.ULabel.filter(name="is_experiment").one()
is_biosample = ln.ULabel.filter(name="is_biosample").one()
exp2 = is_experiment.children.filter(description__contains="Perturb-seq").one()
biosample = is_biosample.children.get(name="S001")
output_file.labels.add(exp2, features.experiment)
output_file.labels.add(biosample, features.biosample)

ln.finish()
