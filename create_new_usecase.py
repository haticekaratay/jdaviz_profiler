#!/usr/bin/env python3

"""
Create a new directory with an example template notebook and a
parameters file that can be filled-in to run a new profiling
"use case" (a new combination of example notebook and parameters).
"""

import argparse
from pathlib import Path

from src.generate_notebooks import (
    NOTEBOOK_TEMPLATE_FILENAME,
    OUTPUT_DIR_PATH,
    PARAMS_FILENAME,
)
from src.utils import set_logger

EXAMPLE_NOTEBOOK_CONTENT: str = """{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "7fb27b941602401d91542211134fc71a",
      "metadata": {"tags": ["skip_profiling"]},
      "outputs": [],
      "source": [
        "### imports\\n",
        "\\n",
        "from jdaviz import Imviz"
      ]
    }, {
      "cell_type": "code",
      "execution_count": null,
      "id": "acae54e37e7d407bbb7b55eff062a284",
      "metadata": {"tags": ["parameters", "skip_profiling"]},
      "outputs": [],
      "source": [
        "# paramA parameter\\n",
        "paramA = {paramA_value}  # noqa: F821\\n",
        "\\n",
        "# paramB parameter\\n",
        "paramB = \\"{paramB_value}\\"  # noqa: F821\\n",
        "\\n",
        "# paramC parameter\\n",
        "paramC = {paramC_value}  # noqa: F821"
      ]
    }, {
      "cell_type": "code",
      "execution_count": null,
      "id": "9a63283cbaf04dbcab1f6479b197f3a8",
      "metadata": {"tags": ["wait_for_viz"]},
      "outputs": [],
      "source": [
        "### Initialize and show Imviz\\n",
        "imviz = Imviz()\\n",
        "imviz.show(\\"sidecar:split-right\\")"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "python3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.12.9"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}"""

EXAMPLE_PARAMS_CONTENT: str = """{
  "paramA_value": [1, 2, 3],
  "paramB_value": ["x", "y", "z"],
  "paramC_value": [true, false]
}"""

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Script to add new use cases for notebook generation and profiling."
        )
    )
    parser.add_argument(
        "--dir_path",
        help="The directory where the new use case directory will be created.",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "--log_file",
        help="Path to the log file.",
        required=False,
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--log_level",
        help="Set the logging level (default: INFO).",
        required=False,
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    # Parse arguments
    _args: argparse.Namespace = parser.parse_args()

    # Set logger with given log_level and log_file
    set_logger(log_level=_args.log_level, log_file=_args.log_file)

    # Create new use case directory
    usecase_dir_path: Path = _args.dir_path
    if usecase_dir_path.exists():
        raise FileExistsError(
            f"The use case directory '{usecase_dir_path}' already exists."
        )
    usecase_dir_path.mkdir(parents=True)

    try:
        # Create empty template.ipynb and params.json files
        notebook_template_path: Path = usecase_dir_path / NOTEBOOK_TEMPLATE_FILENAME
        with notebook_template_path.open(mode="w", encoding="utf-8") as notebook_file:
            notebook_file.write(EXAMPLE_NOTEBOOK_CONTENT)

        # Create example params.json file
        params_path: Path = usecase_dir_path / PARAMS_FILENAME
        with params_path.open(mode="w", encoding="utf-8") as params_file:
            params_file.write(EXAMPLE_PARAMS_CONTENT)

        # Create notebooks output directory
        notebooks_dir_path: Path = usecase_dir_path / OUTPUT_DIR_PATH
        notebooks_dir_path.mkdir()
        (notebooks_dir_path / ".keep").touch()
    except Exception as e:
        # Clean up by removing the created use case directory
        for child in usecase_dir_path.rglob("*"):
            if child.is_file():
                child.unlink()
            else:
                child.rmdir()
        usecase_dir_path.rmdir()
        raise e
