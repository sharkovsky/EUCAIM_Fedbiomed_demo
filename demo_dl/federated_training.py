import torch
import torch.nn as nn
from torchvision import datasets, transforms
from fedbiomed.common.training_plans import TorchTrainingPlan
from fedbiomed.common.data import DataManager
from fedbiomed.researcher.experiment import Experiment
from fedbiomed.researcher.aggregators.fedavg import FedAverage


class MyTrainingPlan(TorchTrainingPlan):
    
    def init_dependencies(self):
        deps = ["from torchvision import datasets, transforms",
                "import torch.nn as nn"]

        return deps
        
    def init_model(self, model_args):
    
        class CnnModel(nn.Module):
            def __init__(self, num_classes=2):
                super(CnnModel, self).__init__()

                self.conv1 = nn.Conv2d( in_channels = 3, out_channels = 12, kernel_size = 3, stride = 1, padding = 1 )
                self.bn1   = nn.BatchNorm2d( num_features = 12 )
                self.relu1 = nn.ReLU()   
                self.pool  = nn.MaxPool2d( kernel_size = 2 )
                self.conv2 = nn.Conv2d( in_channels = 12, out_channels = 20, kernel_size = 3, stride = 1, padding = 1 )
                self.relu2 = nn.ReLU()
                self.conv3 = nn.Conv2d( in_channels = 20, out_channels = 32, kernel_size = 3, stride = 1, padding = 1 )
                self.bn3   = nn.BatchNorm2d( num_features = 32 )
                self.relu3 = nn.ReLU()
                self.fc    = nn.Linear( in_features = 32 * 112 * 112, out_features = num_classes )

            def forward( self, input ):
                output = self.conv1( input )
                output = self.bn1( output )
                output = self.relu1( output )
                output = self.pool( output )
                output = self.conv2( output )
                output = self.relu2( output )
                output = self.conv3( output )
                output = self.bn3( output )
                output = self.relu3( output )            
                output = output.view( -1, 32*112*112 )
                output = self.fc( output )
                return output
            
        model = CnnModel()
        self.loss_f = nn.CrossEntropyLoss()
        return model 

    
    def init_optimizer(self, optimizer_args):
        return torch.optim.Adam(self.model().parameters())
    
    def training_data(self, batch_size):
        preprocess = transforms.Compose([transforms.ToTensor(),
                                         transforms.Resize([224, 224])
                                        ])
        train_data = datasets.ImageFolder(self.dataset_path, transform = preprocess)
        train_kwargs = {'batch_size': batch_size, 'shuffle': True}
        return DataManager(dataset=train_data, **train_kwargs)
    
    def training_step(self, data, target):
        output = self.model().forward(data)
        loss   = self.loss_f(output, target)
        return loss

model_args = {}

training_args = {
    'batch_size': 8, 
    'num_updates': 1,
}

tags =  ['eucaim_dl_demo']
num_rounds = 2

exp = Experiment(tags=tags,
                 training_plan_class=MyTrainingPlan,
                 model_args=model_args,
                 training_args=training_args,
                 round_limit=num_rounds,
                 aggregator=FedAverage(),
                 node_selection_strategy=None)


exp.run()
