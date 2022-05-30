import numpy as np
import pandas as pd

from featuretools.primitives.base.aggregation_primitive_base import(
     AggregationPrimitive
)

from featuretools.utils.gen_utils import Library
from featuretools.variable_types import(
     Boolean,
     Discrete,
     Index,
     Numeric,
     Variable
)


class IsUnique(AggregationPrimitive):
    """ Detect Values outside the allowed error range
        in the column of unique values.

        Description:
            Given a list of values, detect values in a range that are not allowed in a unique column.

        Args:
            skipna (bool): Determines whether to ignore thre rows have 'NaN' values.
                           Default to True. => the rows that have "NaN" are not removed.

        Examples:
            >>> is_unique_col = IsUnique()
            >>> tolerance_percent = 100
            >>> IsUnique([3, 1, 2, 3, 4], tolerance_percent)
                [True, False, True, True, True]

            We can remove the rows having 'NaN' values.

            >>> is_unique_col = IsUnique()
            >>> tolerance_percent = 100
            >>> IsUnique([3, 1, 2, 3, 4, None], tolerance_percent)
                [True, False, True, True, True, False]

            >>> is_unique_col = IsUnique(skipna=False)
            >>> tolerance_percent = 100
            >>> IsUnique([3, 1, 2, 3, 4, None], tolerance_percent)
               [ True, False, True, True, True]
    """

    name = "is_unique"
    input_types = [Discrete]
    return_type = [Discrete]
    description_template = "detect the values not allowed in unique columns"

    def __init__(self, skipna=True):
        self.skipna = skipna


    def get_function(self):
        def is_uniq(input_data, tolerance_percent):
            df1 = pd.DataFrame(data=input_data)
            df1.rename(columns={0: "value"}, inplace=True)
            if self.skipna == False:
                df1.dropna(inplace=True)

            ## Extract the reference value
            df2 = input_data.value_counts()
            df2 = pd.DataFrame(data=df2)
            df2.reset_index(inplace=True)
            df2.rename(columns={"index": "value", 0: "count"}, inplace=True)
            reference_value = df2['value'].values[0]

            ## Calculate allowed range
            upper_tolerance = reference_value * (1 + tolerance_percent/100)
            lower_tolerance = reference_value * (1 - tolerance_percent/100)

            ## Detect values in unacceptable ranges
            result = []
            for index, row in df1.iterrows():
                if row['value'] >= lower_tolerance and row['value'] <= upper_tolerance:
                    result.append(True)
                else:
                    result.append(False)
            return result
        return is_uniq




