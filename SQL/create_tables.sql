-- Table: aqa.check_sql

-- DROP TABLE IF EXISTS aqa.check_sql;

CREATE TABLE IF NOT EXISTS aqa.check_sql
(
    aqa_id numeric NOT NULL DEFAULT nextval('aqa.check_sql_next_aqa_id'::regclass),
    tst_object character varying COLLATE pg_catalog."default",
    aqa_desc character varying COLLATE pg_catalog."default",
    sql_text character varying COLLATE pg_catalog."default",
    update_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT aqa_check_sql_pkey PRIMARY KEY (aqa_id),
    CONSTRAINT aqa_check_sql_aqa_id_aqa_id1_key UNIQUE (aqa_id)
        INCLUDE(aqa_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS aqa.check_sql
    OWNER to postgres;

-- Table: aqa.check_val

-- DROP TABLE IF EXISTS aqa.check_val;

CREATE TABLE IF NOT EXISTS aqa.check_val
(
    aqa_id numeric NOT NULL,
    val numeric,
    test_date date,
    update_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT aqa_check_val_aqa_id_fkey FOREIGN KEY (aqa_id)
        REFERENCES aqa.check_sql (aqa_id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS aqa.check_val
    OWNER to postgres;

-- Table: tst1.test_tbl

-- DROP TABLE IF EXISTS tst1.test_tbl;

CREATE TABLE IF NOT EXISTS tst1.test_tbl
(
    update_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    today_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    test_field character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS tst1.test_tbl
    OWNER to postgres;

-- Table: tst2.test_tbl

-- DROP TABLE IF EXISTS tst2.test_tbl;

CREATE TABLE IF NOT EXISTS tst2.test_tbl
(
    update_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    today_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    test_field character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS tst2.test_tbl
    OWNER to postgres;