"""Test Module for MediaCreator."""

from pathlib import Path

import pandas as pd
import pytest
from bokeh.plotting.figure import Figure as BokePlot
from content_analysis.media_creation.media_creator import MediaCreator
from content_analysis.media_creation.preprocessing import Preprocessor
from .preprocessing_test import TEST_INPUT, INPUT_COLUMNS


@pytest.fixture
def test_data():
    test_data = pd.DataFrame(TEST_INPUT, columns=INPUT_COLUMNS)

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
