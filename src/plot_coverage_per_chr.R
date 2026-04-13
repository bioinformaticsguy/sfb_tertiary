# Usage: Rscript plot_coverage_per_chr.R <config.yaml>

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(plotly))
suppressPackageStartupMessages(library(htmlwidgets))
suppressPackageStartupMessages(library(yaml))

# --- Read config
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No YAML config provided. Usage: Rscript plot_coverage_per_chr.R config.yaml")
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
    summarise(total_aligned_bases = sum(bases)) %>%
    arrange(desc(total_aligned_bases))

p_aligned <- plot_ly(
        total_aligned_summary,
        x = ~reorder(sample, -total_aligned_bases),
        y = ~round(total_aligned_bases / 1e9, 2),
        type = "bar",
        hovertemplate = "<b>%{x}</b><br>%{y:.2f} Gb<extra></extra>",
        marker = list(color = ~total_aligned_bases / 1e9,
                      colorscale = "Blues", showscale = FALSE)) %>%
    layout(
        title = "Total aligned bases per sample (Chr1-22, X, Y)",
        xaxis = list(title = "Sample", tickangle = -45),
        yaxis = list(title = "Aligned bases (Gb)"),
        showlegend = FALSE)

# --- Plot 2: Coverage per chromosome per sample
mosdepth_summary <- mosdepth_summary %>%
    group_by(sample) %>%
    mutate(median_coverage = median(mean))

p_coverage <- plot_ly(
        mosdepth_summary,
        x = ~reorder(sample, -median_coverage),
        y = ~mean,
        color = ~sample,
        type = "box",
        text = ~chrom,
        hovertemplate = "<b>%{text}</b><br>Coverage: %{y:.1f}x<extra></extra>",
        boxpoints = "outliers",
        pointpos = 0) %>%
    layout(
        title = "Coverage per chromosome per sample",
        xaxis = list(title = "Sample", tickangle = -45),
        yaxis = list(title = "Mean coverage (X)"),
        showlegend = FALSE)

# --- Combine and save as self-contained HTML
combined <- subplot(p_aligned, p_coverage,
                    nrows = 1, shareX = FALSE,
                    titleX = TRUE, titleY = TRUE,
                    margin = 0.06) %>%
    layout(title = list(text = "Coverage Summary", x = 0.5))

if (!exists("plot_name")) {
    plot_name <- "coverage_plot.html"
}

filename <- normalizePath(file.path(out_dir, plot_name), mustWork = FALSE)
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
saveWidget(combined, file = filename, selfcontained = TRUE)
cat("Plot saved to:", filename, "\n")
