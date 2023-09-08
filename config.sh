#! /bin/sh

git clone --depth 1 --branch v4.4.3 git@github.com:fedbiomed/fedbiomed.git

mkdir fedbiomed/etc
cp etc/* fedbiomed/etc/

cd demo_ml
git clone --depth 1 git@github.com:EUCAIM/demo_ml_data.git

cd ../fedbiomed
for data_provide in bsc ub forth
do
	./scripts/fedbiomed_run node config ${data_provider}.ini configuration create
	./scripts/fedbiomed_run node config ${data_provider}.ini --add-dataset-from-file ../demo_ml/${data_provider}.json
done



