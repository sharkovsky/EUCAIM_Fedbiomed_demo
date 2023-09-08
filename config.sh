#! /bin/sh

git clone --depth 1 --branch v4.4.3 git@github.com:fedbiomed/fedbiomed.git

mkdir fedbiomed/etc
cp etc/* fedbiomed/etc/

git clone --depth 1 git@github.com:EUCAIM/demo_ml_data.git fedbiomed/envs/vpn/docker/node/run_mounts/data/
git clone --depth 1 git@github.com:EUCAIM/demo_dl_data.git fedbiomed/envs/vpn/docker/node/run_mounts/data/
wget -p fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_dl_data https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia/download?datasetVersionNumber=2

cp demo_ml/*.json fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_ml_data

cd fedbiomed
for data_provider in bsc ub forth
do
	./scripts/fedbiomed_run node config ${data_provider}.ini --add-dataset-from-file envs/vpn/docker/node/run_mounts/data/demo_ml_data/${data_provider}.json
done



