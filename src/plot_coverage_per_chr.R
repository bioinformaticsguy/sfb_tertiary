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

# --- Output filenames derived from plot_name
if (!exists("plot_name")) plot_name <- "coverage_plot.html"
base_name <- sub("\\.html$", "", plot_name)
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

save_plot <- function(p, suffix) {
    f <- normalizePath(file.path(out_dir, paste0(base_name, suffix)), mustWork = FALSE)
    saveWidget(p, file = f, selfcontained = TRUE)
    cat("Saved:", f, "\n")
}

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

save_plot(p_aligned, "_aligned.html")

# --- Plot 2: Coverage distribution per sample (boxplot)
mosdepth_summary <- mosdepth_summary %>%
    group_by(sample) %>%
    mutate(median_coverage = median(mean))

p_boxplot <- plot_ly(
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
        title = "Coverage distribution per sample (Chr1-22, X, Y)",
        xaxis = list(title = "Sample", tickangle = -45),
        yaxis = list(title = "Mean coverage (X)"),
        showlegend = FALSE)

save_plot(p_boxplot, "_boxplot.html")

# --- Plot 3: Per-chromosome coverage with chrX/chrY highlighted
chrom_order <- c(paste0("chr", 1:22), "chrX", "chrY")

mosdepth_per_chr <- mosdepth_summary %>%
    filter(chrom %in% chrom_order) %>%
    mutate(chrom = factor(chrom, levels = chrom_order))

# One trace per sample so each gets its own colour and legend entry
p_per_chr <- plot_ly()
for (s in unique(mosdepth_per_chr$sample)) {
    d <- filter(mosdepth_per_chr, sample == s)
    p_per_chr <- add_trace(p_per_chr,
        x = ~chrom, y = ~mean,
        data = d,
        name = s,
        type = "scatter",
        mode = "lines+markers",
        marker = list(size = 8),
        hovertemplate = paste0("<b>%{x}</b><br>Coverage: %{y:.1f}x<extra>", s, "</extra>"))
}

# Shade sex chromosomes — x0/x1 are 0-based category indices (chrX=22, chrY=23)
p_per_chr <- layout(p_per_chr,
    title = "Per-chromosome coverage",
    xaxis = list(title = "Chromosome", tickangle = -45),
    yaxis = list(title = "Mean coverage (X)"),
    showlegend = TRUE,
    shapes = list(
        list(type = "rect",
             xref = "x", yref = "paper",
             x0 = 21.5, x1 = 23.5,
             y0 = 0, y1 = 1,
             fillcolor = "rgba(135, 206, 250, 0.20)",
             line = list(width = 0))),
    annotations = list(
        list(x = 22.5, xref = "x",
             y = 1, yref = "paper",
             text = "sex chromosomes",
             showarrow = FALSE,
             yanchor = "bottom",
             font = list(size = 11, color = "steelblue"))))

save_plot(p_per_chr, "_per_chr.html")
