"""
Test authentication with various file formats.

Date: 2021-05-30
Author: Vitali Lupusor
"""

# Import local modules
from binance import Binance  # type: ignore


def test_authentication_from_env_file():
    """
    Test authentication with bad path to `.env` file.

    Expect `FileNotFoundError`.
    """
    # Import third-party modules
    from pytest import raises

    with raises(FileNotFoundError) as invalidPath:
        Binance.from_env_file('noSuchPath/.env')

        err = (
            "No such file or directory: 'noSuchPath/.env'"
        )
        err in str(invalidPath.value)


def test_authentication_from_json_file():
    """
    Test authentication with bad path to `json` format file.

    Expect `FileNotFoundError`.
    """
    # Import third-party modules
    from pytest import raises

    with raises(FileNotFoundError) as invalidPath:
        Binance.from_json_file('noSuchPath/credentials.json')

        err = (
            "No such file or directory: 'noSuchPath/credentials.json'"
        )
        err in str(invalidPath.value)
