## Dashboard Docker File
# Get Base Image
FROM python:3.8

# Set Workdir
WORKDIR /home/usr

# Get code and working files
COPY ./content_analysis ./content_analysis
COPY ./dashboard ./dashboard
COPY ./data/data.db ./data/data.db
COPY pyproject.toml .
COPY poetry.lock .
COPY .env .

# Install poetry and create environment
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install poetry
RUN poetry env use 3.8.5
RUN poetry install --no-dev

# Expose port for dashboard
EXPOSE 8000

# Run dashboard
CMD ["poetry", "run", "python3", "dashboard/manage.py", "runserver", "0.0.0.0:8000"]