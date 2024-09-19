import numpy as np
from numpy.testing import assert_array_equal
from polyfactory.factories.pydantic_factory import ModelFactory
import pytest

from sodym import NamedDimArray, Dimension, DimensionSet
from sodym.named_dim_array_helper import ndarray_stack, ndarray_split


dimension_set = DimensionSet(
    dimensions = [
        {'name': 'time', 'letter': 't', 'items': [1990, 2000, 2010]},
        {'name': 'place', 'letter': 'p', 'items': ['World', ]}
    ]
)

class NamedDimArrayFactory(ModelFactory[NamedDimArray]):
    dims = dimension_set
    values = np.random.rand(3, 1)


@pytest.mark.parametrize("new_dim_length", [2, 7])
def test_ndarray_stack(new_dim_length):
    named_dim_arrays = [NamedDimArrayFactory.build() for _ in range(new_dim_length)]
    additional_dim = Dimension(name='extra', letter='x', items=list(range(new_dim_length)))
    stacked = ndarray_stack(named_dim_arrays, additional_dim)

    assert stacked.shape[:-1] == dimension_set.shape()
    assert stacked.dims.dimensions[:-1] == dimension_set.dimensions

    for i in range(new_dim_length):
        assert_array_equal(stacked.values[:, :, i], named_dim_arrays[i].values)
    assert stacked.shape[-1] == new_dim_length
    assert stacked.dims.dimensions[-1] == additional_dim


def test_ndarray_split():
    named_dim_arrays = [NamedDimArrayFactory.build() for _ in range(3)]
    items = ['pre-industrial', 1950, 2000]
    additional_dim = Dimension(name='extra', letter='x', items=items)
    stacked = ndarray_stack(named_dim_arrays, additional_dim)
    split = ndarray_split(stacked, dim_letter='x')
    assert len(split) == 3
    assert list(split.keys()) == items
    for i, item in enumerate(items):
        assert_array_equal(split[item].values, named_dim_arrays[i].values) 