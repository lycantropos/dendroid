from .literals import base, factories

empty_value_sequence_with_order_strategy = (
    base.empty_value_sequence_with_order_strategy
)
non_empty_value_sequence_with_order_strategy = (
    base.non_empty_value_sequence_with_order_strategy
)
single_value_with_order_strategy = base.single_value_with_order_strategy
two_or_more_values_with_order_strategy = (
    base.two_or_more_values_with_order_strategy
)
value_sequence_with_none_order_strategy = (
    base.value_sequence_with_none_order_strategy
)
value_sequence_with_order_strategy = base.value_sequence_with_order_strategy
value_with_order_strategy = base.value_with_order_strategy
value_with_order_strategy_strategy = base.value_with_order_strategy_strategy

to_non_empty_set_with_their_value_strategy = (
    factories.to_non_empty_set_with_their_value_strategy
)
to_value_sequences_with_order_strategy = (
    factories.to_value_sequences_with_order_strategy
)
