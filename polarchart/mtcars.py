

def load_mtcars():
    """load_mtcars()

    The data was extracted from the 1974 _Motor Trend_ US magazine,
    and comprises fuel consumption and 10 aspects of automobile design
    and performance for 32 automobiles (1973-74 models).

    A data frame with 32 observations on 11 (numeric) variables.

    [, 1]  ‘mpg’   Miles/(US) gallon                        
    [, 2]  ‘cyl’   Number of cylinders                      
    [, 3]  ‘disp’  Displacement (cu.in.)                    
    [, 4]  ‘hp’    Gross horsepower                         
    [, 5]  ‘drat’  Rear axle ratio                          
    [, 6]  ‘wt’    Weight (1000 lbs)                        
    [, 7]  ‘qsec’  1/4 mile time                            
    [, 8]  ‘vs’    Engine (0 = V-shaped, 1 = straight)      
    [, 9]  ‘am’    Transmission (0 = automatic, 1 = manual) 
    [,10]  ‘gear’  Number of forward gears                  
    [,11]  ‘carb’  Number of carburetors

    Source
    ======
    Borrowed from the R package 'datasets'; original source: Henderson and
    Velleman (1981), Building multiple regression models interactively.
    _Biometrics_, *37*, 391-411.

    Return
    ======
    pandas.DataFrame : Returns a pandas DataFrame with the test
    data shipped with the package.
    """
    from importlib.resources import files
    from pandas import read_csv

    csv = files("polarchart.data").joinpath("mtcars.csv")
    return read_csv(csv, index_col = 0)
