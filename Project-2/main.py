from tools.stock import *
#from tools.news import *
from tools.data import *

from networks.lstmmlp import LSTMMLP

from config import get_config

import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable

import pdb

class Model(object):
    def __init__(self, config, train_loader = None, test_loader = None):
        self.config  = config
        self.train_loader = train_loader
        self.test_loader = test_loader

    # build lstm-mlp model
    def build(self):
        # network
        self.lstmmlp = LSTMMLP(config.input_size, config.hidden_size, config.batch_size).cuda()
    
        # loss function
        self.loss_function = nn.MSELoss()
    
        # optimizer
        self.optimizer = optim.Adam(self.lstmmlp.parameters(), lr = config.learning_rate)
        # set training mode
        self.lstmmlp.train()

    # training
    def train(self):
        for epoch_i in range(self.config.n_epochs):
            for batch_i, (feature, label) in enumerate(self.train_loader):

                output = self.lstmmlp(Variable(feature.cuda()))
                label = Variable(label.cuda())

                loss = self.loss_function(output, label)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                print(loss.cpu().data.numpy())

    # testing
    def test(self):
        for batch_i, (feature, label) in enumerate(self.test_loader):
            output = self.lstmmlp(Variable(feature.cuda()))

            print('prediction: ', end = '')
            print(output.data.cpu().numpy())
            print('ground-truth: ', end = '')
            print(label)

if __name__ == '__main__':
    
    # get config
    config = get_config()
    
    #get_news_title(config.news_raw_dir, config.news_title_dir)
    #get_tags(config.news_title_dir, config.news_tag_dir)
    #word_to_vector(config.news_tag_dir, config.news_word2vec_dir, config.word2vec_model_path)
    
    company = 'google'
    #create_dataset(config.news_word2vec_dir, config.stock_diff_dir, company, config.fea_label_dir)

    train_data_dir = config.fea_label_dir + '/' + company
    train_loader = feature_loader(train_data_dir, config.batch_size, mode = 'train')

    test_data_dir = config.fea_label_dir + '/' + company
    test_loader = feature_loader(test_data_dir, config.batch_size, mode = 'test')
    
    model = Model(config, train_loader, test_loader)

    model.build()

    model.train()

    model.test()

    #filename = '/home/aaron/Documents/Courses/440/dataset/stock/avg/google.csv'
    #norm_price(filename)
    #diff_price(filename)
