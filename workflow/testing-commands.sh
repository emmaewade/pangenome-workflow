snakemake --profile config/  \
    --config \
        outname=all_omni_419015 \
        accortaxon=taxonomy \
        filename=testing-files/taxonomy.txt \
        only_download_complete_genomes=f \
        only_download_latest=t \
        roary_command='-r -p 30 -e --mafft -i 80 -cd 80 -f'

snakemake --profile config/  \
    --config \
        outname=acc_of_interest \
        accortaxon=accession \
        filename=testing-files/taxonomy.txt \
        only_download_complete_genomes=f \
        only_download_latest=f \
        roary_command='-r -p 30 -e --mafft -i 80 -cd 80 -f'
