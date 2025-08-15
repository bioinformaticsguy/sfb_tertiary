def parse_mark_duplicates_metrics(file_path):
    """Parse MarkDuplicates metrics file and extract key metrics"""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Find the metrics data line (after the header)
        for i, line in enumerate(lines):
            if line.startswith('LIBRARY'):
                # This is the header line
                header = line.strip().split('\t')
                if i + 1 < len(lines):
                    # Next line contains the data
                    data = lines[i + 1].strip().split('\t')
                    
                    # Create a dictionary mapping header to data
                    metrics = dict(zip(header, data))
                    return metrics
        
        return None
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None



def extract_percent_duplication(file_path):
    """Extract just the percent duplication value"""
    metrics = parse_mark_duplicates_metrics(file_path)
    if metrics and 'PERCENT_DUPLICATION' in metrics:
        return float(metrics['PERCENT_DUPLICATION'])
    return None


def get_alignment_metrics(file_path):
    """Extract multiple alignment metrics"""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('PAIR'):
                    parts = line.strip().split('\t')
                    return {
                        'total_reads': int(parts[1]),
                        'pf_reads': int(parts[2]),
                        'pct_pf_reads': float(parts[3]),
                        'pf_reads_aligned': int(parts[5]),
                        'pct_pf_reads_aligned': float(parts[6]),
                        'mean_read_length': float(parts[15])
                    }
        return None
    except:
        return None


def get_mosdepth_metrics(file_path):
    """Extract multiple metrics from mosdepth summary file"""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('total'):
                    parts = line.strip().split('\t')
                    return {
                        'total_length': int(parts[1]),
                        'total_bases': int(parts[2]),
                        'mean_coverage': float(parts[3]),
                        'min_coverage': int(parts[4]),
                        'max_coverage': int(parts[5])
                    }
        return None
    except:
        return None


def calculate_additional_reads(current_reads, current_coverage, target_coverage, saturation_fraction):
    """
    Calculate additional reads needed to reach target coverage
    
    Parameters:
    - current_reads: Total number of current reads
    - current_coverage: Current mean coverage
    - target_coverage: Desired target coverage
    - saturation_fraction: 1 - percent_duplication
    
    Returns:
    - Dictionary with calculation results
    """
    
    # Handle edge cases
    if current_coverage <= 0:
        return {
            'additional_coverage_needed': None,
            'additional_reads_needed': None,
            'additional_reads_adjusted': None
        }
    
    # Step 1: Calculate additional coverage needed
    additional_coverage = target_coverage - current_coverage
    
    # If already at or above target, no additional reads needed
    if additional_coverage <= 0:
        return {
            'additional_coverage_needed': 0,
            'additional_reads_needed': 0,
            'additional_reads_adjusted': 0,
        }
    
    # Step 2: Calculate reads needed ignoring duplication
    additional_reads = current_reads * (additional_coverage / current_coverage)
    
    # Step 3: Adjust for duplication (saturation fraction)
    if saturation_fraction > 0:
        additional_reads_adjusted = additional_reads / saturation_fraction
    else:
        additional_reads_adjusted = float('inf')  # Cannot reach target if saturation is 0
        
    return {
        'additional_coverage_needed': additional_coverage,
        'additional_reads_needed': additional_reads,
        'additional_reads_adjusted': additional_reads_adjusted,
    }

def format_number_readable(num):
    """Convert large numbers to human readable format"""
    if num >= 1_000_000:
        return float(f"{num/1_000_000:.1f}")
    else:
        return float(f"{num:.0f}")