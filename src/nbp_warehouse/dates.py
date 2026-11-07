from datetime import date, timedelta

def date_chunks(start: date, end: date, max_days: int = 93) -> list[tuple[date, date]]:
    chunks=[]
    current=start
    chunk_end=start+timedelta(max_days-1)
    while current<=end:
        chunk_end = min(current + timedelta(days=max_days - 1), end)
        chunks.append((current, chunk_end))
        current = chunk_end + timedelta(days=1)
    return chunks
    return chunks
    return chunks


if __name__ == "__main__":
    print(date_chunks(date(2024, 1, 1), date(2024, 12, 31)))
    print(date_chunks(date(2024, 1, 2), date(2024, 1, 2)))
    print(date_chunks(date(2024, 1, 1), date(2024, 1, 31)))