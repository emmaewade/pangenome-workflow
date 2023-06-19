## Environment Setup
Install singularity and GNU parallel inside snakemake conda environment: 

```
conda activate snakemake
conda install -c conda-forge singularity
conda install -c conda-forge parallel
```

### Configuration

The workflow is given three arguments: 

*outname* : output files will be put in the directory `directory/*outname*`

*accortaxon* : specifies whether the given filename contains a list of accession numbers or taxon IDs. *options: accession or taxonomy*

*filename* : a new line delimited file of accession numbers or NCBI taxonomy IDs 


The workflow can be run interactively by : 
```
#To run on a list of accession IDs: 
snakemake --use-singularity --config outname=testingacc accortaxon=accession filename=workflow/testing-files/accsofinterest.txt

#To run on a list of taxon IDs: 
snakemake --use-singularity --config outname=testingtax accortaxon=taxonomy filename=workflow/testing-files/taxons.txt
```

The workflow can be run on a job manager by adjusting the commands in config/config.yaml and by running one of these commands:
```
#To run on a list of accession IDs:
snakemake --profile config/ --config outname=testingacc accortaxon=accession filename=workflow/testing-files/accsofinterest.txt

#To run on a list of taxon IDs:
snakemake --profile config/ --config outname=testingtax accortaxon=taxonomy filename=workflow/testing-files/taxons.txt
```
