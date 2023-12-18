import pandas as pd

a = pd.DataFrame(columns = ['a', 'b'])
a = pd.concat([a, pd.Series({'a':1 , 'b': 2}).to_frame().T])
a = pd.concat([a, pd.Series({'a':1 , 'b': 23}).to_frame().T])


print(a)
