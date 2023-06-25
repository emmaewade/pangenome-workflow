#!/usr/bin/env bash
# setting colors to use
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'
## help info ##
# called by program name with no arguments or with "-h" as only positional argument
if [ "$#" == 0 ] || [ $1 == "-h" ] || [ $1 == "help" ]; then


    printf "\n --------------------------------  HELP INFO  --------------------------------- \n\n"
    printf "  This program downloads assembly files for NCBI genomes. It takes as input\n"
    printf "  assembly accessions (either GCA_* or GCF_*) and optionally a specification of\n"
    printf "  which format to download. For version info, run \`bit-version\`.\n\n"

    printf "    Required input:\n\n"
    printf "        - [-w <file>] single-column file of NCBI assembly accessions or taxonomy IDs\n\n"

    printf "    Optional arguments include:\n\n"

    printf "        - [-f <str>] \n"
    printf "                  Specify the desired format. Available options currently\n"
    printf "                  include: taxonomy or accession. If provided taxonomy, \n"
    printf "                  will additionally parse NCBI taxonomy. \n\n"
    printf "        - [-d <str> ] default: ./\n"
    printf "                  Output directory.\n\n"
    printf "        - [-c <str> ] default: t\n"
    printf "                  Filter to only complete genomes. CASE SENSITIVE t/f
    printf "                  t = only complete genomes 
    printf "                  f = complete genomes, scaffolds, chromosomes, and contigs.\n\n"
    printf "        - [-v <str> ] default: t\n"
    printf "                  Filter to only latest genomes. CASE SENSITIVE t/f
    printf "                  t = only latest
    printf "                  f = latest, replaces, and supresses.\n\n"
    printf "    Example usage:\n\n\t bit-dl-ncbi-assemblies -w ncbi_accessions.txt -f accession -d . -c t -v t. \n\n"

    exit
fi

printf "\n"

## setting default ##
#format="genbank"
#num_jobs=1
outdir="."
complete=t
version=t

## parsing arguments
while getopts :w:f:d:c:v: args
do
    case "${args}" 
    in
        w) NCBI_file=${OPTARG};;
        f) format=${OPTARG};;
        d) outdir=${OPTARG};;
        c) complete=${OPTARG};;
        v) version=${OPTARG};;
        \?) printf "\n  ${RED}Invalid argument: -${OPTARG}${NC}\n\n    Run 'bit-adapted-assemble-wanted.sh' with no arguments or '-h' only to see help menu.\n\n" >&2 && exit
    esac
done

## making sure input file was provided ##
if [ ! -n "$NCBI_file" ]; then
    printf "\n  ${RED}You need to provide an input file with NCBI accessions or taxonomies!${NC}\n"
    printf "\nExiting for now.\n\n"
    exit
fi

## making sure format specified is interpretable
if [[ "$format" != "taxonomy" && $format != "accession" ]]; then
    printf "\n  ${RED}Invalid argument passed to \'-f' option: $format\n\n${NC}"
    printf "  Valid options are taxonomy or accession.\n"
    printf "Exiting for now.\n\n"
    exit
fi

if [[ "$complete" != "t" && "$complete" != "f" ]]; then
    printf "\n  ${RED}Invalid argument passed to \'-c' option: $complete\n\n${NC}"
    printf "  Valid options are t or f, case sensitive.\n"
    printf "Exiting for now.\n\n"
    exit
fi

if [[ "$version" != "t" && "$version" != "f" ]]; then
    printf "\n  ${RED}Invalid argument passed to \'-v' option: $version\n\n${NC}"
    printf "  Valid options are t or f, case sensitive.\n"
    printf "Exiting for now.\n\n"
    exit
fi


