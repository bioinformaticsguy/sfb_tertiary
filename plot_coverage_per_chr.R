# Usage: Rscript plot_coverage_per_chromosome.R. Needs to have an associated data_to_plot.yaml file with parameters

# load libraries
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(docopt))
suppressPackageStartupMessages(library(yaml))
suppressPackageStartupMessages(library(forcats))
suppressPackageStartupMessages(library(ggrepel))
suppressPackageStartupMessages(library(cowplot))


# Ensure the script correctly captures command-line arguments
args <- commandArgs(trailingOnly = TRUE)  # Get arguments properly

# Check if an argument (YAML file) is provided
if (length(args) == 0) {
  stop("Error: No YAML file provided. Usage: Rscript plot_coverage_per_chr.R data_to_plot.yaml")
}

# --- Read in the parameters from the yaml file
yaml_file <- ifelse(length(args) > 0, args[1], "data_to_plot.yaml")  # Use argument if provided, else default
params <- read_yaml(yaml_file)
#print(glimpse(params)) # Print all the requested parameters
list2env(x = params, envir = environment()) # make all the list elements into variables in the current env
rm(params)

# Function to read in the mosdpeth summary file
read_mosdepth_summary <- function(sample_list_with_id_path) {
    list2env(x = sample_list_with_id_path, envir = environment())
    file_mosdepth <- list.files(pattern = paste0(id, ".*", ".mosdepth.summary.txt$"),
        path = paste0(path, "/mosdepth"))
        print(path)
    file_mosdepth <- paste0(path, file_mosdepth)
    print(file_mosdepth)
    mosdepth_df <- read.table(file_mosdepth, sep = "\t", header = TRUE) %>%
        filter(!grepl(chrom, pattern = "_")) %>%
        filter(!(chrom %in% c("chrM", "chrEBV", "total"))) %>%
        mutate(sample = id)
}

# Get mosdepth summaries across all samples
mosdepth_summary <- lapply(samples, FUN = read_mosdepth_summary) %>%
    do.call(args = ., what = rbind)

## Create plots
plots <- list()

total_aligned_summary <- mosdepth_summary %>%
    group_by(sample) %>%
    summarise(total_aligned_bases = sum(bases))
plots$total_aligned_bases <- ggplot(total_aligned_summary, 
        aes(x = fct_reorder(sample, desc(total_aligned_bases)),
            y = total_aligned_bases/1E9, 
            fill = total_aligned_bases/1E9)) +
    geom_col() + 
    theme_classic() +
    ylab("Total number of aligned bases (Gb)") +
    xlab("Samples") +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1), legend.position = "none") +
    ggtitle("Number of aligned bases per sample (Chr1-22,X,Y)")

mosdepth_summary <- mosdepth_summary %>%
    group_by(sample) %>%
    mutate(outlier = (mean < median(mean) - (sd(mean) * 2)) | (mean > median(mean) + (sd(mean) * 1.3))) %>%
    mutate(label = case_when(outlier ~ chrom)) %>%
    mutate(median_coverage = median(mean))
plots$coverage_per_sample <- ggplot(mosdepth_summary,
        aes(x = fct_reorder(.f = sample, .x = mean, .fun = sum, .desc = TRUE),
            y = mean,
            label = label,
            fill = mean)) +
    geom_boxplot(aes(fill = median_coverage)) +
    scale_fill_continuous(limits = c(10, 25)) +
    geom_text_repel(direction = "y") +
    theme_classic() +
    ylab("Mean coverage (X)") +
    xlab("Samples") +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1), legend.position = "none") +
    ggtitle("Coverage per sample across chromosomes")

dir.create(path = out_dir)
filename <- paste0(out_dir, "hg002_minimai.png")
ggsave(plot = plot_grid(plotlist = plots, ncol = 2), filename = filename, width = 10, height = 5)