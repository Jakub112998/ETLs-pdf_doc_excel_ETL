from unittest.mock import MagicMock
from my_abc import AbstractAdder, ConcreteAdder, AddExecuter

import pipeline
import pytest


# python -m venv .venv
# source .venv/bin/activate
# python -m pip install pytest
#

def test_collect_files(tmp_dir, monkeypatch):
    # temp_dir - to get temp directory
    # monkeypatch - to replace real directory with temp_dir
    # given
    temp_data_dir = tmp_dir / "data"
    temp_data_dir.mkdir(parents=True)  # makes sure that all parent directories inside are created also
    temp_file = temp_data_dir / "file1.txt"  # create single tekst file inside
    temp_file.touch()

    monkeypatch.setattr(pipeline, "DATA_DIR",
                        temp_data_dir)  # new value for "DATA_DIR" inside pipeline module is temp_data_dir

    expected_length = 1  # because only 1 file is in temp_directory
    # when
    list_of_files = pipeline.collect_files("*.txt")
    actual_length = len(list_of_files)
    # and then
    assert expected_length == actual_length

def test_AddExecuterCallAddAndReturnsResult():
    mock_adder = MagicMock(AbstractAdder)
    mock_adder.add = MagicMock(return_value=3)
    result = AddExecuter(mock_adder)
    mock_adder.add.assert_called_once_with(1, 2)
    assert result == 3

