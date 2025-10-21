#!/usr/bin/env python3
"""Run Cell Ranger pipeline on FASTQ files from LaminDB.

Example usage:
    python run_cellranger.py \
        --fastq-prefix fastq/perturbseq \
        --sample-id perturbseq_sample \
        --transcriptome refdata-gex-GRCh38-2020-A \
        --localcores 8 \
        --localmem 64
"""

import argparse
import lamindb as ln
import subprocess as sp
from pathlib import Path
import shutil


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Cell Ranger pipeline on FASTQ files from LaminDB"
    )
    parser.add_argument(
        "--fastq-prefix",
        required=True,
        help="Key prefix to filter FASTQ files (e.g., fastq/perturbseq)",
    )
    parser.add_argument(
        "--sample-id",
        default="perturbseq_sample",
        help="Sample ID for Cell Ranger output (default: perturbseq_sample)",
    )
    parser.add_argument(
        "--transcriptome",
        default="refdata-gex-GRCh38-2020-A",
        help="Path to Cell Ranger transcriptome reference (default: refdata-gex-GRCh38-2020-A)",
    )
    parser.add_argument(
        "--localcores",
        type=int,
        default=8,
        help="Number of cores for Cell Ranger to use (default: 8)",
    )
    parser.add_argument(
        "--localmem",
        type=int,
        default=64,
        help="Amount of memory in GB for Cell Ranger to use (default: 64)",
    )
    parser.add_argument(
        "--project",
        default="Schmidt22",
        help="Project name for tracking (default: Schmidt22)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Track the pipeline
    ln.track(
        transform=ln.Transform.get(key="Cell Ranger", version="7.2.0"),
        project=args.project,
    )

    # Configuration
    sample_id = args.sample_id
    transcriptome = args.transcriptome
    output_dir = Path(f"./{sample_id}")

    # Download input files and organize them for Cell Ranger
    print(f"Searching for FASTQ files with prefix: {args.fastq_prefix}")
    input_artifacts = ln.Artifact.filter(key__startswith=args.fastq_prefix).all()

    if not input_artifacts:
        raise ValueError(
            f"No FASTQ files found with key starting with '{args.fastq_prefix}'"
        )

    # Create a temporary directory for FASTQ files
    fastq_dir = Path("./fastq_input")
    fastq_dir.mkdir(exist_ok=True)

    # Download and symlink files to the fastq directory
    print(f"Downloading {len(input_artifacts)} FASTQ files...")
    for artifact in input_artifacts:
        cached_path = Path(artifact.cache())
        symlink_path = fastq_dir / cached_path.name
        if not symlink_path.exists():
            symlink_path.symlink_to(cached_path)
        print(f"  - {cached_path.name}")

    # Verify transcriptome exists
    if not Path(transcriptome).exists():
        raise FileNotFoundError(
            f"Transcriptome reference not found at {transcriptome}. "
            "Please download it using 'cellranger mkref' or provide correct path."
        )

    # Run Cell Ranger count
    print(f"\nRunning Cell Ranger count for sample: {sample_id}")
    cmd = [
        "cellranger",
        "count",
        f"--id={sample_id}",
        f"--transcriptome={transcriptome}",
        f"--fastqs={fastq_dir}",
        f"--localcores={args.localcores}",
        f"--localmem={args.localmem}",
    ]

    print(f"Command: {' '.join(cmd)}\n")

    try:
        sp.run(cmd, check=True)
    except sp.CalledProcessError as e:
        print(f"Cell Ranger failed with error: {e}")
        raise

    # Register output files
    print("\nRegistering output files...")

    # Register the filtered feature-barcode matrix
    filtered_matrix_dir = output_dir / "outs" / "filtered_feature_bc_matrix"
    if filtered_matrix_dir.exists():
        ln.Artifact(
            filtered_matrix_dir,
            key=f"cellranger/{sample_id}/filtered_feature_bc_matrix",
            description="Filtered feature-barcode matrix from Cell Ranger",
        ).save()
        print(f"✓ Registered filtered matrix: {filtered_matrix_dir}")

    # Register other important outputs
    important_files = [
        "outs/web_summary.html",
        "outs/metrics_summary.csv",
        "outs/molecule_info.h5",
        "outs/cloupe.cloupe",
    ]

    for file_path in important_files:
        full_path = output_dir / file_path
        if full_path.exists():
            ln.Artifact(
                full_path,
                key=f"cellranger/{sample_id}/{Path(file_path).name}",
                description=f"Cell Ranger output: {Path(file_path).name}",
            ).save()
            print(f"✓ Registered: {file_path}")

    # Clean up temporary FASTQ directory
    print("\nCleaning up temporary files...")
    shutil.rmtree(fastq_dir)

    print("\n✓ Cell Ranger pipeline completed successfully!")
    ln.finish()


if __name__ == "__main__":
    main()
