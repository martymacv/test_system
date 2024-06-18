-- SEQUENCE: aqa.check_sql_next_aqa_id

DROP SEQUENCE IF EXISTS aqa.check_sql_next_aqa_id;

CREATE SEQUENCE IF NOT EXISTS aqa.check_sql_next_aqa_id
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE aqa.check_sql_next_aqa_id
    OWNED BY aqa.check_sql.aqa_id;

ALTER SEQUENCE aqa.check_sql_next_aqa_id
    OWNER TO postgres;

GRANT ALL ON SEQUENCE aqa.check_sql_next_aqa_id TO postgres;