## making sure input file is there, and storing total number of targets ##
if [ -f "$NCBI_file" ]; then

    if [ $format == "accession" ]; then
        NCBI_input_genomes_total=$(wc -l $NCBI_file | sed "s/^ *//" | cut -d " " -f 1)
        printf "    Targeting $NCBI_file genomes.\n\n"
    fi
    
    if [ $format == "taxonomy" ]; then
    
        ## downloading taxonomy names and nodes (if not present in cwd already) ##
        if [ ! -s workflow/data/names.dmp ]; then
        
            printf "    ${GREEN}Downloading NCBI taxonomy data...${NC}\n\n"
            wd=$(pwd)
            curl --connect-timeout 30 --retry 10 ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz > workflow/data/taxdump.tar.gz || echo "failed" > capture_any_dl_errors.tmp
            
            # making sure file downloaded with no errors, trying again if it did not (i can't figure out why, but it fails sometimes and then works others)
            # trying a max of 10 times
            attempt=1
        
            while [ -s $outdir/capture_any_dl_errors.tmp ]; do
        
                if [[ ${attempt} -lt 16 ]]; then
        
                    # waiting a few seconds
                    sleep 3
        
                    # incrementing counter
                    attempt=$((attempt+1))
        
                    printf "\n    ${YELLOW}Snag downloading GenBank assembly summary table, trying up to 15 times. Attempt: ${attempt}${NC}\n\n"
        
                    if ! curl --connect-timeout 30 --retry 10 ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz > workflow/data/taxdump.tar.gz ; then
                        echo "failed" > $outdir/capture_any_dl_errors.tmp
                    else
                        rm -rf $outdir/capture_any_dl_errors.tmp
                    fi
        
                else
        
                        printf "\n\n  ${RED}Download of NCBI taxonomy failed :(${NC}\n  Is the internet connection weak?\n\nExiting for now.\n\n"
                        rm -rf $outdir/capture_any_dl_errors.tmp workflow/data/taxdump.tar.gz
                        exit
        
                fi
        
            done
            
            wd=$(pwd)
            cd workflow/data
            tar -xzf taxdump.tar.gz names.dmp nodes.dmp
            rm taxdump.tar.gz
            cd $wd
            rm -rf $outdir/capture_any_dl_errors.tmp
        
            
            printf "\n    ${YELLOW}Assembly summary tables downloaded successfully. They are stored\n"
            printf "    in the directory workflow/data/ as \"ncbi_assembly_info.tsv\".\n"
            printf "    That file is left here in you'd like to use it again soon. But be\n"
            printf "    sure to delete it if you'd like. Now getting to work on our targets.${NC}\n\n"
        
        fi

    
        python3 workflow/scripts/parse_taxon.py --filename $NCBI_file --savespeciesto $outdir
        total_IDs=$(wc -l $outdir"/species.csv" | sed "s/^ *//" | cut -d " " -f 1)
        
        if [ $total_IDs == 0 ]; then
            printf "    No taxonomy IDs found. Exiting... "
            exit
        fi
        
        printf "    Found $total_IDs taxon IDs. Noted under $outdir/species.csv.\n\n"
    fi
else
    printf "\n${RED}      You specified $NCBI_file, but that file cannot be found :(${NC}\n"
    printf "\nExiting for now.\n\n"
    exit
fi


# making sure output file to hold accessions not downloaded doesn't exist already, as it gets appended to
rm -rf $outdir/CBI-accessions-not-downloaded.txt

