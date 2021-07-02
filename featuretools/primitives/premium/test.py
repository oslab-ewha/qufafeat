import featuretools as tf
import pandas as pd

from featuretools.entityset import Entity, EntitySet

from pandas import DataFrame
from featuretools.primitives import Correlation
from featuretools.primitives import Variance
from featuretools.primitives import UpperCaseCount

corr = Correlation(method='kendall')
array_1 = [1, 4, 6, 7]
array_2 = [1, 5, 9, 7]
print(corr(array_1, array_2))

variance = Variance()
print(variance([0, 3, 4, 3]))

x = ['This IS a string.', 'This is a string', 'aaa']
upper_count = UpperCaseCount()
print(upper_count(x).tolist())

exit(1)
