import csv

"""
normalize stock price, use formula: ((open + close) - (high + low)) / (high - low)Args:
    filename: a stock price file, csv format: [Date, Open, High, Low, Close]
"""
def norm_price(filename):
    dest_filename = filename.replace('raw', 'avg')
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

"""
        
