#!/usr/bin/env python3
"""Post-process Cell Ranger output files.

Example usage:
    python post_process_cellranger.py \
        --experiment "Schmidt22 EXP002" \
        --biosample "Schmidt22 S001" \
        --project Schmidt22 \
        --dry-run
"""

import argparse
import lamindb as ln
import scanpy as sc
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--biosample", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip scanpy processing, only process LaminDB",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    ln.track(
        "piG5scNASXcc",
        project=args.project,
        features={
            "experiment": args.experiment,
            "biosample": args.biosample,
        },
    )

    identifier = (
        f"{args.experiment.replace(' ', '_')}_{args.biosample.replace(' ', '_')}"
    )

    # get inputs
    matrix_artifact = (
        ln.Artifact.filter(key__endswith="filtered_feature_bc_matrix", suffix=".h5")
        .filter(experiment=args.experiment, biosample=args.biosample)
        .one()
    )

    if not args.dry_run:
        adata = sc.read_10x_h5(
            matrix_artifact.cache() / "filtered_feature_bc_matrix.h5"
        )
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)
        output_path = Path(f"./processed_{identifier}.h5ad")
        adata.write(output_path)
    else:
        output_path = "s3://lamindata/schmidt22_perturbseq/schmidt22_perturbseq.h5ad"

    # register/upload outputs
    ln.Artifact(
        output_path,
        key="schmidt22_perturbseq/schmidt22_perturbseq.h5ad",
        description=f"Processed counts for {args.experiment} {args.biosample}",
        features={
            "experiment": args.experiment,
            "biosample": args.biosample,
        },
    ).save()

    print(f"✓ registered: {output_path}")
    ln.finish()


if __name__ == "__main__":
    main()
