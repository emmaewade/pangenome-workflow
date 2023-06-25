#!/usr/bin/perl
#function: converting GenBank file into FASTA file.

#Copy (C) 2018-2019 Massey University. All rights reserved
#Written by Ji Zhang, MD, PhD

# Revision notes
# Changed from output file to output directory
# Added gunzip capability

use Bio::SeqIO;
use IO::Uncompress::Gunzip;

my $usage = "Example: perl gbk2fasta.pl in.gbff.gz outdir\n";
my $infile = shift or die $usage;
my $outdir = shift or die $usage;

my ($base) = $infile =~ /([^\/\\]+)\.gz$/;
my $outfile = $outdir . '/' . $base . '.fa';

# Create a new Gunzip object to read the compressed file
my $gz = IO::Uncompress::Gunzip->new($infile) or die "Cannot open $infile: $!\n";

my $seqin = Bio::SeqIO->new(-fh => $gz, -format => 'Genbank');
my $seqout = Bio::SeqIO->new(-file => ">$outfile", -format => 'Fasta');

while (my $inseq = $seqin->next_seq) {
   $seqout->write_seq($inseq);
}

# Close the input file handle
$gz->close();

print "Conversion complete. FASTA file saved as $outfile.\n";
