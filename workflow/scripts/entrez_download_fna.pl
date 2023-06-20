use LWP::Simple;
use Getopt::Long;

# Get the filename and output directory from command line arguments
my ($accession_file, $output_dir);
GetOptions(
    "file=s" => \$accession_file,
    "output=s" => \$output_dir
);

# Check if the filename and output directory arguments are provided
unless ($accession_file && $output_dir) {
    die "Error: Please provide a filename containing the list of accession numbers using --file option, and the output directory using --output option.\n";
}

# Batch size for downloading sequences
my $batch_size = 10;

# Read the accession numbers from the file
open(my $fh, '<', $accession_file) or die "Error: Can't open file $accession_file: $!\n";
my @accession_numbers = <$fh>;
close($fh);

# Remove newline characters and leading/trailing whitespaces
chomp(@accession_numbers);
s/\s+//g for @accession_numbers;

# Create the output directory if it doesn't exist
mkdir $output_dir unless -d $output_dir;

# Loop through the accession numbers in batches
for (my $i = 0; $i < scalar(@accession_numbers); $i += $batch_size) {
    # Determine the range of accession numbers for the current batch
    my $start_index = $i;
    my $end_index = $i + $batch_size - 1;
    $end_index = scalar(@accession_numbers) - 1 if $end_index >= scalar(@accession_numbers);
    my @current_batch = @accession_numbers[$start_index..$end_index];

    # Assemble the esearch URL
    my $query = join('+OR+', map { $_ . '[acc]' } @current_batch);
    my $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    my $url = $base . "esearch.fcgi?db=nucleotide&term=$query&usehistory=y";

    # Post the esearch URL
    my $output = get($url);

    # Parse WebEnv, QueryKey and Count (# records retrieved)
    my ($web) = $output =~ /<WebEnv>(\S+)<\/WebEnv>/;
    my ($key) = $output =~ /<QueryKey>(\d+)<\/QueryKey>/;
    my ($count) = $output =~ /<Count>(\d+)<\/Count>/;

    # Retrieve data for the current batch
    my $retmax = $end_index - $start_index + 1;
    my $retstart = 0;
    my $efetch_url = $base ."efetch.fcgi?db=nucleotide&WebEnv=$web";
    $efetch_url .= "&query_key=$key&retstart=$retstart";
    $efetch_url .= "&retmax=$retmax&rettype=fasta&retmode=text";
    my $efetch_out = get($efetch_url);

    # Save FASTA sequences to separate files
    foreach my $accession (@current_batch) {
        my $filename = $output_dir . '/' . $accession . ".fasta";
        open(OUT, ">$filename") || die "Can't open file $filename!\n";
        my ($seq) = $efetch_out =~ /^>.*$accession.*\n(.+)/ms;
        print

