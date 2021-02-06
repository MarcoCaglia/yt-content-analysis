import os
from pathlib import Path

from content_analysis.media_creation.media_creator import MediaCreator
from content_analysis.media_creation.preprocessing import Preprocessor
from content_analysis.media_creation.exceptions import NoDataError
from django.shortcuts import render
from dotenv import load_dotenv
import pandas as pd
from bokeh.embed import components
from sqlalchemy import create_engine

load_dotenv()

DATA_PATH = Path(__file__).parent.parent.parent \
    .joinpath(os.getenv("DATA_PATH")).joinpath(os.getenv("DATABASE_NAME"))

# Create your views here.


def _create_media(kind):
    # Check if the DB is at the expected position
    if not DATA_PATH.is_file():
        raise NoDataError(f"No DB at {DATA_PATH}")

    # Create DB connection for loading the data
    engine = create_engine(f"sqlite:///{DATA_PATH.as_posix()}")

    # Load the data with pandas and filter by currently active project tag
    # (Project Tag as specified in .env file)
    project_tag = os.getenv("PROJECT_TAG")
    data = pd.read_sql(
        f"SELECT * FROM video_info WHERE project_tag = '{project_tag}'",
        engine
        )

    # Preprocess the data
    preprocessed = Preprocessor(data).preprocess()

    # Initialize Media Creator
    media_creator = MediaCreator(preprocessed)

    # Create and return the appropriate graphs
    if kind == "overviews":
        graphs = media_creator.generate_overviews()
    elif kind == "ot_graphs":
        graphs = media_creator.generate_ot_plots()
    else:
        raise AssertionError

    # Return components as list of tuples
    graph_components = [components(graph) for graph in graphs]

    return graph_components



def home(request):
    # Just return base html page
    return render(request, "visuals/base.html")


def overviews(request):
    # Create Media
    media = _create_media("overviews")
    scripts, divs = zip(*media)

    div_groups = _media_to_grid(divs)

    return render(
        request,
        "visuals/graphs.html",
        {
            "scripts": scripts,
            "div_groups": div_groups,
            "title": "Overview Graphs"
            }
        )


def ot_graphs(request):
    # Create Media
    media = _create_media("ot_graphs")
    scripts, divs = zip(*media)

    div_groups = _media_to_grid(divs)

    return render(
        request,
        "visuals/graphs.html",
        {
            "scripts": scripts,
            "div_groups": div_groups,
            "title": "Overtime Graphs"
            }
        )


def _media_to_grid(media_list):
    # Set number of columns
    cols = 2

    row_cols = [
        media_list[col * cols: (col + 1) * cols] for
        col in
        range(len(media_list) // cols + 1)
        ]

    return row_cols
