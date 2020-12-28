"""Module for creating visualizations from preprocessed data."""

from typing import Dict, List, Tuple

import pandas as pd
from bokeh.models import HoverTool
from bokeh.palettes import Spectral4
from bokeh.plotting import ColumnDataSource, figure
from bokeh.plotting.figure import Figure as BokePlot


class MediaCreator:
    """Class for creating visualizations from preprocessed data."""

    def __init__(self, data: pd.DataFrame) -> None:
        """Initialize MediaCreator class.

        Args:
            data (pd.DataFrame): Data scraped from sourcing.
        """
        self.data = data.copy()

    def generate_overviews(
        self,
        grouper: str = "author",
        features: List[str] = [
            "like_ratio",
            "comments_per_view",
            "likes_per_view",
            "views",
        ],
        aggregator: str = "mean",
    ) -> List[BokePlot]:
        """Generate Overview Graphs.

        Overview Graphs are bar plots, displaying success metrics per creator
        over the entire observation period.

        Args:
            grouper (str, optional): Column by which to group the data.
                Defaults to 'author'.
            features (List[str], optional): List of features to be depicted.
                Defaults to standard features.
            aggregator (str, optional): Aggregation operation to perform on
                grouping. Standard is 'mean'.

        Returns:
            List[boke.Figure]: List of bokeh plots.
        """
        plots = []
        for feature in features:
            grouped_data = (
                self.data.groupby(grouper)[[feature]]
                .agg(aggregator)
                .reset_index()
                .sort_values(by=feature, ascending=False)
            )
            source = ColumnDataSource(data=grouped_data)

            plot = self._create_overview_plot(
                grouper=grouper,
                feature=feature,
                source=source,
                aggregator=aggregator,
                x_range=grouped_data[grouper].tolist(),
            )
            plots.append(plot)

        return plots

    def _create_overview_plot(
        self,
        grouper: str,
        feature: str,
        source: ColumnDataSource,
        aggregator: str,
        x_range: List[str],
    ) -> BokePlot:
        tooltip = [
            (self._prettify_string(grouper), "@" + grouper),
            (self._prettify_string(grouper), "@" + feature),
        ]
        plot = figure(
            tools="pan,box_zoom,reset,save",
            y_axis_label=self._prettify_string(feature),
            x_axis_label=self._prettify_string(grouper),
            x_range=x_range,
            tooltips=tooltip,
        )

        plot.vbar(x=grouper, top=feature, source=source, width=0.9)
        plot.title.text = (
            f"{self._prettify_string(aggregator)} of "
            f"{self._prettify_string(feature)} per "
            f"{self._prettify_string(grouper)}"
        )
        plot.title.align = "center"
        plot.title.text_font_size = "20px"

        return plot

    def generate_ot_plots(
        self,
        features: List[str] = [
            "like_ratio",
            "comments_per_view",
            "likes_per_view",
            "views",
        ],
        date_column: str = "upload_date",
    ) -> List[BokePlot]:
        """Create List of over-time comparison plots for selected features.

        Args:
            features (List[str], optional): Features to be compared over-time.
                Defaults to ["like_ratio", "comments_per_view",
                "likes_per_view", "views"].
            date_column (str, optional): Name of the date_column to use.
                Defaults to "upload_date".

        Returns:
            List[BokePlot]: List of Bokeh Plots.
        """
        ot_data = self.data.sort_values(by=date_column).set_index("author").copy()

        tooltips = [
            ("Author", "@author"),
            ("Upload Date", "@upload_date{%F}"),
            ("Title", "@title"),
        ]

        formatters = {"@author": "printf", "@upload_date": "datetime"}

        plots = []

        for feature in features:
            plot = self._create_ot_plot(
                ot_data=ot_data,
                feature=feature,
                date_column=date_column,
                tooltips=tooltips,
                formatters=formatters,
            )

            plot = self._set_plot_settings(plot, feature)

            plots.append(plot)

        return plots

    def _set_plot_settings(self, plot, feature):
        plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"
        plot.title.text = (
            f"{self._prettify_string(feature)} per Author " "Over Time"
        )

        plot.title.align = "center"
        plot.title.text_font_size = "20px"

        return plot

    def _create_ot_plot(
        self,
        ot_data: pd.DataFrame,
        feature: str,
        date_column: str,
        tooltips: List[Tuple[str, str]],
        formatters: Dict,
    ) -> BokePlot:
        plot = figure(
            tools="pan,box_zoom,reset,save",
            y_axis_label=self._prettify_string(feature),
            x_axis_label=self._prettify_string(date_column),
            x_axis_type="datetime",
        )
        hovertool = HoverTool(
            tooltips=tooltips + [(self._prettify_string(feature), "@" + feature)],
            formatters=formatters,
        )
        plot.add_tools(hovertool)

        plot = self._add_lines(plot, ot_data, date_column, feature)

        return plot

    @staticmethod
    def _add_lines(
        plot: BokePlot, ot_data: pd.DataFrame, date_column: str, feature: str
    ) -> BokePlot:
        for author, colour in zip(ot_data.index.unique(), Spectral4):
            tmp = ot_data.loc[[author], [date_column, feature, "title"]].copy()
            source = ColumnDataSource(tmp)
            plot.circle(
                date_column,
                feature,
                source=source,
                legend_label=author,
                fill_color=colour,
            )
            plot.line(
                date_column,
                feature,
                source=source,
                legend_label=author,
                line_color=colour,
            )
        return plot

    @staticmethod
    def _prettify_string(string):
        prettified = string.replace("_", " ").title()

        return prettified
