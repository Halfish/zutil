import torch.nn as nn


class ConvBlockModule(nn.Sequential):
    '''
    fast convolution layer builder
    '''
    def __init__(self,
                 dims=[3, 16, 32, 64],
                 kernel_size=(3, 3),
                 pooling_size=(2, 2),
                 prefix='basic',
                 basic_layers='conv, batchnorm, relu, pooling'):
        super(ConvBlockModule, self).__init__()
        self.basic_layers = map(str.strip, basic_layers.split(','))
        assert set(self.basic_layers) <= {'conv', 'batchnorm', 'relu', 'pooling'} , 'unsupported layers'

        for i in range(len(dims) - 1):
            name_prefix = prefix + '_' + str(i+1) + '_'
            for layer in self.basic_layers:
                if layer == 'conv':
                    self.add_module(name_prefix + 'conv', nn.Conv2d(dims[i], dims[i+1], kernel_size))
                elif layer == 'batchnorm':
                    self.add_module(name_prefix + 'batchnorm', nn.BatchNorm2d(dims[i+1]))
                elif layer == 'relu':
                    self.add_module(name_prefix + 'relu', nn.ReLU())
                elif layer == 'pooling':
                    self.add_module(name_prefix + 'maxpool', nn.MaxPool2d(pooling_size,))


if __name__ == '__main__':
    block = ConvBlockModule()
    print(block)
