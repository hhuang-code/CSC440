import csv

"""
normalize stock price, use formula: ((open + close) - (high + low)) / (high - low)
Args:
    filename: a stock price file, csv format: [Date, Open, High, Low, Close]
"""
def norm_price(filename):
    dest_filename = filename.replace('raw', 'avg')  # change folder
    with open(filename, 'r') as rf, open(dest_filename, 'w') as wf:
        reader = csv.reader(rf)
        next(reader, None)  # skip the header
        wf.write('Date,Price\n')   # write the header
        for row in reader:
            date = row[0].strip()
            open_ = float(row[1].strip())
            high = float(row[2].strip())
            low = float(row[3].strip())
            close_ = float(row[4].strip())
            # calculate average price
            avg_price = ((open_ + close_) - (high + low)) / (high - low)
            wf.write(date + ',' + str(avg_price) + '\n')
        wf.close()
        rf.close()

"""
calculate stock price daily change, use (today's change = next day's price - today's price)
Args:
    filename: a stock price file, csv format: [Date, Price]
"""
def diff_price(filename):
    dest_filename = filename.replace('avg', 'diff') # change folder
    with open(filename, 'r') as rf, open(dest_filename, 'w') as wf:
        reader = csv.reader(rf)
        next(reader, None)  # skip the header
        wf.write('Date,Diff\n') # write the header
        cur_row = []
        next_row = []
        for row in reader:
            next_row = row
            if len(cur_row) == 0: # first sample
                cur_row = next_row
                continue
            else:
                cur_date = cur_row[0].strip()
                cur_price = float(cur_row[1].strip())
                next_price = float(next_row[1].strip())
                # calculate price change
                diff_price = next_price - cur_price
                cur_row = next_row
                wf.write(cur_date + ',' + str(diff_price) + '\n')
        wf.close()
        rf.close()
