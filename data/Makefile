# canonical transcripts per gene id and per hugo symbol

ensembl_biomart_geneids_grch37.p13.transcript_info.txt: ensembl_biomart_geneids_grch37.p13.txt
	cd ../scripts && python download_transcript_info_from_ensembl.py > ../data/$@

ensembl_biomart_transcripts.txt: ensembl_biomart_geneids_grch37.p13.transcript_info.txt
	csvcut -tc transcript_stable_id,gene_stable_id,hgnc_symbol,protein_stable_id,protein_length $< | csvsort -c transcript_stable_id,gene_stable_id,protein_stable_id,protein_length | uniq | csvformat -T > $@

Homo_sapiens.GRCh37.gff3.gz:
	curl ftp://ftp.ensembl.org/pub/grch37/release-91/gff3/homo_sapiens/Homo_sapiens.GRCh37.87.gff3.gz > $@

ensembl_exon_info.txt: Homo_sapiens.GRCh37.gff3.gz
	cd ../scripts && python transform_gff_to_tsv_for_exon_info_from_ensembl.py ../data/$< > ../data/$@

ensembl_biomart_transcripts.json.gz: ensembl_biomart_transcripts.txt ensembl_biomart_pfam_grch37.p13.txt ensembl_exon_info.txt
	cd ../scripts && python add_domains_hugo_exon_info_to_ensembl_transcript.py $(foreach file,$^,../data/$(file)) | gzip -c > ../data/$@

# give default/canonical geneid/transcript based on given hugo symbol takes
# about 50m to run (TODO: this can be easilty optimized)
ensembl_biomart_canonical_transcripts_per_hgnc.txt: ensembl_biomart_geneids_grch37.p13.transcript_info.txt isoform_overrides_uniprot.txt isoform_overrides_at_mskcc.txt isoform_overrides_genome_nexus.txt hgnc.txt
	cd ../scripts && python make_one_canonical_transcript_per_gene.py > ../data/$@

hgnc.txt: 20180321_hgnc_symbols.txt
	 (head -1 $< | tr '[:upper:]' '[:lower:]' | sed -E 's/\([a-z ]*\)//g' | sed 's/\ /_/g'; tail -n +2 $< | grep -v '~withdrawn') > $@

# vcf2maf canonical transcripts
VCF2MAF_RAW_URL=https://raw.githubusercontent.com/mskcc/vcf2maf/v1.6.16
isoform_overrides_uniprot.txt:
	curl '$(VCF2MAF_RAW_URL)/data/isoform_overrides_uniprot_from_biomart_91' | sed 's/^#//' > $@

isoform_overrides_at_mskcc.txt:
	curl '$(VCF2MAF_RAW_URL)/data/isoform_overrides_at_mskcc' | sed 's/^#//' | sed 's/dmp_refseq_id/refseq_id/' | sed 's/isoform_override/enst_id/g' > $@

export: ensembl_biomart_canonical_transcripts_per_hgnc.txt ensembl_biomart_transcripts.json.gz
	cp $^ export/

all: ensembl_biomart_geneids_grch37.p13.transcript_info.txt ensembl_biomart_geneids_grch37.p13.transcript_info.txt ensembl_biomart_canonical_transcripts_per_hgnc.txt isoform_overrides_uniprot.txt isoform_overrides_at_mskcc.txt ensembl_biomart_transcripts.json.gz hgnc.txt

.PHONY: all export
