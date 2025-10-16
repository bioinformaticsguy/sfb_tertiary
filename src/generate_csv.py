"""
Main script to generate sample metrics CSV and Excel files
"""

## Change the file paths in the config.py file before running this script. 
## Three main things to adjust are the RESULTS_PATH, OUTPUT_DIR, and CSV_FILE_PATH variables.

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