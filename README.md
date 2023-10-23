# EUCAIM_Fedbiomed_demo
Fed-BioMed demonstrator for the EUCAIM project M9 milestone

## Instructions for data providers

First, clone the fedbiomed directory
```bash
git clone --branch master git@github.com:fedbiomed/fedbiomed.git
export FEDBIOMED_DIR=$PWD/fedbiomed
```

### Infrastructure deployment

You may find deployment instructions for Fed-BioMed at the following [link](https://fedbiomed.org/latest/user-guide/deployment/deployment-vpn/#deploy-on-the-node-side). 
Specifically, you should only follow the instructions under the heading "Deploy on the node side". 
Basically, they amount to 
1. building one docker image (you may only build the `node` image, and avoid the `gui` image)
2. copying a vpn configuration file to a predefined path/name in the docker container
3. generating a public vpn key

To obtain the vpn configuration file, please contact [francesco.cremonesi@inria.fr](mailto:francesco.cremonesi@inria.fr).
When the public key has been generated, please send it to [francesco.cremonesi@inria.fr](mailto:francesco.cremonesi@inria.fr), so it can be registered on the vpn server. 

Some additional information:

- the documentation says to checkout the master branch of fedbiomed. You may alternatively checkout the v4.4.4 tag (or any higher available tag if we push more in the meantime). In any case, the master branch is fine since it is up to date with the latest hotfixes required for correctly building the docker images
- using the GUI is fully optional. In case you don’t want to do it, then obviously there is no need to build the corresponding image 

### Uploading data

Copy the node's configuration provided in the repo to the fedbiomed directory

```bash
data_provider=bsc  # other options: ub, forth
cp etc/${data_provider}.ini fedbiomed/envs/vpn/docker/node/run_mounts/etc
```

#### ML demo

Clone the data directory
```bash
git clone git@github.com:EUCAIM/demo_ml_data.git fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_ml_data
```

Copy the dataset configuration files to the appropriate location (each data provider has a specific file)
```bash
data_provider=bsc  # other options: ub, forth
cp ../demo_ml/${data_provider}.json fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_ml_data/
```

Then start your node
```bash
cd ${FEDBIOMED_DIR}/envs/vpn/docker
docker-compose exec -u $(id -u) node bash -ci 'export MPSPDZ_IP=$VPN_IP && export MPSPDZ_PORT=14001 && export MQTT_BROKER=10.220.0.2 && export MQTT_BROKER_PORT=1883 && export UPLOADS_URL="http://10.220.0.3:8000/upload/" && export PYTHONPATH=/fedbiomed && export FEDBIOMED_NO_RESET=1 && eval "$(conda shell.bash hook)" && conda activate fedbiomed-node && bash'
```

This will open a shell on the container. From that shell you can add a dataset
```bash
./scripts/fedbiomed_run node config ${data_provider}.ini --add-dataset-from-file /data/demo_ml_data/${data_provider}.json
```

Start the node in the background
```bash
nohup ./scripts/fedbiomed_run node config ${data_provider}.ini start >./fedbiomed_node.out &
```


#### DL demo

Clone the data directory
```bash
git clone git@github.com:EUCAIM/demo_ml_data.git fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_dl_data
```

Download the dataset from [kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia), and extract its contents.
Then you need to change the directory structure:
```bash
PATH_TO_DOWNLOADED_DATA=<input here the path to where you extracted the archived data>
CSV_FILE_ID=2_1  # 2_1 for bsc, 2_2 for forth
while read img; do
  mv $PATH_TO_DOWNLOADED_DATA/chest_xray/train/PNEUMONIA/$img fedbiomed/envs/vpn/docker/node/run_mounts/data/chest_xray/PNEUMONIA/$img
done < <(tail -n +2 fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_dl_data/data_ids/two_datasites_scenario/train.pnm.${CSV_FILE_ID}.csv)

while read img; do
  mv $PATH_TO_DOWNLOADED_DATA/chest_xray/train/NORMAL/$img fedbiomed/envs/vpn/docker/node/run_mounts/data/chest_xray/NORMAL/$img
done < <(tail -n +2 fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_dl_data/data_ids/two_datasites_scenario/train.nrm.${CSV_FILE_ID}.csv)
```

Copy the dataset configuration files to the appropriate location (the same file for all data providers)
```bash
cp ../demo_dl/dataset.json fedbiomed/envs/vpn/docker/node/run_mounts/data/demo_dl_data/
```

Then start your node
```bash
cd ${FEDBIOMED_DIR}/envs/vpn/docker
docker-compose exec -u $(id -u) node bash -ci 'export MPSPDZ_IP=$VPN_IP && export MPSPDZ_PORT=14001 && export MQTT_BROKER=10.220.0.2 && export MQTT_BROKER_PORT=1883 && export UPLOADS_URL="http://10.220.0.3:8000/upload/" && export PYTHONPATH=/fedbiomed && export FEDBIOMED_NO_RESET=1 && eval "$(conda shell.bash hook)" && conda activate fedbiomed-node && bash'
```

This will open a shell on the container. From that shell you can add a dataset
```bash
./scripts/fedbiomed_run node config ${data_provider}.ini --add-dataset-from-file /data/demo_dl_data/dataset.json
```

Start the node in the background
```bash
nohup ./scripts/fedbiomed_run node config ${data_provider}.ini start >./fedbiomed_node.out &
```

## Instructions for the data scientist

First clone fedbiomed if you haven't done so yet
```bash
git clone --branch master git@github.com:fedbiomed/fedbiomed.git
export FEDBIOMED_DIR=$PWD/fedbiomed
cd envs/vpn/docker
```

Build the container
```bash
${FEDBIOMED_DIR}/scripts/fedbiomed_vpn build researcher
```

Copy the VPN configuration file that was provided to you via email to the appropriate location
```bash
cp config.env ./researcher/run_mounts/config/config.env
```

Retrieve the public key
```bash
docker-compose exec researcher wg show wg0 public-key | tr -d '\r' >/tmp/publickey-researcher
```

Send the public key via email to [francesco.cremonesi@inria.fr](mailto:francesco.cremonesi@inria.fr).

Create the fedbiomed configuration for the researcher
```bash
docker-compose exec -u $(id -u) researcher bash -ci 'export MPSPDZ_IP=$VPN_IP && export MPSPDZ_PORT=14001 && export MQTT_BROKER=10.220.0.2 && export MQTT_BROKER_PORT=1883 && export UPLOADS_URL="http://10.220.0.3:8000/upload/" && export PYTHONPATH=/fedbiomed && export FEDBIOMED_NO_RESET=1 && eval "$(conda shell.bash hook)" && conda activate fedbiomed-researcher && ./scripts/fedbiomed_run researcher configuration create'
```

Copy the training files to the appropriate location

```bash
mkdir ${FEDBIOMED_DIR}/envs/vpn/docker/researcher/run_mounts/samples/demo_ml/
mkdir ${FEDBIOMED_DIR}/envs/vpn/docker/researcher/run_mounts/samples/demo_dl/
cp ${EUCAIM_DEMO_DIR}/demo_ml/federated_training.py ${FEDBIOMED_DIR}/envs/vpn/docker/researcher/run_mounts/samples/demo_ml/
cp ${EUCAIM_DEMO_DIR}/demo_dl/federated_training.py ${FEDBIOMED_DIR}/envs/vpn/docker/researcher/run_mounts/samples/demo_dl/
```

Finally, start the container

```bash
docker-compose exec -u $(id -u) researcher bash -ci 'export MPSPDZ_IP=$VPN_IP && export MPSPDZ_PORT=14000 && export MQTT_BROKER=10.220.0.2 && export MQTT_BROKER_PORT=1883 && export UPLOADS_URL="http://10.220.0.3:8000/upload/" && export PYTHONPATH=/fedbiomed && export FEDBIOMED_NO_RESET=1 && eval "$(conda shell.bash hook)" && conda activate fedbiomed-researcher && bash'
```

From within the container, you may run the federated training
```bash
python /fedbiomed/notebooks/samples/demo_ml/federated_training.py
```


