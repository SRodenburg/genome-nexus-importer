# Genome Nexus Data Importer
This repo contains all the transformation scripts and data to set up the mongo
database for genome nexus. 

## Using the mongo database

### Using docker container
There's a mongo docker container that has all the data imported. You can use
the docker compose file in the genome nexus repo itself to start both the web
app and the database: [genome
nexus](https://github.com/genome-nexus/genome-nexus).

### Directly import to mongo database
Run the script [scripts/import_mongo.sh](scripts/import_mongo.sh) to import processed data files into a running 
database. When running this script, please specify:
- mongo database address, for example `mongodb://127.0.0.1:27017/annotator`.
- Reference Genome and Ensembl Release, for example `grch37_ensembl92` or `grch38_ensembl92`. Files are imported from 
`data/<refgenome_ensemblversion>/export/`.

Example:
```bash
./scripts/import_mongo.sh mongodb://127.0.0.1:27017/annotator grch37_ensembl92
```

## Update data

### Create folders
- `data/<refgenome_ensemblversion>/input`
- `data/<refgenome_ensemblversion>/export`
- `data/<refgenome_ensemblversion>/tmp`

The `input` and `export` folders are tracked by Git, while the `tmp` folder contains the intermediate files and is not 
tracked by Git.

### Manually download Ensembl BioMart files

- GRCh37 / hg19: https://grch37.ensembl.org/biomart
- GRCh38 / hg38: https://www.ensembl.org/biomart

http://www.ensembl.org/Help/ArchiveList contains archived BioMart releases.

##### PFAM endpoint
Ensembl Biomart file is required by the PFAM endpoint. In order to download this file
follow these steps:

1. Go to the Ensemble BioMart website of the reference genome and Ensembl Release of interest.
2. Select `Ensemble Genes` from the `Database` dropdown menu.
3. Select `Human Genes` from the `Dataset` dropdown menu.
4. Click on `Attributes`, and select these ones:
Gene stable ID, Transcript stable Id, Protein stable Id, Gene name, Pfam domain ID, Pfam domain start, Pfam domain end.
5. Click on `Results`, and export all results to a `TSV` file.
6. Save the downloaded file as `ensembl_biomart_pfam.txt` in `data/<refgenome_ensemblversion>/input`.

##### Ensembl endpoint 
1. Go to the Ensemble BioMart website of the reference genome and Ensembl Release of interest.
2. Select `Ensemble Genes` from the `Database` dropdown menu.
3. Select `Human Genes` from the `Dataset` dropdown menu.
4. Click on `Attributes`, and select these ones:
Gene stable ID, Transcript stable Id, HGNC Symbol, HGNC ID
5. Click on `Results`, and export all results to a `TSV` file.
6. Save the downloaded file as `ensembl_biomart_geneids.txt` in `data/<refgenome_ensemblversion>/input`.

##### Ensembl endpoint RefSeq identifiers
1. Go to the Ensemble BioMart website of the reference genome and Ensembl Release of interest.
2. Select `Ensemble Genes` from the `Database` dropdown menu.
3. Select `Human Genes` from the `Dataset` dropdown menu.
4. Click on `Attributes`, and select these ones:
Transcript stable Id, RefSeq mRNA ID
5. Click on `Results`, and export all results to a `TSV` file.
6. Save the downloaded file as `ensembl_biomart_refseq.txt` in `data/<refgenome_ensemblversion>/input`.

##### Ensembl endpoint CCDS identifiers
1. Go to the Ensemble BioMart website of the reference genome and Ensembl Release of interest.
2. Select `Ensemble Genes` from the `Database` dropdown menu.
3. Select `Human Genes` from the `Dataset` dropdown menu.
4. Click on `Attributes`, and select these ones:
Transcript stable Id, CCDS ID
5. Click on `Results`, and export all results to a `TSV` file.
6. Save the downloaded file as `ensembl_biomart_ccds.txt` in `data/<refgenome_ensemblversion>/input`.

## Download and transform data
To run the pipeline that transforms all intermediate data, run the following. This takes _roughly two hours_ to complete.

```bash
cd data
make all
```

During this process, every transcript in `ensembl_biomart_geneids.txt` is assessed to be either canonical or not, by 
querying the Ensembl REST API. This takes a while, because only 1000 transcripts can be queried at a time. Progress can 
be viewed by inspecting the temporary files created in  `data/<refgenome_ensemblversion>/tmp/transcript_info`. Gene 
source file `ensembl_biomart_geneids.txt` contains about _224596_ transcripts, so the pipeline will save about _225_ 
of these files.

## Verify data
To verify the pipeline ran data for the correct reference genome, you can verify the exon coordinates in
`export/ensembl_biomart_transcripts.json.gz`. Select an Ensembl Exon ID, query it on Ensembl GRCh38 or GRCh37, select
the gene, select transcript, and select 'Exons'. This will display all the exons of the transcript and their genomic
coordinates.