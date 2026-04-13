# Usage: Rscript plot_coverage_static.R <config.yaml>
# Produces a static PNG with two panels: total aligned bases + coverage boxplot.

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(yaml))
suppressPackageStartupMessages(library(forcats))
suppressPackageStartupMessages(library(ggrepel))
suppressPackageStartupMessages(library(cowplot))

# --- Read config
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No YAML config provided. Usage: Rscript plot_coverage_static.R config.yaml")
}
params <- read_yaml(args[1])
list2env(x = params, envir = environment())
rm(params)

# --- Load data
read_mosdepth_summary <- function(sample_list_with_id_path) {
    list2env(x = sample_list_with_id_path, envir = environment())
    read.table(path, sep = "\t", header = TRUE) %>%
        filter(!grepl(chrom, pattern = "_")) %>%
        filter(!(chrom %in% c("chrM", "chrEBV", "total"))) %>%
        mutate(sample = id)
}

mosdepth_summary <- lapply(samples, FUN = read_mosdepth_summary) %>%
    do.call(args = ., what = rbind)

# --- Plot 1: Total aligned bases per sample
total_aligned_summary <- mosdepth_summary %>%
    group_by(sample) %>%
    summarise(total_aligned_bases = sum(bases))

p_aligned <- ggplot(total_aligned_summary,
        aes(x = fct_reorder(sample, desc(total_aligned_bases)),
            y = total_aligned_bases / 1e9,
            fill = total_aligned_bases / 1e9)) +
    geom_col() +
    theme_classic() +
    ylab("Total aligned bases (Gb)") +
    xlab("Sample") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "none") +
    ggtitle("Total aligned bases per sample (Chr1-22, X, Y)")

# --- Plot 2: Coverage boxplot with outlier chromosome labels
mosdepth_summary <- mosdepth_summary %>%
    group_by(sample) %>%
    mutate(
        outlier = (mean < median(mean) - sd(mean) * 2) |
                  (mean > median(mean) + sd(mean) * 1.3),
        label   = if_else(outlier, chrom, NA_character_),
        median_coverage = median(mean)
    )

p_coverage <- ggplot(mosdepth_summary,
        aes(x    = fct_reorder(.f = sample, .x = mean, .fun = sum, .desc = TRUE),
            y     = mean,
            label = label)) +
    geom_boxplot(aes(fill = median_coverage)) +
    scale_fill_continuous(limits = c(10, 40)) +
    geom_text_repel(direction = "y", na.rm = TRUE) +
    theme_classic() +
    ylab("Mean coverage (X)") +
    xlab("Sample") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "none") +
    ggtitle("Coverage per sample across chromosomes")

# --- Save
if (!exists("plot_name")) plot_name <- "coverage_plot.html"
png_name <- paste0(sub("\\.html$", "", plot_name), ".png")
filename  <- file.path(out_dir, png_name)

dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
ggsave(
    plot     = plot_grid(p_aligned, p_coverage, ncol = 2),
    filename = filename,
    width    = 12,
    height   = 6
)
cat("Plot saved to:", filename, "\n")
