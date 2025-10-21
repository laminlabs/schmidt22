import lamindb as ln
import bionty as bt


def main():
    ln.track(project="Schmidt22")

    biosample_type = ln.Record(
        name="Biosample", description="A biological sample", is_type=True
    ).save()
    experiment_type = ln.Record(
        name="Experiment", description="An experiment", is_type=True
    ).save()

    ln.Feature(
        name="biosample",
        dtype=biosample_type,
    ).save()
    ln.Feature(
        name="experiment",
        dtype=experiment_type,
    ).save()
    ln.Feature(
        name="assays_efo",
        dtype=list[bt.ExperimentalFactor],
        description="EFO term describing an assay",
    ).save()
    ln.Feature(
        name="readouts_efo",
        dtype=list[bt.ExperimentalFactor],
        description="EFO term describing a readout",
    ).save()

    ln.finish()
