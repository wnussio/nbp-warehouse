from datetime import date
import pytest
from nbp_warehouse.dates import date_chunks


def test_single_day():
    result = date_chunks(date(2024, 1, 2), date(2024, 1, 2))
    assert result == [(date(2024, 1, 2),date(2024, 1, 2))]

def test_full_year():
    result = date_chunks(date(2024, 1, 1), date(2024, 12,31))
    assert result == [(date(2024, 1, 1),date(2024, 4, 2)),
      (date(2024, 4, 3),date(2024, 7, 4)),
       (date(2024, 7, 5),date(2024, 10, 5)),
       (date(2024, 10, 6),date(2024, 12, 31))]


@pytest.mark.parametrize(
    "start, end, expected_len",
    [
        (date(2024, 1, 1), date(2024, 4, 2), 1),   # dokładnie 93 dni
        (date(2024, 1, 1), date(2024, 4, 3), 2),   # 94 dni
        (date(2024, 1, 2), date(2024, 1, 1), 0),   # start po końcu
    ],
)
def test_number_of_windows(start, end, expected_len):
    assert len(date_chunks(start, end)) == expected_len