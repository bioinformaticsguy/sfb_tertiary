# Use rocker's R Ubuntu image with tidyverse pre-installed
FROM rocker/tidyverse:4.3

# Set working directory
WORKDIR /app

# Install additional R packages not included in tidyverse
RUN R -e "install.packages(c('docopt', 'yaml', 'ggrepel', 'cowplot'), repos='https://cloud.r-project.org/')"

# Default command
CMD ["R"]