import lamindb as ln

# Post-process 3 cellranger output files
ln.settings.sync_git_repo = "https://github.com/laminlabs/rnd-demo"
ln.track("piG5scNASXcc5zKv", params={"project": "schmidt22"})
# label the transform
ulabel1 = ln.ULabel.get(name="use-case")
ulabel2 = ln.ULabel.get(name="schmidt22")
ln.context.transform.ulabels.add(ulabel1, ulabel2)

# Download the input artifacts
input_artifacts = ln.Artifact.filter(
    key__startswith="schmidt22_perturbseq/filtered_feature_bc_matrix"
).all()
[f.cache() for f in input_artifacts]

# Register the output artifact
output_artifact = ln.Artifact(
    "s3://lamindata/schmidt22_perturbseq/schmidt22_perturbseq.h5ad",
    description="schmidt22 perturbseq counts",
)
output_artifact.save()

# Add labels to the output artifact
output_artifact.labels.add_from(input_artifacts[0])
output_artifact.features._add_from(input_artifacts[0])

ln.finish()
