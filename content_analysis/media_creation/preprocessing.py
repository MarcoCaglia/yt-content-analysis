"""Preprocessing Module for media creation."""

import re

import pandas as pd


class Preprocessor:
    """Prperocessing Module."""

    def __init__(self, data: pd.DataFrame) -> None:
        """Initialize Preprocessor.

        Args:
            data (pd.DataFrame): Scraped Data.
        """
        self.data = data

        self.anti_numerical_pattern = re.compile(r"[^\d]")

    def preprocess(self) -> pd.DataFrame:
        """Execute preprocessing."""
        processed_data = self.data.copy()
        processed_data = self._parse_upload_date(processed_data)
        processed_data = self._parse_views(processed_data)
        processed_data = self._parse_likes_dislikes(processed_data)
        processed_data = self._parse_comments(processed_data)

        return processed_data

    def _parse_upload_date(self, data):
        data.upload_date = pd.to_datetime(
            data.upload_date.map(lambda date: date[-12:])
            )

        return data

    def _parse_views(self, data):
        data.views = pd.to_numeric(data.views.map(self._get_numerical_value))

        return data

    def _parse_likes_dislikes(self, data):
        data.likes = pd.to_numeric(data.likes.map(self._get_numerical_value))
        data.dislikes = pd.to_numeric(
            data.dislikes.map(self._get_numerical_value)
            )

        data["like_ratio"] = data.likes / (data.likes + data.dislikes)
        data["likes_per_view"] = data.likes / data.views
        data["dislikes_per_view"] = data.dislikes / data.views

        return data

    def _parse_comments(self, data):
        data.comments = pd.to_numeric(
            data.comments.map(self._get_numerical_value)
            )
        data["comments_per_view"] = data.comments / data.views

        return data

    def _get_numerical_value(self, value):
        if isinstance(value, (int, float)):
            numerical = value
        else:
            numerical = re.sub(self.anti_numerical_pattern, "", str(value))

        return numerical
