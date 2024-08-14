import datetime
from unittest import mock

import pytest

from app.main import outdated_products


class MockDate(datetime.date):
    @classmethod
    def today(cls) -> datetime:
        return cls(2000, 2, 2)


@pytest.fixture
def product_list() -> list:
    return [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 5),
            "price": 120
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
            "price": 160
        }
    ]


@pytest.fixture
def mocked_date() -> MockDate:
    with mock.patch("datetime.date", MockDate):
        yield


@pytest.mark.parametrize(
    "test_day, result_list",
    [
        (datetime.date(2022, 1, 30), []),
        (datetime.date(2022, 2, 11), ["salmon", "chicken", "duck"]),
        (datetime.date(2022, 2, 5), ["duck"])
    ]
)
def test_function_returns_outdated_products(
        mocked_date: MockDate,
        product_list: list,
        test_day: datetime,
        result_list: list
) -> None:
    MockDate.today = mock.Mock(return_value=test_day)
    print(MockDate.today)
    assert outdated_products(product_list) == result_list
