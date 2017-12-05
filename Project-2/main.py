from tools.stock import *
from tools.news import *
from tools.data import *

from config import get_config

if __name__ == '__main__':
    
    # get config
    config = get_config()
    
    #get_news_title(config.news_raw_dir, config.news_title_dir)
    #get_tags(config.news_title_dir, config.news_tag_dir)
    #word_to_vector(config.news_tag_dir, config.news_word2vec_dir, config.word2vec_model_path)
    
    company = 'google'
    create_dataset(config.news_word2vec_dir, config.stock_diff_dir, company, config.fea_label_dir)
        
    #filename = '/home/aaron/Documents/Courses/440/dataset/stock/avg/google.csv'
    #norm_price(filename)
    #diff_price(filename)
