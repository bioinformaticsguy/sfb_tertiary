"""
Configuration file containing all variables and settings
"""

import os

# File paths 
OUTPUT_DIR = "/data/humangen_kircherlab/Users/hassan/sfb_tertiary/output/csv_files"
RESULTS_PATH = "/data/humangen_kircherlab/Users/hassan/run_rare/rare-disease-pipeline/outputs/sample_sheet_30_demultiplexed"
CSV_FILE_PATH = "/data/humangen_kircherlab/Users/hassan/run_rare/rare-disease-pipeline/samplesheets/old_sample_sheets/sample_sheet_30_demultiplexed.csv"

# Analysis parameters
TARGET_COVERAGE = 24

# Samples to exclude from analysis
SAMPLES_TO_EXCLUDE = ['hugelymodelbat', 'A4842_DNA_42']

# File naming patterns
MARK_DUPLICATES_PATTERN = "{sample}_sorted_md.MarkDuplicates.metrics.txt"
ALIGNMENT_SUMMARY_PATTERN = "{sample}_multiplemetrics.CollectMultipleMetrics.alignment_summary_metrics"
MOSDEPTH_SUMMARY_PATTERN = "{sample}_mosdepth.mosdepth.summary.txt"

# Output file names
OUTPUT_CSV_FILE = "sample_metrics_summary.csv"
OUTPUT_EXCEL_FILE = "sample_metrics_summary.xlsx"

# Column metadata for Excel documentation
COLUMN_METADATA = {
    'Column Name': [
        'sample_name',
        'total_reads', 
        'aligned_reads',
        'mean_coverage',
        'percent_duplication',
        'saturation_fraction', 
        'additional_reads'
    ],
    'Description': [
        'Sample identifier/name',
        'Total number of sequencing reads generated for this sample',
        'Number of reads that successfully aligned to the reference genome',
        'Average sequencing depth/coverage across the genome',
        'Percentage of reads identified as PCR duplicates',
        'Library saturation metric (1 - percent_duplication), indicates sequencing efficiency',
        'Additional reads needed to reach target coverage (30x), adjusted for duplication rate'
    ],
    'Units/Format': [
        'Text',
        'Number (M = millions)',
        'Number (M = millions)',
        'Fold coverage (e.g., 25.5x)',
        'Percentage (e.g., 24.5%)',
        'Decimal fraction (0.000-1.000)',
        'Number of reads (M = millions)'
    ]
}

CALCULATIONS_INFO = {
    'Calculation': [
        'Saturation Fraction',
        'Additional Reads Needed',
    ],
    'Formula': [
        'saturation_fraction = 1 - percent_duplication',
        'additional_reads = (current_reads × (target_coverage - current_coverage) / current_coverage) / saturation_fraction',

    ]
}