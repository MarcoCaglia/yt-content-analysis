"""Test Module for MediaCreator."""

from pathlib import Path

import pandas as pd
import pytest
from bokeh.plotting.figure import Figure as BokePlot
from content_analysis.media_creation.media_creator import MediaCreator
from content_analysis.media_creation.preprocessing import Preprocessor

TEST_DATA_PATH = Path("./tests/data/preprocessor_input.csv")


@pytest.fixture
def test_data():
    test_data = pd.read_csv(TEST_DATA_PATH)

    test_data = Preprocessor(test_data).preprocess()

    return test_data


@pytest.fixture
def test_instance(test_data):
    test_instance = MediaCreator(test_data)

    return test_instance


def generate_overviews_success_test(test_instance):
    actual = test_instance.generate_overviews()

    assert isinstance(actual, list)
    assert len(actual) == 4
    is_plot = map(lambda element: isinstance(element, BokePlot), actual)
    assert all(is_plot)


def generate_ot_plots_success_test(test_instance):
    actual = test_instance.generate_ot_plots()

    assert isinstance(actual, list)
    assert len(actual) == 4
    is_plot = map(lambda element: isinstance(element, BokePlot), actual)
    assert all(is_plot)
