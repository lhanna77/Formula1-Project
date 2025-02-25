#!/bin/bash
gcloud config set project mstr-globalbi-sbx-c730
bq.cmd show --schema --format=prettyjson mstr-dwh-dev-83bf:JobApplies.race_circuits > race_circuits.json