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
    # define generic features
    ln.Feature(name="biosample", dtype=biosample_type).save()
    ln.Feature(name="experiment", dtype=experiment_type).save()
    ln.Feature(name="assays_efo", dtype=list[bt.ExperimentalFactor]).save()
    ln.Feature(name="readouts_efo", dtype=list[bt.ExperimentalFactor]).save()
    ln.Feature(name="s3_folder", dtype=str).save()
    ln.Feature(name="library_preparation", dtype=bt.ExperimentalFactor).save()
    ln.Feature(name="technology", dtype=bt.ExperimentalFactor).save()
    ln.Feature(name="instrument", dtype=bt.ExperimentalFactor).save()
    ln.Feature(name="original_publication", dtype=ln.Reference.abbr).save()
    # create labels for samples and experiments
    ln.Record(name="Schmidt22-S001", type=biosample_type).save()
    ln.Record(name="Schmidt22-EXP001", type=experiment_type).save()
    ln.Record(name="Schmidt22-EXP002", type=experiment_type).save()
    # create labels for instrument, technology, library preparation
    bt.ExperimentalFactor.from_values(
        [
            "Illumina NovaSeq 6000",
            "Perturb-Seq",
            "gRNA-seq",
            "10x 3' v2",
            "interferon gamma",
        ]
    ).save()
    # create the reference
    ln.Reference(
        abbr="Schmidt22",
        name="CRISPR activation and interference screens decode stimulation responses in primary human T cells",
        pubmed_id=35113687,
        text="Regulation of cytokine production in stimulated T cells can be disrupted in autoimmunity, immunodeficiencies, and cancer. Systematic discovery of stimulation-dependent cytokine regulators requires both loss-of-function and gain-of-function studies, which have been challenging in primary human cells. We now report genome-wide CRISPR activation (CRISPRa) and interference (CRISPRi) screens in primary human T cells to identify gene networks controlling interleukin-2 (IL-2) and interferon-γ (IFN-γ) production. Arrayed CRISPRa confirmed key hits and enabled multiplexed secretome characterization, revealing reshaped cytokine responses. Coupling CRISPRa screening with single-cell RNA sequencing enabled deep molecular characterization of screen hits, revealing how perturbations tuned T cell activation and promoted cell states characterized by distinct cytokine expression profiles. These screens reveal genes that reprogram critical immune cell functions, which could inform the design of immunotherapies.",
    ).save()
    # create features for cell ranger run
    ln.Feature(name="transcriptome_link", dtype=str).save()
    # finish the script
    ln.finish()


if __name__ == "__main__":
    main()
