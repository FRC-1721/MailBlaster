# Set base docker
FROM python:3
# Authors
LABEL authors="31870999+KenwoodFox@users.noreply.github.com"

# Set the name of our app
ARG APP_NAME=email-blaster
ENV APP_NAME=${APP_NAME}

# Get the current git version
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

# UID, GID
ARG USER_ID="10001"
ARG GROUP_ID="app"

# App home
ARG HOME="/app"
ENV HOME=${HOME}

# Perms for home
RUN groupadd --gid ${USER_ID} ${GROUP_ID} && \
    useradd --create-home --uid ${USER_ID} --gid ${GROUP_ID} --home-dir /app ${GROUP_ID}

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        file        \
        gcc         \
        libwww-perl && \
    apt-get autoremove -y && \
    apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

# Set workdir
WORKDIR ${HOME}

# Copy in all requirements
ADD requirements requirements/
# Install normal reqs
RUN pip install -r requirements/requirements.txt
# Install testing reqs
RUN pip install -r requirements/test_requirements.txt

# Copy in everything else
ADD . ${HOME}
# Add /bin to path
ENV PATH $PATH:${HOME}/bin

# Install our app in edit mode using pip
RUN pip install -e ${HOME}

# Drop root and change ownership of /app to app:app
RUN chown -R ${USER_ID}:${GROUP_ID} ${HOME}
USER ${USER_ID}

# Run the entrypoint bin
ENTRYPOINT ["entrypoint"]