## downloading assembly summaries (if not present in cwd already) ##
if [ ! -s workflow/data/assembly_summary_genbank.txt ]; then

    printf "    ${GREEN}Downloading ncbi assembly summaries to be able to construct ftp links...${NC}\n\n"
    curl --connect-timeout 30 --retry 10 ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/assembly_summary_genbank.txt > workflow/data/assembly_summary_genbank.txt || echo "failed" > capture_any_dl_errors.tmp

    # making sure file downloaded with no errors, trying again if it did not (i can't figure out why, but it fails sometimes and then works others)
    # trying a max of 10 times
    attempt=1

    while [ -s $outdir/capture_any_dl_errors.tmp ]; do

        if [[ ${attempt} -lt 16 ]]; then

            # waiting a few seconds
            sleep 3

            # incrementing counter
            attempt=$((attempt+1))

            printf "\n    ${YELLOW}Snag downloading GenBank assembly summary table, trying up to 15 times. Attempt: ${attempt}${NC}\n\n"

            if ! curl --connect-timeout 30 --retry 10 ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/assembly_summary_genbank.txt > workflow/data/assembly_summary_genbank.txt ; then
                echo "failed" > $outdir/capture_any_dl_errors.tmp
            else
                rm -rf $outdir/capture_any_dl_errors.tmp
            fi

        else

                printf "\n\n  ${RED}Download of NCBI assembly summaries failed :(${NC}\n  Is the internet connection weak?\n\nExiting for now.\n\n"
                rm -rf $outdir/capture_any_dl_errors.tmp workflow/data/ncbi_assembly_info.tsv
                exit

        fi

    done

    rm -rf $outdir/capture_any_dl_errors.tmp

    printf "\n"
    curl --connect-timeout 30 --retry 10 ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt >> workflow/data/assembly_summary_refseq.txt || echo "failed" > $outdir/capture_any_dl_errors.tmp

    # doing the same as above, trying a few times because sometimes seems to work and others not for reasons I can't pin down yet
    attempt=1

    while [ -s $outdir/capture_any_dl_errors.tmp ]; do

        if [[ ${attempt} -lt 16 ]]; then

            # incrementing counter
            attempt=$((attempt+1))

            printf "\n    ${YELLOW}Snag downloading RefSeq assembly summary table, trying up to 15 times. Attempt: ${attempt}${NC}\n\n"

            if ! curl --connect-timeout 30 --retry 10 ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt >> workflow/data/ncbi_assembly_info.tsv ; then
                echo "failed" > $outdir/capture_any_dl_errors.tmp
            else
                rm -rf $outdir/capture_any_dl_errors.tmp
            fi

        else

                printf "\n\n  ${RED}Download of NCBI assembly summaries failed :(${NC}\n  Is the internet connection weak?\n\nExiting for now.\n\n"
                rm -rf $outdir/capture_any_dl_errors.tmp workflow/data/ncbi_assembly_info.tsv
                exit

        fi

    done

    rm -rf $outdir/capture_any_dl_errors.tmp
    
    printf "\n    ${YELLOW}Assembly summary tables downloaded successfully. They are stored\n"
    printf "    in the directory workflow/data/.\n"
    printf "    That file is left here in you'd like to use it again soon. But be\n"
    printf "    sure to delete it if you'd like. Now getting to work on our targets.${NC}\n\n"

fi


## parsing assembly summaries and generating base ftp link info tab ##
master=$outdir/master.tsv

if [ $format == "taxonomy" ]; then
    idfile=$outdir/species.csv
    printf "    Searching assembly summaries..."
    python3 workflow/scripts/helper-bit-parse-assembly-summary-file.py -g workflow/data/assembly_summary_genbank.txt -r workflow/data/assembly_summary_refseq.txt -w $idfile -t taxonomy -o $master -f $complete -v $version
    if [ -s $master ]; then 
        num=$(wc -l $master | sed "s/^ *//" | cut -d " " -f 1) 
        printf "   $num assemblies written to $master \n\n " 
    fi
fi 

if [ $format == "accession" ]; then
    printf "    Searching assembly summaries..."
    python3 workflow/scripts/helper-bit-parse-assembly-summary-file.py -g workflow/data/assembly_summary_genbank.txt -r workflow/data/assembly_summary_refseq.txt -w $NCBI_file -t accession -o $master -f $complete -v $version
    num=$(wc -l $master | sed "s/^ *//" | cut -d " " -f 1) 
    if [ -s $master ] ; then  
        num=$(wc -l $master | sed "s/^ *//" | cut -d " " -f 1) 
        printf "    $num assemblies written to $master \n\n " 
    fi
fi




