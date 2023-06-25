#!/usr/bin/env bash

### Helper script used with `bit-dl-ncbi-assemblies` when run in parallel; for version info, run or see `bit-version` ###

# setting colors to use
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

my_ext=$2
ext=$3
format=$4
outdir=$5

assembly=$(echo "$1" | cut -f 2)
downloaded_accession=$(echo "$1" | cut -f 2)

# storing and building links
base_link=$(echo "$1" | cut -f 9)
#base_link=$(echo "$1" | cut -f 8)

#Regular output : GCA_018603945.1 GCA_018603945.1 ASM1860394v1    28037   Streptococcus mitis     strain=14-4881  latest  Contig  https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/018/603/945/GCA_018603945.1_ASM1860394v1
# GCA_018215285.1 GCA_018215285.1 SAMN18737296    2828286 Streptococcus sp. 11-4097       SAMN18737296    1       https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/018/215/285/GCA_018215285.1_ASM1821528v1
# checking link was actually present (sometimes, very rarely, it is not there)
# if not there, attempting to build ourselves
if [ $base_link == "na" ] || [ -z $base_link ]; then

    p1=$(printf "ftp://ftp.ncbi.nlm.nih.gov/genomes/all")

    # checking if GCF or GCA
    if [[ $assembly == "GCF"* ]]; then 
        p2="GCF"
    else
        p2="GCA"
    fi
    
    p3=$(echo $assembly | cut -f 2 -d "_" | cut -c 1-3)
    p4=$(echo $assembly | cut -f 2 -d "_" | cut -c 4-6)
    p5=$(echo $assembly | cut -f 2 -d "_" | cut -c 7-9)

    ass_name=$(echo "$1" | cut -f 3)
    end_path=$(paste -d "_" <(echo "$assembly") <(echo "$ass_name"))

    base_link=$(paste -d "/" <(echo "$p1") <(echo "$p2") <(echo "$p3") <(echo "$p4") <(echo "$p5") <(echo "$end_path"))

else

    end_path=$(basename $base_link)

fi

curl --silent --retry 10 -o ${outdir}/${assembly}${my_ext} "${base_link}/${end_path}${ext}"

# grabbing this to check if " XML " is in there
    # when this was first written, trying to download a link that wasn't there would fail
    # now it can download an xml-formated file saying the link wasn't found at NCBI
    # so this let's us check for that, and report and remove it if that's the case
file_command_output=$(file ${outdir}/${assembly}${my_ext})

if [ -s ${outdir}/${assembly}${my_ext} ] && [[ ${file_command_output} != *" XML "* ]] && [[ ${file_command_output} != *" XHTML "* ]]; then

    printf "\r\t  Successfully downloaded: $assembly"

else

    printf "\n     ${RED}******************************* ${NC}NOTICE ${RED}*******************************${NC}  \n"
    printf "\t    $assembly's $format file didn't download successfully.\n"
    printf "\t    That file type may not exist for this accession.\n\n"
    printf "\t    Written to \"NCBI-accessions-not-downloaded.txt\".\n"
    printf "     ${RED}********************************************************************** ${NC}\n\n"

    echo ${assembly} >> ${outdir}/NCBI-accessions-not-downloaded.txt

    rm -rf ${outdir}/${assembly}${my_ext}

fi