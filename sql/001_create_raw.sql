-- sql/001_create_raw.sql
CREATE TABLE IF NOT EXISTS raw_nbp_tables (
    id             bigserial   PRIMARY KEY,
    table_type     char(1)     NOT NULL,             -- 'A' albo 'C'
    effective_date date        NOT NULL,             -- data notowania z odpowiedzi
    payload        jsonb       NOT NULL,             -- jedna tabela z odpowiedzi, bez zmian
    source_url     text        NOT NULL,             -- zapytanie, które ją zwróciło
    loaded_at      timestamptz NOT NULL DEFAULT now()
);