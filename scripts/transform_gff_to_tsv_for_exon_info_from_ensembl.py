#!/usr/bin/env python3
"""
Copyright (c) 2018 The Hyve B.V.
This code is licensed under the GNU Affero General Public License (AGPL),
version 3, or (at your option) any later version.
"""

import pandas as pd
import sys
import gzip
import argparse


def transform_gff_to_tsv(gff_file, tsv_file):

    # Dataframe to append the transcript information
    transcript_info = pd.DataFrame(columns=['transcript_id', 'type', 'id', 'start', 'end', 'rank', 'strand', 'version'])
    # list to append transcript information per row
    rows = []

    # Open gff file and read lines, when line contains transcript information, extract this information
    with gzip.open(gff_file, 'rt') as gff:
        for line in gff:
            if line[0] != '#':
                list_line = line.strip('\n').split('\t')
                entry_dict = {}

                # Extract UTRs and exons
                if len(list_line) > 1 and list_line[2] in ['exon', 'five_prime_UTR', 'three_prime_UTR']:

                    meta_info = list_line[8].split(';')
                    entry_dict['transcript_id'] = meta_info[0].split(':')[1]
                    entry_dict['type'] = list_line[2]
                    entry_dict['start'] = list_line[3]
                    entry_dict['end'] = list_line[4]
                    strand = list_line[6]
                    # Convert plus strand into 1 and minus strand into -1
                    if strand == '+':
                        entry_dict['strand'] = '1'
                    elif strand == '-':
                        entry_dict['strand'] = '-1'
                    else:
                        entry_dict['strand'] = ''

                    if list_line[2] == 'exon':
                        entry_dict['id'] = meta_info[5].split('=')[1]
                        entry_dict['rank'] = meta_info[6].split('=')[1]
                        entry_dict['version'] = meta_info[7].split('=')[1]
                    else:
                        entry_dict['id'] = ''
                        entry_dict['rank'] = ''
                        entry_dict['version'] = ''
                    rows.append(entry_dict)

    # By first appending it to a list and only adding it to a DF once, performance is greatly improved
    transcript_info = transcript_info.append(rows, ignore_index=True, sort=False)
    transcript_info.to_csv(tsv_file, sep='\t', index=False, compression='gzip')
    return


def main(gff_file):
    tsv_file = "../data/ensembl_transcript_info.txt.gz"
    transform_gff_to_tsv(gff_file, tsv_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform GFF3 file to TSV for exons and UTRs. Output is written to '
                                                 'stdout, as the Makefile wrapper expects.')
    parser.add_argument("gff_file",
                        default="../data/Homo_sapiens.GRCh38.92.gff3.gz",
                        help="Homo_sapiens.GRCh38.92.gff3.gz")
    args = parser.parse_args()

    main(args.gff_file)
