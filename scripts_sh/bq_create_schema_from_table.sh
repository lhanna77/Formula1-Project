#!/bin/bash
gcloud config set project mstr-globalbi-sbx-c730
bq.cmd show --schema --format=prettyjson mstr-globalbi-sbx-c730:lh_f1_silver.results > results.json