import lamindb as ln

# register the pipeline and track input/output artifacts
transform = ln.Transform.filter(name="Cell Ranger", version="9.0.0").one_or_none()
if transform is None:
    transform = ln.Transform(
        name="Cell Ranger",
        version="9.0.0",
        type="pipeline",
        reference="https://www.10xgenomics.com/support/software/cell-ranger/9.0",
    ).save()

ln.track(transform=transform, params={"project": "schmidt22"})
# access uploaded files as inputs for the pipeline
input_artifacts = ln.Artifact.filter(key__startswith="fastq/schmidt22_perturbseq").all()
input_paths = [artifact.cache() for artifact in input_artifacts]
# register output files
output_artifacts = ln.Artifact.from_dir(
    "s3://lamindata/schmidt22_perturbseq/filtered_feature_bc_matrix"
)
ln.save(output_artifacts)

for artifact in output_artifacts:
    artifact.labels.add_from(input_artifacts[0])
    artifact.features._add_from(input_artifacts[0])
