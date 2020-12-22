"""Test Module for preprocessing."""

from pathlib import Path

import pandas as pd
import pytest
from content_analysis.media_creation.preprocessing import Preprocessor

TEST_INPUT_PATH = Path("./tests/data/preprocessor_input.csv")
TEST_OUTPUT_PATH = Path("./tests/data/preprocessor_output.csv")


@pytest.fixture
def test_input():
    test_input = pd.read_csv(TEST_INPUT_PATH)

    return test_input


@pytest.fixture
def expected_output():
    expected_output = pd.read_csv(TEST_OUTPUT_PATH)

    return expected_output


def preprocessor_success_test(test_input):
    test_instance = Preprocessor(test_input)
    actual = test_instance.preprocess()

    assert isinstance(actual, pd.DataFrame)


def preprocess_output_as_expected_test(test_input, expected_output):
    actual = Preprocessor(test_input).preprocess()

    pd.testing.assert_frame_equal(actual, expected_output)
