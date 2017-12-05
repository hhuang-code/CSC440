import os
import h5py
import csv
import numpy as np
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader

import pdb

def create_dataset(news_word2vec_dir, stock_diff_dir, company, fea_label_dir):
    # stock price file
    stock_diff_filename = os.path.join(stock_diff_dir, company + '.csv')
    print(stock_diff_filename)

    for dirpath, dirname, filenames in os.walk(news_word2vec_dir):
        for filename in [f for f in filenames if f.endswith('.h5')]:
            if company.lower() in filename.lower():
                stock_diff = None
                tokens = dirpath.split('/')
                date = tokens[-1]
                # change date format from e.g. 2017-12-04 to 2017-12-4
                if date[-2] == '0':
                    date = date[:-2] + date[-1]
                # change date format from e.g. 2017-02-14 to 2017-2-14
                if date[5] == '0':
                    date = date[:5] + date[6:]
                # get stock price in stock diff file
                with open(stock_diff_filename, 'r') as sf:
                    reader = csv.reader(sf) 
                    next(reader, None)  # skip the header
                    for row in reader:
                        if date in row: # find the date in stock price file
                            stock_diff = float(row[1].strip())
                            print(date)
                            break
                sf.close()
                if stock_diff == None:
                    continue    # no stock price for this day
                else:
                    # open this word2vec .h5 file, add label, and save to another file
                    dest_h5_dir = fea_label_dir + '/' + company + '/' + tokens[-1]  # token[-1] is date
                    if not os.path.exists(dest_h5_dir):
                        os.makedirs(dest_h5_dir)
                    
                    dest_h5_filename = os.path.join(dest_h5_dir, filename)
                    src_h5_filename = os.path.join(dirpath, filename)
                    print(dest_h5_filename)
                    
                    sh5 = h5py.File(src_h5_filename, 'r')
                    dh5 = h5py.File(dest_h5_filename, 'w')  # add stock price as label
                    dh5.create_dataset('feature', data = sh5['feature'])
                    sh5.close()
                    dh5.create_dataset('label', data = np.array([stock_diff]))
                    dh5.close()
                    
"""
transform dataset to a pytorch dataset
"""
class FeatureData(Dataset):
    """
    Args:
        fea_label_dir: a directory containing news title feature and stock price label
    """
    def __init__(self, fea_label_dir):
        self.fea_label_dir =Path(fea_label_dir)
        # find all subfolders and files
        subdir_and_file = self.fea_label_dir.glob('**/*')
        self.fea_label_list = [x for x in subdir_and_file if x.is_file()]

    # return num of features (equal to num of titles)
    def __len__(self):
        return len(self.fea_label_list)

    def __getitem__(self, index):
        fea_label_file = self.fea_label_list[index]
        with h5py.File(fea_label_file, 'r') as f:   # for each title
            feature = torch.Tensor(np.array(f['feature']))
            label = torch.Tensor(np.array(f['label']))
        f.close()

        return feature, label

# generate feature loader according to the given feature directory
def feature_loader(fea_label_dir, batch_size, mode = 'train'):
    if mode.lower() == 'train':
        return DataLoader(FeatureData(fea_label_dir), batch_size = batch_size)
    elif mode.lower() == 'test':
        return DataLoader(FeatureData(fea_label_dir), batch_size = batch_size)
    else:
        raise 'No such mode!'
