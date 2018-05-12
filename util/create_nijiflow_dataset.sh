#/bin/bash

python3 models/research/slim/create_niji_dataset.py \
	--output_dir=./drive/fleetclassify_dataset \
	${HOME}/pixiv_data/image__艦これ/nijiflow_data/nijiflow.list \
	${HOME}/pixiv_data/image__アズールレーン/nijiflow_data/nijiflow.list

