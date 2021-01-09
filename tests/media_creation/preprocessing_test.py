"""Test Module for preprocessing."""

import pandas as pd
import pytest
from content_analysis.media_creation.preprocessing import Preprocessor

INPUT_COLUMNS = ['title', 'upload_date', 'views', 'author', 'likes', 'dislikes', 'comments', 'timestamp']
TEST_INPUT = [
    ['Slow ASMR to Make You All Sleepy 😴', 'Dec 18, 2020', '104,424 views', 'ASMR Glow', '5,695 likes', '111 dislikes', '669 Comments', '2020-12-19 11:13:22.345294'],
    ['[ASMR- NO TALKING] 👅 👄ALL THE MOUTH SOUNDS! w/ Tascam Tapping ~ 👄👅 (this will knock you tf out)', 'Jun 8, 2020', '3,471,617 views', 'FrivolousFox ASMR', '59,115 likes', '3,400 dislikes', '7,156 Comments', '2020-12-19 10:52:49.038966'],
    ['ASMR Come Antique Shopping With Me', 'May 13, 2019', '269,848 views', 'Goodnight Moon', '9,785 likes', '98 dislikes', '497 Comments', '2020-12-19 11:20:45.193789'],
    ['ASMR | Poker Set // Cards, Chips, Dice, Wooden Box ~', 'Sep 22, 2020', '645,829 views', 'Gibi ASMR', '18,440 likes', '476 dislikes', '1,918 Comments', '2020-12-19 11:09:09.903929'],
    ['Gibi ASMR | Pure Finger Flutters Trigger [Compilation]', 'Oct 27, 2020', '364,127 views', 'Gibi ASMR', '14,679 likes', '229 dislikes', '1,711 Comments', '2020-12-19 11:11:05.214979']
]

OUTPUT_COLUMNS = ['title', 'upload_date', 'views', 'author', 'likes', 'dislikes', 'comments', 'timestamp', 'like_ratio', 'likes_per_view', 'dislikes_per_view', 'comments_per_view']
EXPECTED_OUTPUT = [
    ['Slow ASMR to Make You All Sleepy 😴', '2020-12-18', 104424, 'ASMR Glow', 5695, 111, 669, '2020-12-19 11:13:22.345294', 0.9808818463658284, 0.0545372711254117, 0.0010629740289588, 0.0064065732015628],
    ['[ASMR- NO TALKING] 👅 👄ALL THE MOUTH SOUNDS! w/ Tascam Tapping ~ 👄👅 (this will knock you tf out)', '2020-06-08', 3471617, 'FrivolousFox ASMR', 59115, 3400, 7156, '2020-12-19 10:52:49.038966', 0.945613052867312, 0.0170280880638618, 0.0009793707082319, 0.0020612872906199],
    ['ASMR Come Antique Shopping With Me', '2019-05-13', 269848, 'Goodnight Moon', 9785, 98, 497, '2020-12-19 11:20:45.193789', 0.9900839825963776, 0.0362611544276778, 0.0003631674127657, 0.0018417775933117],
    ['ASMR | Poker Set // Cards, Chips, Dice, Wooden Box ~', '2020-09-22', 645829, 'Gibi ASMR', 18440, 476, 1918, '2020-12-19 11:09:09.903929', 0.9748361175724256, 0.0285524496422427, 0.0007370372033463, 0.0029698263781898],
    ['Gibi ASMR | Pure Finger Flutters Trigger [Compilation]', '2020-10-27', 364127, 'Gibi ASMR', 14679, 229, 1711, '2020-12-19 11:11:05.214979', 0.984639119935605, 0.0403128578765101, 0.0006289014547122, 0.0046989099956883]
]


@pytest.fixture
def test_input():
    test_input = pd.DataFrame(TEST_INPUT, columns=INPUT_COLUMNS)

    return test_input


@pytest.fixture
def expected_output():
    expected_output = pd.DataFrame(EXPECTED_OUTPUT, columns=OUTPUT_COLUMNS)
    expected_output.upload_date = pd.to_datetime(expected_output.upload_date)

    return expected_output


def preprocessor_success_test(test_input):
    test_instance = Preprocessor(test_input)
    actual = test_instance.preprocess()

    assert isinstance(actual, pd.DataFrame)


def preprocess_output_as_expected_test(test_input, expected_output):
    actual = Preprocessor(test_input).preprocess()

    pd.testing.assert_frame_equal(actual, expected_output)
