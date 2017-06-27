import json
import re


class Config(object):
    '''
    class for configures and parameters
    '''
    def __init__(self, source={}, overwrite=False, **args):
        super(Config, self).__init__()
        if isinstance(source, str):
            with open(source, 'r') as f:
                line = ''.join([re.sub('#.+', '', line) for line in f.readlines()])
                try:
                    source = json.loads(line)
                except:
                    print line
                    raise ValueError('Invalid json, please check your json file')
        source = source is None and {} or source
        assert isinstance(source, dict), 'must be dict or valid json'
        self.store = source
        self.overwrite = overwrite
        for key, value in args.iteritems():
            self.store[key] = value

    def __getitem__(self, key):
        assert isinstance(key, str), 'key of parameter must be str type!'
        if not self.store.has_key(key):
            raise KeyError('no such parameter as ' + key + ' in Config')
        return self.store[key]

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setitem__(self, key, value, overwrite=None):
        overwrite = overwrite or self.overwrite
        if self.store.has_key(key) and overwrite == False:
            raise ValueError('key already exist, maybe you should set overwrite to True')
        self.store[key] = value

    def __getstate__(self):
        return self.store

    def __setstate__(self, store):
        self.store = store

    def __repr__(self):
        return self.store.__repr__()

    def select(self, keys, strict=True):
        if isinstance(keys, str):
            keys = map(str.strip, keys.split(','))
        if not strict:
            keys = filter(self.store.has_key, keys)
        assert isinstance(keys, list), 'only accept str or list!'
        source = dict([(key, self.store[key]) for key in keys])
        return Config(source)

    def update(self, **args):
        for key, value in args.iteritems():
            self.__setitem__(key, value, overwrite=True)
        return self

    def copy(self, **args):
        '''
        you should use copy rather than __setitem__ to change config
        '''
        store = self.store.copy()
        for key, value in args.iteritems():
            store[key] = value      # overwrite by force
        return Config(store)

    def __add__(self, y):
        if isinstance(y, Config):
            y = Config.store
        assert isinstance(y, dict), 'only support class of Config or built in dict'
        return self.copy(**y)

    def getdict(self):
        return self.store


def test():
    opt = {'word_emb_dim': 300,
           'filter_num': 32,
           'dropout_rate': 0.5,
           'num_layers': 1,
           'cuda': True,
           'max_epoch': 1000,
           'savefreq': 10,
           'batch_size': 100,
           'learning_rate': 1e-2,
           }

    # init from dict
    config = Config(source=opt, overwrite=True, woqu='woququ')
    print config['woqu']

    print config['savefreq']    # test __getitem__
    config['savefreq'] = 1000   # test __setitem__
    print config.savefreq       # test __getattr__
    print config                # test __repr__

    config1 = Config(source='parameters.json')
    print config1

    # test select function
    config2 = config.select('savefreq, learning_rate, max_epppoch', strict=False)
    print type(config2), config2

    # test update function
    config3 = config.update(savefreq=5000)
    print type(config3), config3 == config

    # test copy function
    config4 = config.copy(savefreq=6000)
    print type(config4), config4 == config

    # test __add__ operator
    config5 = Config({'name':'Bruce'}) + {'whahahah':'youhouhouhou'}
    print type(config5), config5


if __name__ == '__main__':
    test()
