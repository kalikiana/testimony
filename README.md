<!--
SPDX-FileCopyrightText: 2024 Liv Dywan <liv.dywan@suse.com>

SPDX-License-Identifier: EUPL-1.2
-->

## testimony

![GitHub Actions](https://github.com/kalikiana/testimony/actions/workflows/test.yaml/badge.svg)
![GitHub Actions](https://github.com/kalikiana/testimony/actions/workflows/container.yaml/badge.svg)

### What's this project about?

The log files of [openQA](https://open.qa) jobs are key to reviewing the result of a test. What if they could be processed and analyzed with the help of AI? More specifically using [TensorFlow](https://www.tensorflow.org/) to train a model on passing and failing jobs.

### How do I build and run this?

The quickest way to run testimony is via the container:

```bash
podman run -it --rm -v $(pwd):/w -w /w ghcr.io/kalikiana/testimony/min:latest
```

For a typical development setup the necessary dependencies can be installed via [poetry](https://python-poetry.org):

```bash
poetry install
poetry run pytest -v
```
