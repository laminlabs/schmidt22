import lamindb as ln
import bionty as bt


def main():
    ln.track(project="Schmidt22")

    biosample_type = ln.Record(name="Biosample", is_type=True).save()
    experiment_type = ln.Record(name="Experiment", is_type=True).save()

    ln.Feature(name="biosample", dtype=biosample_type).save()
    ln.Feature(name="experiment", dtype=experiment_type).save()
    ln.Feature(name="assays_efo", dtype=list[bt.ExperimentalFactor]).save()
    ln.Feature(name="readouts_efo", dtype=list[bt.ExperimentalFactor]).save()

    ln.finish()


if __name__ == "__main__":
    main()
