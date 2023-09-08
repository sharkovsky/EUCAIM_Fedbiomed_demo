# EUCAIM_Fedbiomed_demo
Fed-BioMed demonstrator for the EUCAIM project M9 milestone

## Instructions for data providers

### Infrastructure deployment

You may find deployment instructions for Fed-BioMed at the following [link](https://fedbiomed.org/latest/user-guide/deployment/deployment-vpn/#deploy-on-the-node-side). 
Specifically, you should only follow the instructions under the heading "Deploy on the node side". 
Basically, they amount to 
1. building one (or two if you also want the gui) docker image
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
mkdir fedbiomed/etc
cp etc/${data_provider}.json fedbiomed/etc/
cp ../demo_ml/${data_provider}.json fedbiomed/etc
export FEDBIOMED_DIR=$PWD/fedbiomed
```

Then start your node
```bash
cd ${FEDBIOMED_DIR}/envs/vpn/docker
docker-compose exec -u $(id -u) node bash -ci 'export MPSPDZ_IP=$VPN_IP && export MPSPDZ_PORT=14001 && export MQTT_BROKER=10.220.0.2 && export MQTT_BROKER_PORT=1883 && export UPLOADS_URL="http://10.220.0.3:8000/upload/" && export PYTHONPATH=/fedbiomed && export FEDBIOMED_NO_RESET=1 && eval "$(conda shell.bash hook)" && conda activate fedbiomed-node && bash'
```

This will open a shell on the container. From that shell you can add a dataset
```bash
data_provider=bsc  # other options: ub, forth
./scripts/fedbiomed_run node config ${data_provider}.ini --add-dataset-from-file ./etc/${data_provider}.json
```

Start the node in the background
```bash
nohup ./scripts/fedbiomed_run node start >./fedbiomed_node.out &
```



#### ML demo




