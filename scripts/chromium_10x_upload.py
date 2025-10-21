#!/usr/bin/env python3
"""Register FASTQ files from S3 with metadata annotations.

Example usage:
    python register_fastq.py \
        --s3-folder s3://lamindata/fastq \
        --experiment EXP002 \
        --biosample S001 \
        --project Schmidt22
"""

import argparse
import lamindb as ln


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3-folder", required=True)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--biosample", required=True)
    parser.add_argument("--project", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    ln.track(
        "J5ZTmVxSch3U",
        project=args.project,
        features={
            "s3_folder": args.s3_folder,
            "experiment_record": args.experiment,
            "biosample_record": args.biosample,
        },
    )
    raw_files = list(ln.UPath(args.s3_folder).glob("*.fastq.gz"))
    for raw_file in raw_files:
        ln.Artifact(
            raw_file,
            features={
                "instrument": "Illumina NovaSeq 6000",
                "technology": "Perturb-Seq",
                "library_preparation": "10x 3' v2",
                "experiment_record": args.experiment,
                "biosample_record": args.biosample,
            },
        ).save()
    print(f"registered {len(raw_files)} artifacts")
    ln.finish()


if __name__ == "__main__":
    main()
