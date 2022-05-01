from metricflow.dataset.dataset import DataSet
from metricflow.time.time_granularity import TimeGranularity

PTD = DataSet.plot_time_dimension_name()
PTD_SPEC_DAY = DataSet.plot_time_dimension_spec(TimeGranularity.DAY)
PTD_SPEC_MONTH = DataSet.plot_time_dimension_spec(TimeGranularity.DAY)
