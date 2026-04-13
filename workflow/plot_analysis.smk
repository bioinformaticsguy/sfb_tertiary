## Included by the main Snakefile — do not run directly.
## To trigger this rule, pass a configfile:
##   snakemake --configfile config/plot_config.yaml --cores 1

import os

rule plot_coverage:
    output:
        os.path.join(config["out_dir"], config["plot_name"])
    params:
        config_file=workflow.configfiles[0]
    conda:
        "envs/r_environment.yaml"
    container:
        "docker://bioinformaticsguy/r-plotting:latest"
    shell:
        """
        mkdir -p {config[out_dir]}
        Rscript src/plot_coverage_per_chr.R {params.config_file}
        """
