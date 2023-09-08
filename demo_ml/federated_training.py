import numpy as np
from fedbiomed.common.training_plans import FedSGDRegressor
from fedbiomed.common.data import DataManager
from fedbiomed.researcher.experiment import Experiment
from fedbiomed.researcher.aggregators.fedavg import FedAverage

model_args = {
    'eta0':5e-3,
    'n_features': 4,
    'penalty': None,
    'random_state': 12342,
    'feature_cols': ['PM25', 'dummy_male', 'age', 'cbmi'],
    'target_cols': ['blood_pre'],
    'X_fed_mean': [ 1.1655,  0.52336,  4.2187, 16.213],
    'X_fed_std': [0.037987, 0.49945 , 0.15293, 1.6210],
}

training_args = {
    'num_updates': 500,
    'batch_size': 5,
    'log_interval': 100
}

tags =  ['eucaim_demo_ml']
num_rounds = 20

class SGDRegressorTrainingPlan(FedSGDRegressor):
    def training_data(self, batch_size):
        dataset = pd.read_csv(self.dataset_path)

        # create dummy male variable
        dataset['dummy_male'] = (dataset['sex'] == 'male').astype(int)

        # select feature columns
        dataset = dataset[self.model_args()['feature_cols'] + self.model_args()['target_cols']]

        # drop NaN values
        dataset = dataset.dropna(axis=0)
        
        # convert to numpy array
        X = dataset[self.model_args()['feature_cols']].values
        y = dataset[self.model_args()['target_cols']].values

        # normalize feature values
        X = (X - np.array(self.model_args()['X_fed_mean']))/np.array(self.model_args()['X_fed_std'])
        
        return DataManager(dataset=X, 
                           target=y, 
                           batch_size=batch_size, 
                           shuffle=True)


# Define the training experiment
exp = Experiment(tags=tags,
                 model_args=model_args,
                 training_plan_class=SGDRegressorTrainingPlan,
                 training_args=training_args,
                 round_limit=num_rounds,
                 aggregator=FedAverage(),
                 node_selection_strategy=None,
                 skip_data_quality_check=True)

# Run the training
exp.run()

# Extract regression parameters
params = exp.aggregated_params()[num_rounds-1]['params']

# Scale back to unnormalized values
intercept = params['intercept_'] - np.dot(np.array(model_args['X_fed_mean']), params['coef_']/np.array(model_args['X_fed_std']))
coef = np.array(params['coef_'])/np.array(model_args['X_fed_std'])

print(f'Intercept: {intercept}')
for feature_col_name, coef in zip(model_args['feature_cols'], coef):
    print(f'{feature_col_name}: {coef}')
