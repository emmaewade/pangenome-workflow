# (name) : Pangenomics Snakemake Workflow
[![Snakemake](https://img.shields.io/badge/snakemake-≥7.25.0-brightgreen.svg)](https://snakemake.github.io)

## Environment Setup
Snakemake is best installed via the [Mamba package manager](https://github.com/mamba-org/mamba) (a drop-in replacement for conda). If you have neither Conda nor Mamba, it can be installed via [Mambaforge](https://github.com/conda-forge/miniforge#mambaforge). For other options see [here](https://github.com/mamba-org/mamba).

Given that Mamba is installed, run the following command to make a conda environment including snakemake, singularity, and GNU parallel. Activate your environment.

```
mamba create -c conda-forge -c bioconda --name snakemake snakemake singularity parallel

mamba activate snakemake
```

If you would rather not use mamba, conda works fine too

```
conda create -c conda-forge -c bioconda --name snakemake snakemake singularity parallel

conda activate snakemake
```

Ensure your snakemake version is > 7.0.0! Try `mamba update snakemake` if it is the incorrect version.

## Clone directory

First, create an appropriate project working directory on your system and enter it:

```
mkdir -p path/to/project-workdir
cd path/to/project-workdir
```

In all following steps, we will assume that you are inside of that directory.

Second, run
```
git clone https://github.com/emmaewade/pangenome-workflow . 
```

Two folders, *workflow* and *config*, will be downloaded to your current directory. *Workflow* contains the Snakefile aka a file of rules or the "control center" of the workflow, a folder of needed scripts, and a folder of input files for practice. *Config* contains files for cluster control and *config.yaml*. *Config.yaml* will be editted later to configure the workflow.

## Configuration

The workflow is given six arguments: 

**outname** : output files will be put in the directory *directory/outname*

**accortaxon** : specifies whether the given filename contains a list of accession numbers or taxon IDs. *options: accession or taxonomy*

**filename** : a new line delimited file of accession numbers or NCBI taxonomy IDs 

**only_download_complete_genomes** : will limit the downloaded assemblies to assembly_level=complete genome. if t *options: t or f*

**only_download_latest** : will limit the downloaded assemblies to version=latest if t. *options: t or f*

**roary_command** : command fed to roary. example: *'-r -p 30 -e --mafft -i 80 -cd 80 -f'*

Arguments, wanted cores, and job resources can be adjusted in the configuration file **config/config.yaml** . 

## Running
After configuration, the workflow can be run by 

```
snakemake --profile config/  
```

or command line arguments can override those in **config/config.yaml** like so: 

```
snakemake --profile config/  \
    --config \
        outname=taxonomy_test \
        accortaxon=taxonomy \
        filename=workflow/testing-files/taxons.txt \
        only_download_complete_genomes=f \
        only_download_latest=t \
        roary_command='-r -p 30 -e --mafft -i 80 -cd 80 -f'
```

To submit jobs to a job manager like SLURM, uncomment and adjust the SLURM job submission lines in **config/config.yaml** appropriate to your cluster. Then edit (if necessary) and make the config/parseJobID.sh config/status-saact.sh files executable: 
```
chmod +x config/parseJobID.sh config/status-sacct.sh 
```
Run the workflow with the same commands as above. This time they will be submitted to your job manager. 

A few example commands are available in *workflow/testing-commands.sh* for practice.

## Output
After the workflow parses taxonomies (if necessary), downloads GBFF files, processes GFF and FASTA files, and runs ABySS and Roary, a number of files and directories will be created in the output directory results/*outname*.

- *abyss_fac_output.txt* : output of abyss-fac analysis on FASTA files
- *gbff-downloads* : folder of downloaded gbff files
- *master_abyss.csv* : file joining master.tsv and abyss_fac_output.txt, useful for downstream analysis
- *NCBI-gbff-accessions-not-downloaded.txt* : file of gbff accessions not downloaded, could be processing issues or if gbff file doesn't exist
- *roary* : folder of roary log files
- *species.csv* : file containing taxonomy ids (not necessarily species) that will be parsed for
- *for_download.txt* : file of ftp paths 
- *incomplete_files* : folder of gbff files that were not completely downloaded, common when downloading a large number of files
- *master.tsv* : file of useful assembly information
- *processed_files* : folder of processed GFF3 and FASTA files
- *roary_%number%* : roary output directory
- *summaries* : folder of files used mainly to connect workflow rules

Additionally *assembly_summary_genbank.txt* , *assembly_summary_refseq.txt*,  *names.dmp*, and  *nodes.dmp* will be downloaded into *workflow/data* after the first run. These are heavy files and can be deleted in between or after running. 

## Citations
1. ABySS:
2. Bit Package:
3. GNU Parallel: 
4. Roary:
5. Snakemake:

## Please cite XXX at DOI: 

