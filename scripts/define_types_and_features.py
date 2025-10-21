import lamindb as ln
import bionty as bt


def main():
    # define project only a single time
    ln.Project(name="Schmidt22").save()
    # track this script
    ln.track("kiWfzmPCrof8", project="Schmidt22")
    # define types
    biosample_type = ln.Record(name="Biosample", is_type=True).save()
    experiment_type = ln.Record(name="Experiment", is_type=True).save()
    # define features
    ln.Feature(name="biosample", dtype=biosample_type).save()
    ln.Feature(name="experiment", dtype=experiment_type).save()
    ln.Feature(name="assays_efo", dtype=list[bt.ExperimentalFactor]).save()
    ln.Feature(name="readouts_efo", dtype=list[bt.ExperimentalFactor]).save()
    ln.Feature(name="s3_folder", dtype=str).save()
    # create labels for samples and experiments
    ln.Record(name="Schmidt22 S001", type=biosample_type).save()
    ln.Record(name="Schmidt22 EXP001", type=experiment_type).save()
    # finish the script
    ln.finish()


if __name__ == "__main__":
    main()
