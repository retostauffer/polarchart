

def load_mtcars():
    from pandas import read_csv
    return read_csv("mtcars.csv", index_col = 0)