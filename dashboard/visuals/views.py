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

DATA_PATH = Path(__file__).parent.parent.joinpath(os.getenv("DATA_PATH")) \
    .joinpath(os.getenv("DATABASE_NAME"))

# Create your views here.


def _create_media(kind):
    # Check if the DB is at the expected position
    if not DATA_PATH.isfile():
        raise NoDataError(f"No DB at {DATA_PATH}")

    # Create DB for loading the data
    engine = create_engine(f"sqlite:///{DATA_PATH.as_posix}")

    # Load the data with pandas
    data = pd.read_sql("SELECT * FROM video_info", engine)

    # Preprocess the data
    preprocessed = Preprocessor(data).preprocess

    # Initialize Media Creator
    media_creator = MediaCreator(preprocessed)

    # Create and return the appropriate graphs
    if kind == "overview":
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

    return render(
        request,
        "visuals/graphs.html",
        {"graphs": graph_htmls, "title": {"Overview Graphs"}}
        )


def ot_graphs(request):
    # Navigate to folder where OT graphs are stored
    overviews_folder = DATA_PATH.joinpath("ot_graphs")

    # Generate graphs paths
    graphs_paths = overviews_folder.iterdir()

    # Load all graphs
    graph_htmls = []
    for path in graphs_paths:
        with path.open("r") as f:
            graph_htmls.append(f.read())

    return render(
        request,
        "visuals/graphs.html",
        {"graphs": graph_htmls, "title": "Overtime Graphs"}
        )
