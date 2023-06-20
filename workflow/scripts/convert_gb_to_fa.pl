#!/usr/bin/perl
#function: converting GenBank file into FASTA file.

#Copy (C) 2018-2019 Massey University. All rights reserved
#Written by Ji Zhang, MD, PhD

#Revision notes

use strict;
use warnings;
use Bio::SeqIO;

my $usage = "Example: perl gbk2fasta.pl in.gbk.gz out_directory/\n";
my $gzipped_file = shift or die $usage;
my $output_dir = shift or die $usage;

my ($base) = $gzipped_file =~ /([^\/\\]+)\.gz$/;
my $outfile = $output_dir . '/' . $base . '.fa';

# Decompress the GenBank file
my $cmd = "gzip -d -c $gzipped_file > $base";
system($cmd) == 0 or die "Failed to decompress $gzipped_file: $!";

# Open the decompressed file for reading
open my $fh, '<', $base or die "Cannot open $base: $!";

# Create Bio::SeqIO objects for reading and writing
my $seqin = Bio::SeqIO->new(-fh => $fh, -format => 'Genbank');
my $seqout = Bio::SeqIO->new(-file => ">$outfile", -format => 'Fasta');

# Convert GenBank to FASTA
while (my $inseq = $seqin->next_seq) {
   $seqout->write_seq($inseq);
}

# Close file handles
close $fh;

# Remove the decompressed file
unlink $base or warn "Failed to remove $base: $!";

#print "Converted $gzipped_file to $outfile\n";
