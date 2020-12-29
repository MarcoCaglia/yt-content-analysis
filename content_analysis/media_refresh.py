"""Module housing a refresh script for the graphs."""

from pathlib import Path
from typing import List

import pandas as pd
from bokeh.plotting import save
from bokeh.plotting.figure import Figure as BokehPlot
from sqlalchemy import create_engine
from bokeh.resources import CDN

from media_creation.exceptions import NoDataError
from media_creation.media_creator import MediaCreator
from media_creation.preprocessing import Preprocessor

DATA_PATH = Path(".").absolute().joinpath("data/data.db")
OVERVIEW_PATH = DATA_PATH.parent.joinpath("overviews")
OT_PATH = DATA_PATH.parent.joinpath("ot_graphs")


def refresh_media() -> None:
    """Refresh all graphs.

    Raises:
        NoDataError: Database was not found. Run Scraper and/or check that
            DATA_PATH is defined correctly.
    """
    # Check if the DB exists at DATA_PATH; raise error if it doesn't
    if not DATA_PATH.is_file():
        raise NoDataError(f"No File at {DATA_PATH.as_posix()}")

    # Since DB exists at DATA_PATH, create engine with DATA_PATH
    engine = create_engine("sqlite:///" + DATA_PATH.as_posix())

    # Load the data
    data = pd.read_sql("SELECT * FROM video_info", engine)

    # Apply preprocessing
    processed_data = Preprocessor(data).preprocess()

    # Get the graphs
    media_creator = MediaCreator(processed_data)
    overview_graphs = media_creator.generate_overviews()
    ot_graphs = media_creator.generate_ot_plots()

    # Save Graphs
    _save_graphs(overviews=overview_graphs, ot_graphs=ot_graphs)


def _save_graphs(
    overviews: List[BokehPlot],
    ot_graphs: List[BokehPlot]
) -> None:
    # Create list of (directory, objects) tuples.
    to_be_saved = zip([OVERVIEW_PATH, OT_PATH], [overviews, ot_graphs])

    # Check if target directories exist and create if needed.
    for directory, objects in to_be_saved:
        if not directory.is_dir():
            directory.mkdir()
        for graph in objects:
            save(
                graph,
                directory.joinpath(_generate_filename(graph.title.text)),
                resources=CDN,
                title=graph.title.text
                )


def _generate_filename(string: str) -> str:
    title = string.replace(" ", "_").lower() + ".html"
    return title


if __name__ == "__main__":
    refresh_media()
