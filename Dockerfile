### Build and install packages
FROM python:3.8 as build-python
LABEL maintainer="Shpilievoi Oleksandr <shpilevoy29@gmail.com>"

# Cleanup apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/
WORKDIR /app/
RUN pip install -r requirements.txt
### Final image
FROM python:3.8-slim

# Remove apt chache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/

# Copy scripts for starting project
COPY . /app/
WORKDIR /app/

EXPOSE 8000
ENV PYTHONPATH=.


# Run the app via the start.sh script
CMD ["bash", "/app/bash_scripts/start.sh"]
