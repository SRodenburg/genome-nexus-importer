# Genome Nexus Data Importer
This repo contains all the transfromation scripts and data for the mongo
database for genome nexus. 

## Using the mongo database

### Using docker container
There's a mongo docker container that has all the data imported. You can use
the docker compose file in the genome nexus repo itself to start both the web
app and the database: [genome
nexus](https://github.com/genome-nexus/genome-nexus).

### Directly import to mongo database
Run the script [scripts/import_mongo.sh](scripts/imort_mongo.sh). It will
import files from [export/](export/):
```
./scripts/import_mongo.sh mongodb://127.0.0.1:27017/annotator # change accordingly
```

## Update data
### Manually download these files

#### Ensembl Biomart

##### PFAM endpoint

Ensembl Biomart file is required by the PFAM endpoint. In order to download this file
follow these steps:

1. Go to the [Biomart](www.ensembl.org/biomart/martview) page on the Ensemble website.
2. Select `Ensemble Genes` from the `Database` dropdown menu.
3. Select `Human Genes` from the `Dataset` dropdown menu.
4. Click on `Attributes`, and select these ones:
Gene stable ID, Transcript stable Id, Protein stable Id, Gene name, Pfam domain ID, Pfam domain start, Pfam domain end.
5. Click on `Results`, and export all results to a `TSV` file.
6. Copy over the downoaded file to replace [pfamA.txt](pfamA.txt).

##### Ensembl endpoint 
1. Go to Biomart ([grch37.ensembl.org/biomart/martview](grch37.ensembl.org/biomart/martview)) page on the Ensemble website.
2. Select `Ensemble Genes` from the `Database` dropdown menu.
3. Select `Human Genes` from the `Dataset` dropdown menu.
4. Click on `Attributes`, and select these ones:
Gene stable ID, Transcript stable Id, HGNC Symbol, HGNC ID
5. Click on `Results`, and export all results to a `TSV` file.
6. Copy over the downoaded file to replace [ensembl_biomart_geneids_grch37.p13.txt](ensembl_biomart_geneids_grch37.p13.txt).

### Change curl commands
Some data is downloaded automatically through curl commands see
[data/Makefile](data/Makefile). Change those if you want to change the data.

### Download and transform data
```
cd data
make all # takes about 30m from scratch
```
