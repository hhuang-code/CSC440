import argparse

"""
set configuration argument as class attributes
"""

class Config(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

"""
get configuration arguments
"""
def get_config(**kwargs):
    parser = argparse.ArgumentParser()

    # news base
    parser.add_argument('--news_base_dir', type = str, default = '/tmp/440/dataset/news')

    # raw news
    parser.add_argument('--news_raw_dir', type = str, default = '/tmp/440/dataset/news/raw')
    parser.add_argument('--news_bloomberg_dir', type = str, default = '/tmp/440/dataset/news/raw/bloomberg')
    parser.add_argument('--news_reuters_dir', type = str, default = '/tmp/440/dataset/news/raw/reuters')

    # news title
    parser.add_argument('--news_title_dir', type = str, default = '/tmp/440/dataset/news/title')

    # news tag
    parser.add_argument('--news_tag_dir', type = str, default = '/tmp/440/dataset/news/tag')

    # news title word to vector
    parser.add_argument('--news_word2vec_dir', type = str, default = '/tmp/440/dataset/word2vec')

    # word to vector model path
    parser.add_argument('--word2vec_model_path', type = str, default = '/tmp/440/model/GoogleNews-vectors-negative300.bin')

    # stock base
    parser.add_argument('--stock_base_dir', type = str, default = '/tmp/440/dataset/stock')
    
    # raw stock
    parser.add_argument('--stock_raw_dir', type = str, default = '/tmp/440/dataset/stock/raw')

    # average stock price
    parser.add_argument('--stock_avg_dir', type = str, default = '/tmp/440/dataset/stock/avg')

    # change of stock price
    parser.add_argument('--stock_diff_dir', type = str, default = '/tmp/440/dataset/stock/diff')

    args = parser.parse_args()

    # namespace -> dictionary
    args = vars(args)
    args.update(kwargs)

    return Config(**args)
