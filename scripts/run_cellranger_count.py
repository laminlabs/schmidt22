#!/usr/bin/env python3
"""Run Cell Ranger pipeline on FASTQ files from LaminDB.

Example usage:
    python run_cellranger.py \
        --experiment "Schmidt22 EXP002" \
        --biosample "Schmidt22 S001" \
        --project Schmidt22 \
        --dry-run
"""

import argparse
import lamindb as ln
import subprocess as sp
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--biosample", required=True)
    parser.add_argument(
        "--transcriptome",
        default="https://cf.10xgenomics.com/supp/cell-exp/refdata-gex-GRCh38-2020-A.tar.gz",
    )
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip Cell Ranger execution, only process LaminDB",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    ln.track(
        project=args.project,
        features={
            "transcriptome_link": args.transcriptome,
            "experiment": args.experiment,
            "biosample": args.biosample,
        },
    )
    identifier = (
        f"{args.experiment.replace(' ', '_')}_{args.biosample.replace(' ', '_')}"
    )

    # Get input files
    input_artifacts = (
        ln.Artifact.filter(suffix=".fastq.gz")
        .filter(experiment=args.experiment, biosample=args.biosample)
        .all()
    )
    assert input_artifacts, f"no FASTQ files found with prefix '{args.fastq_prefix}'"
    print(f"found {len(input_artifacts)} FASTQ files")

    fastq_dir = Path(f"./fastq_input_{identifier}")
    fastq_dir.mkdir(exist_ok=True)
    for artifact in input_artifacts:
        cached_path = Path(artifact.cache())
        # only needed in case fastqs are in different directories
        (fastq_dir / cached_path.name).symlink_to(cached_path)
    output_dir = Path(f"./outputs_{identifier}")

    # register transcriptome
    transcriptome_artifact = ln.Artifact(args.transcriptome).save()

    # run cell ranger count
    if not args.dry_run:
        cmd = [
            "cellranger",
            "count",
            f"--id={output_dir.as_posix()}",
            # below will download 10.6GB for the transcriptome file only once
            f"--transcriptome={transcriptome_artifact.cache()}",
            f"--fastqs={fastq_dir}",
        ]
        print(f"running: {' '.join(cmd)}")
        sp.run(cmd, check=True)

    # register/upload outputs
    outputs = [
        "filtered_feature_bc_matrix",
        "web_summary.html",
        "metrics_summary.csv",
        "molecule_info.h5",
    ]
    if not args.dry_run:
        for output in outputs:
            path = output_dir / "outs" / output
            if not path.exists():
                continue
            ln.Artifact(path, key=f"cell_ranger/{identifier}/count/{output}").save()
            print(f"✓ registered: {output}")
    else:
        ln.Artifact(
            "s3://lamindata/schmidt22_perturbseq/filtered_feature_bc_matrix"
        ).save()

    ln.finish()


if __name__ == "__main__":
    main()
