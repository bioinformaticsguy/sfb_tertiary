"""
Functions for processing sequencing metrics and generating reports
"""

import os
import pandas as pd
from curated_functions import parse_mark_duplicates_metrics, get_alignment_metrics, get_mosdepth_metrics, calculate_additional_reads, format_number_readable
from config import *

def load_and_prepare_samples(csv_file_path, samples_to_exclude):
    """
    Load sample list from CSV and prepare it for analysis
    
    Args:
        csv_file_path (str): Path to the sample sheet CSV
        samples_to_exclude (list): List of samples to exclude from analysis
    
    Returns:
        list: Cleaned list of unique sample names
    """
    df = pd.read_csv(csv_file_path)
    sample_names = df['sample'].tolist()
    
    # Remove duplicates from the list
    sample_names = list(set(sample_names))
    
    # Remove specific samples
    sample_names = list(filter(lambda x: x not in samples_to_exclude, sample_names))
    
    print(f"Original samples: {len(df['sample'].tolist())}")
    print(f"After removing duplicates: {len(list(set(df['sample'].tolist())))}")
    print(f"Samples excluded: {samples_to_exclude}")
    print(f"Final samples to process: {len(sample_names)}")
    
    return sample_names

def get_file_paths(sample, results_path):
    """
    Generate file paths for a given sample
    
    Args:
        sample (str): Sample name
        results_path (str): Base path to results directory
    
    Returns:
        tuple: (mark_duplicates_path, alignment_summary_path, mosdepth_summary_path)
    """
    mark_duplicates = os.path.join(results_path, "alignment", MARK_DUPLICATES_PATTERN.format(sample=sample))
    alignment_summary = os.path.join(results_path, "qc_bam", ALIGNMENT_SUMMARY_PATTERN.format(sample=sample))
    mosdepth_summary = os.path.join(results_path, "qc_bam", MOSDEPTH_SUMMARY_PATTERN.format(sample=sample))
    
    return mark_duplicates, alignment_summary, mosdepth_summary

def extract_sample_metrics(sample, results_path, target_coverage):
    """
    Extract all metrics for a single sample
    
    Args:
        sample (str): Sample name
        results_path (str): Base path to results directory
        target_coverage (float): Target coverage for additional reads calculation
    
    Returns:
        dict: Dictionary containing all formatted sample metrics
    """
    try:
        # Get file paths
        mark_duplicates, alignment_summary, mosdepth_summary = get_file_paths(sample, results_path)
        
        # Extract raw metrics
        total_reads = float(get_alignment_metrics(alignment_summary)['total_reads'])
        aligned_reads = float(get_alignment_metrics(alignment_summary)['pf_reads_aligned'])
        percent_dup = float(parse_mark_duplicates_metrics(mark_duplicates)['PERCENT_DUPLICATION'])
        mean_coverage = float(get_mosdepth_metrics(mosdepth_summary)['mean_coverage'])
        
        # Calculations 
        saturation_fraction = 1 - percent_dup
        
        additional_reads = float(calculate_additional_reads(
            current_reads=total_reads, 
            current_coverage=mean_coverage, 
            target_coverage=target_coverage, 
            saturation_fraction=saturation_fraction
        )["additional_reads_adjusted"])
        
        # Format values
        sample_info = {
            'sample_name': sample,
            'total_reads': format_number_readable(total_reads),
            'aligned_reads': format_number_readable(aligned_reads),
            'mean_coverage': mean_coverage,
            'percent_duplication': percent_dup,
            'saturation_fraction': saturation_fraction,
            'additional_reads': format_number_readable(additional_reads)
        }
        
        # Print progress
        print(f"✅ {sample}: {total_reads:,.0f} total, {aligned_reads:,.0f} aligned, {mean_coverage:.2f}x coverage, {percent_dup*100:.2f}% dup")
        
        return sample_info
        
    except Exception as e:
        print(f"❌ {sample}: Error - {e}")
        return {
            'sample_name': sample,
            'total_reads': 'Error',
            'aligned_reads': 'Error',
            'mean_coverage': 'Error',
            'percent_duplication': 'Error',
            'saturation_fraction': 'Error',
            'additional_reads': 'Error'
        }

def process_all_samples(sample_names, results_path, target_coverage):
    """
    Process all samples and extract their metrics
    
    Args:
        sample_names (list): List of sample names to process
        results_path (str): Base path to results directory
        target_coverage (float): Target coverage for calculations
    
    Returns:
        list: List of dictionaries containing sample metrics
    """
    sample_data = []
    
    print(f"\n{'='*80}")
    print("PROCESSING SAMPLES")
    print(f"{'='*80}")
    
    for sample in sample_names:
        sample_info = extract_sample_metrics(sample, results_path, target_coverage)
        sample_data.append(sample_info)
    
    return sample_data

def save_to_csv(sample_data, output_dir, filename):
    """
    Save sample data to CSV file
    
    Args:
        sample_data (list): List of sample data dictionaries
        output_dir (str): Output directory path
        filename (str): Output filename
    
    Returns:
        str: Full path to saved CSV file
    """
    # Create DataFrame
    metrics_df = pd.DataFrame(sample_data)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_csv_file = os.path.join(output_dir, filename)
    metrics_df.to_csv(output_csv_file, index=False)
    
    return output_csv_file

def save_to_excel(sample_data, output_dir, filename, target_coverage):
    """
    Save sample data to Excel file with multiple sheets
    
    Args:
        sample_data (list): List of sample data dictionaries
        output_dir (str): Output directory path
        filename (str): Output filename
        target_coverage (float): Target coverage used in analysis
    
    Returns:
        str: Full path to saved Excel file
    """
    # Create DataFrames
    metrics_df = pd.DataFrame(sample_data)
    metadata_df = pd.DataFrame(COLUMN_METADATA)
    calculations_df = pd.DataFrame(CALCULATIONS_INFO)
    
    # Create summary statistics
    summary_stats = {
        'Metric': [
            'Total Samples',
            'Processing Date',
            'Target Coverage',
            'Results Path',
            'Samples Excluded'
        ],
        'Value': [
            len(metrics_df),
            pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            f'{target_coverage}x',
            RESULTS_PATH,
            ', '.join(SAMPLES_TO_EXCLUDE)
        ]
    }
    summary_df = pd.DataFrame(summary_stats)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Excel
    output_excel_file = os.path.join(output_dir, filename)
    
    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        metrics_df.to_excel(writer, sheet_name='Sample_Metrics', index=False)
        metadata_df.to_excel(writer, sheet_name='Column_Descriptions', index=False)
        calculations_df.to_excel(writer, sheet_name='Calculations', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    return output_excel_file

def print_summary(sample_data, csv_file, excel_file):
    """
    Print analysis summary
    
    Args:
        sample_data (list): List of sample data dictionaries
        csv_file (str): Path to saved CSV file
        excel_file (str): Path to saved Excel file
    """
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"✅ CSV file saved to: {csv_file}")
    print(f"✅ Excel file saved to: {excel_file}")
    print(f"📊 Total samples processed: {len(sample_data)}")
    
    # Count successful vs failed samples
    successful = sum(1 for sample in sample_data if sample['total_reads'] != 'Error')
    failed = len(sample_data) - successful
    
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    if excel_file:
        print(f"\n📋 Excel file contains:")
        print("   • Sheet 1: Sample_Metrics - Main data")
        print("   • Sheet 2: Column_Descriptions - Column explanations")
        print("   • Sheet 3: Calculations - Formulas and methods")
        print("   • Sheet 4: Summary - Analysis summary")