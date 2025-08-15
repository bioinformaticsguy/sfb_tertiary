"""
Main script to generate sample metrics CSV and Excel files
"""

import os
from config import *
from curated_functions import *
from analysis_functions import *

def main():
    """
    Main function to execute the analysis pipeline
    """
    # Print current directory
    print("Current directory:", os.getcwd())
    
    print(f"\n{'='*80}")
    print("SAMPLE METRICS ANALYSIS PIPELINE")
    print(f"{'='*80}")
    print(f"Results path: {RESULTS_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Target coverage: {TARGET_COVERAGE}x")
    
    # Step 1: Load and prepare sample list
    print(f"\n{'='*50}")
    print("STEP 1: LOADING SAMPLES")
    print(f"{'='*50}")
    
    sample_names = load_and_prepare_samples(CSV_FILE_PATH, SAMPLES_TO_EXCLUDE)
    
    if not sample_names:
        print("❌ No samples to process. Exiting.")
        return
    
    # Step 2: Process all samples
    print(f"\n{'='*50}")
    print("STEP 2: EXTRACTING METRICS")
    print(f"{'='*50}")
    
    sample_data = process_all_samples(sample_names, RESULTS_PATH, TARGET_COVERAGE)
    
    # Step 3: Save results
    print(f"\n{'='*50}")
    print("STEP 3: SAVING RESULTS")
    print(f"{'='*50}")
    
    # Save to CSV
    csv_file = save_to_csv(sample_data, OUTPUT_DIR, OUTPUT_CSV_FILE)
    
    # Save to Excel
    excel_file = save_to_excel(sample_data, OUTPUT_DIR, OUTPUT_EXCEL_FILE, TARGET_COVERAGE)
    
    # Step 4: Print summary
    print_summary(sample_data, csv_file, excel_file)


if __name__ == "__main__":
    main()




# import os
# import pandas as pd
# from curated_functions import parse_mark_duplicates_metrics, get_alignment_metrics, get_mosdepth_metrics, calculate_additional_reads, format_number_readable

# # Print the current directory
# print("Current directory:", os.getcwd())

# results_path = "/data/humangen_kircherlab/Users/hassan/rare_disease_outputs/013_thirty_one_samplesheet"
# output_dir = "/data/humangen_kircherlab/Users/hassan/sfb_tertiary/output/csv_files"
# csv_file_path = "/data/humangen_kircherlab/Users/hassan/run_rare/rare-disease-pipeline/sample_sheet_30.csv"




# df = pd.read_csv(csv_file_path)
# target_coverage = 30
# sample_names = df['sample'].tolist()
# # Remove duplicates from the list
# sample_names = list(set(sample_names))  # Convert to set and back to list
# # Remove specific samples
# samples_to_exclude = ['hugelymodelbat', 'A4842_DNA_42']
# sample_names = list(filter(lambda x: x not in samples_to_exclude, sample_names))


# # Create a list to store all sample data
# sample_data = []

# for sample in sample_names:
#         mark_duplicates = os.path.join(results_path, "alignment", f"{sample}_sorted_md.MarkDuplicates.metrics.txt")
#         alignment_summary = os.path.join(results_path, "qc_bam", f"{sample}_multiplemetrics.CollectMultipleMetrics.alignment_summary_metrics")
#         mosdepth_summary = os.path.join(results_path, "qc_bam", f"{sample}_mosdepth.mosdepth.summary.txt")


#         total_reads = float(get_alignment_metrics(alignment_summary)['total_reads'])
#         aligned_reads = float(get_alignment_metrics(alignment_summary)['pf_reads_aligned'])
#         percent_dup = float(parse_mark_duplicates_metrics(mark_duplicates)['PERCENT_DUPLICATION'])
#         mean_coverage = float(get_mosdepth_metrics(mosdepth_summary)['mean_coverage'])


#         # Calculations 
#         saturation_fraction = 1 - (percent_dup)

#         additional_reads = float(calculate_additional_reads(  current_reads=total_reads, 
#                                                         current_coverage=mean_coverage, 
#                                                         target_coverage=target_coverage, 
#                                                         saturation_fraction=saturation_fraction)["additional_reads_adjusted"])


#         # Format values before adding to dictionary
#         sample_info = {
#             'sample_name': sample,
#             'total_reads': format_number_readable(total_reads),
#             'aligned_reads': format_number_readable(aligned_reads),
#             'mean_coverage': f"{mean_coverage:.2f}x",
#             'percent_duplication': f"{percent_dup*100:.2f}%",
#             'saturation_fraction': f"{saturation_fraction:.3f}",
#             'additional_reads': format_number_readable(additional_reads)
#         }

#         sample_data.append(sample_info)

#         # Print progress
#         print(f" {sample}: {total_reads:,.0f} total, {aligned_reads:,.0f} aligned, {mean_coverage:.2f}x coverage, {percent_dup*100:.2f}% dup")


# # Create DataFrame from collected data
# metrics_df = pd.DataFrame(sample_data)


# # Save to CSV file
# output_csv_file = os.path.join(output_dir, "sample_metrics_summary.csv")
# metrics_df.to_csv(output_csv_file, index=False)
# print(f"\n Data saved to: {output_csv_file}")