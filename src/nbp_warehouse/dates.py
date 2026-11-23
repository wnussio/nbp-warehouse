from datetime import date, timedelta
from collections.abc import Iterator

def date_chunks(start: date, end: date, max_days: int = 93) -> Iterator[tuple[date, date]]:
    current=start
    while current<=end:
        chunk_end = min(current + timedelta(days=max_days - 1), end)
        yield (current,chunk_end)
        current = chunk_end + timedelta(days=1)
    
