# SPDX-FileCopyrightText: 2024 Liv Dywan <liv.dywan@suse.com>
#
# SPDX-License-Identifier: EUPL-1.2

FROM python:3.11-alpine
COPY testimony ./testimony
COPY pyproject.toml poetry.lock README.md .
RUN apk add --no-cache poetry && \
    poetry install --no-cache --without dev
ENTRYPOINT ["poetry", "run", "testimony"]
