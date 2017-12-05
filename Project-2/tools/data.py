import os
import h5py
import csv
import numpy as np

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
                    dest_h5_dir = fea_label_dir + '/' + tokens[-1]
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
                    

