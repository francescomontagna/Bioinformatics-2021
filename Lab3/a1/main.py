import subprocess
import os
import pandas as pd

VCF_INPUT = 'sorted_input.vcf'

def process_sam():

    # Compression. convert sam to bami
    subprocess.run('samtools view -S -b input.sam > input.bam', shell = True)

    # Sorting is performed according to what criterion? Slide says 'genomic region'
    subprocess.run('samtools sort input.bam > sorted_input.bam', shell = True)

    # Convert bam to vcf
    subprocess.run('bcftools mpileup --fasta-ref reference_chr10_chr18.fa sorted_input.bam > '
                   + VCF_INPUT, shell = True)

def complete_snp(input_file, output_file):
    """
    Retain only Single Nucleotide Polymorphism (SNP) for which the information is complete
    and store the result in the output_file
    """
    vcf = pd.read_csv(input_file, sep = '\t', header = 22)

    # filter for uncomplete SNP. SNP is uncomplete if ALT = <*>
    snp_mask = vcf.loc[:, 'ALT'] != '<*>'
    indel_mask = vcf.loc[:, 'INFO'].str.contains("INDEL")
    mask = snp_mask & indel_mask
    filtered_vcf = vcf.loc[mask, :]

    filtered_vcf.to_csv(output_file, header = True, sep = '\t', index = False)


if __name__ == '__main__':
    if not os.path.exists(VCF_INPUT):
        process_sam()

    complete_snp(VCF_INPUT, 'filtered_input.vcf')