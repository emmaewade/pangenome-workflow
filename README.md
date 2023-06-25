# (name) : Pangenomics Snakemake Workflow
[![Snakemake](https://img.shields.io/badge/snakemake-≥7.25.0-brightgreen.svg)](https://snakemake.github.io)

## Environment Setup
Snakemake is best installed via the [Mamba package manager] (https://github.com/mamba-org/mamba) (a drop-in replacement for conda). If you have neither Conda nor Mamba, it can be installed via [Mambaforge] (https://github.com/conda-forge/miniforge#mambaforge). For other options see [here] (https://github.com/mamba-org/mamba).

Given that Mamba is installed, run the following command to make a conda environment including snakemake, singularity, and (if available) GNU parallel. 

'''
mamba create -c conda-forge -c bioconda --name snakemake snakemake singularity parallel
'''

## Clone directory

First, create an appropriate project working directory on your system and enter it:

mkdir -p path/to/project-workdir
cd path/to/project-workdir
In all following steps, we will assume that you are inside of that directory.

Second, run
```
git clone https://github.com/emmaewade/pangenome-workflow . 
```

Two folders, *workflow* and *config*, will be downloaded to your current directory. *Workflow* contains the Snakefile aka a file of rules or the "control center" of the workflow, a folder of needed scripts, and a folder of input files for practice. *Config* contains files for cluster control and *config.yaml*. *Config.yaml* will be editted later to configure the workflow.

### Configuration

The workflow is given six arguments: 

**outname** : output files will be put in the directory *directory/outname*

**accortaxon** : specifies whether the given filename contains a list of accession numbers or taxon IDs. *options: accession or taxonomy*

**filename** : a new line delimited file of accession numbers or NCBI taxonomy IDs 

**only_download_complete_genomes** : will limit the downloaded assemblies to assembly_level=complete genome. if t *options: t or f*

**only_download_latest** : will limit the downloaded assemblies to version=latest if t. *options: t or f*

**roary_command** : command fed to roary. example: *'-r -p 30 -e --mafft -i 80 -cd 80 -f'*

Arguments can be adjusted in the configuration file **config/config.yaml** under *config:* and the workflow ran by

```
snakemake --profile config/  
```
or through arguments can be adjust through the command line like so: 

```
snakemake --profile config/  \
    --config \
        outname=hae_inf_727 \
        accortaxon=taxonomy \
        filename=workflow/testing-files/haemophilus.txt \
        only_download_complete_genomes=f \
        only_download_latest=t \
        roary_command='-r -p 30 -e --mafft -i 80 -cd 80 -f'
```

To submit jobs through a cluster environment, uncomment and adjust the *cluster:* lines in **config/config.yaml** appropriate to your cluster. Run the workflow by: 

```
snakemake --profile config/  
```

A few example commands are available in *workflow/testing-taxon-ids.sh*.

