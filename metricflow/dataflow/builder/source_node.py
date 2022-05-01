from typing import Sequence

from metricflow.dataflow.dataflow_plan import ReadSqlSourceNode, PlotTimeDimensionTransformNode, BaseOutput
from metricflow.dataset.data_source_adapter import DataSourceDataSet
from metricflow.model.semantic_model import SemanticModel


class SourceNodeBuilder:
    """Helps build source nodes to use in the dataflow plan builder."""

    def __init__(self, semantic_model: SemanticModel) -> None:  # noqa: D
        self._semantic_model = semantic_model

    def create_from_data_sets(self, data_sets: Sequence[DataSourceDataSet]) -> Sequence[BaseOutput[DataSourceDataSet]]:
        """Creates source nodes from DataSourceDataSets."""
        source_nodes = []
        for data_set in data_sets:
            read_node = ReadSqlSourceNode[DataSourceDataSet](data_set)
            aggregation_time_dimensions = self._semantic_model.data_source_semantics.get_aggregation_time_dimensions(
                data_set.data_source_reference
            )
            # Dimension sources may not have any measures -> no aggregation time dimensions.
            if len(aggregation_time_dimensions) == 0:
                source_nodes.append(read_node)
            else:
                for time_dimension_reference in aggregation_time_dimensions:
                    source_nodes.append(
                        PlotTimeDimensionTransformNode[DataSourceDataSet](
                            parent_node=read_node,
                            aggregation_time_dimension_reference=time_dimension_reference,
                        )
                    )

        return source_nodes
