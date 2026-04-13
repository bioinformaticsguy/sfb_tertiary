## Included by the main Snakefile — do not run directly.
## To trigger these rules, pass a configfile:
##   snakemake --configfile config/plot_config.yaml --use-conda --cores 4

import os

def _plot_files(cfg):
    """Derive all output paths from out_dir and plot_name."""
    base = os.path.join(
        cfg.get("out_dir", "output/plots/r_plots"),
        os.path.splitext(cfg.get("plot_name", "coverage_plot.html"))[0]
    )
    return {
        "aligned": base + "_aligned.html",
        "boxplot":  base + "_boxplot.html",
        "per_chr":  base + "_per_chr.html",
        "static":   base + ".png",
        "report":   base + "_qc_report.html",
    }

rule plot_coverage:
    output:
        aligned = _plot_files(config)["aligned"],
        boxplot  = _plot_files(config)["boxplot"],
        per_chr  = _plot_files(config)["per_chr"],
    params:
        config_file = workflow.configfiles[0]
    conda:
        "envs/r_environment.yaml"
    container:
        "docker://bioinformaticsguy/r-plotting:latest"
    shell:
        """
        mkdir -p {config[out_dir]}
        Rscript src/plot_coverage_per_chr.R {params.config_file}
        """

rule plot_coverage_static:
    output:
        static = _plot_files(config)["static"],
    params:
        config_file = workflow.configfiles[0]
    conda:
        "envs/r_environment.yaml"
    container:
        "docker://bioinformaticsguy/r-plotting:latest"
    shell:
        """
        mkdir -p {config[out_dir]}
        Rscript src/plot_coverage_static.R {params.config_file}
        """

rule render_qc_report:
    output:
        report = _plot_files(config)["report"],
    params:
        config_file = os.path.abspath(workflow.configfiles[0]),
        out_dir     = os.path.abspath(config.get("out_dir", "output/plots/r_plots")),
        report_name = os.path.basename(_plot_files(config)["report"]),
    conda:
        "envs/qc_report.yaml"
    shell:
        """
        mkdir -p {params.out_dir}
        quarto render quarto_rep/qc_report.qmd \
            -P config_file:{params.config_file} \
            --output {params.report_name} \
            --output-dir {params.out_dir}
        """
