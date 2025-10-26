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
    # we need the gene ontology
    bt.Gene.import_source()
    # features for curating the screen results
    schmidt22_features = ln.Feature(
        name="Schmidt22",
        is_type=True,
        description="Features from Schmidt et al. 2022, Genome-wide CRISPRa screen with IFN-gamma readout in melanoma cells",
    ).save()
    target_gene_symbol = ln.Feature(
        name="target_gene_symbol",
        dtype=bt.Gene.symbol,
        type=schmidt22_features,
        description="Target gene of CRISPRa experiment",
    ).save()
    target_gene_ensembl_id = ln.Feature(
        name="target_gene_ensembl_id",
        dtype=bt.Gene.ensembl_gene_id,
        type=schmidt22_features,
        description="Target gene of CRISPRa experiment",
    ).save()
    crispr_ifng_p_value_neg = ln.Feature(
        name="crispr_ifng_p_value_neg",
        dtype=float,
        type=schmidt22_features,
        description="Negative CRISPR IFN-gamma p-value",
    ).save()
    crispr_ifng_p_value_pos = ln.Feature(
        name="crispr_ifng_p_value_pos",
        dtype=float,
        type=schmidt22_features,
        description="Positive CRISPR IFN-gamma p-value",
    ).save()
    # define schema for the screen results
    schmidt22_schemas = ln.Schema(
        name="Schmidt22",
        is_type=True,
        description="Schemas from Schmidt et al. 2022, Genome-wide CRISPRa screen with IFN-gamma readout in melanoma cells",
    ).save()
    schema = ln.Schema(
        name="GWS_CRISPRa_IFN-gamma_readout",
        features=[
            target_gene_symbol,
            target_gene_ensembl_id,
            crispr_ifng_p_value_neg,
            crispr_ifng_p_value_pos,
        ],
        type=schmidt22_schemas,
        description="Genome-wide CRISPRa screen with IFN-gamma readout in melanoma cells",
    ).save()
    schema.describe()
    # define feature for the scRNA analysis
    schmidt22_type = ln.Record(name="Schmidt22", is_type=True).save()
    cell_state_type = ln.Record(
        name="CellState", is_type=True, type=schmidt22_type
    ).save()
    for cell_state in [
        "IFNG High 1",
        "Negative Regulators",
        "Th2",
        "IL22 High",
        "Proliferative (S)",
        "Proliferative (G2/M)",
        "TNF Locus High",
        "GNLY High",
        "CCL3/4 High, IFNG Low",
        "CD8 Common",
        "EMP1 Guides",
        "IFNG High 2",
        "IL2 High 1",
        "CD4 Common",
        "IL2 High 2",
    ]:
        ln.Record(name=cell_state, type=cell_state_type).save()
    ln.Feature(
        name="scrna_cell_state", dtype=cell_state_type, type=schmidt22_features
    ).save()
    # target metric of joint scRNA & screen analysis
    ln.Feature(
        name="enrichment_score_for_screen_results", dtype=float, type=schmidt22_features
    ).save()
    # finish the script
    ln.finish()


if __name__ == "__main__":
    main()
