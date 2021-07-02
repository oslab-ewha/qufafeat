import featuretools as tf
import pandas as pd

from featuretools.entityset import Entity, EntitySet

from pandas import DataFrame
from featuretools.primitives import Correlation

reference_data = pd.to_datetime("01-01-2019")
input_ages = [pd.to_datetime("01-01-1989"), pd.to_datetime("01-01-2002")]

corr = Correlation(method='kendall')
array_1 = [1, 4, 6, 7]
array_2 = [1, 5, 9, 7]
print(corr(array_1, array_2))
exit(1)