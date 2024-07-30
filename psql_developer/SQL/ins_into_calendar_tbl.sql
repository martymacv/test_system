-- создаем производственный календарь
-- Table: ei.calendar

-- DROP TABLE IF EXISTS ei.calendar;

CREATE TABLE IF NOT EXISTS ei.calendar
(
    salary_date date NOT NULL,
    is_workday boolean DEFAULT true,
    is_weekend boolean DEFAULT false,
    is_holiday boolean DEFAULT false,
    CONSTRAINT pk_salary_date PRIMARY KEY (salary_date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS ei.calendar
    OWNER to postgres;

-- date generation

WITH RECURSIVE dates AS (
 SELECT to_date('2024-01-01', 'yyyy-mm-dd') AS date1
 UNION ALL
 SELECT date1 + 1
 FROM dates
 WHERE date1 < to_date('2026-01-01', 'yyyy-mm-dd')
)
INSERT INTO ei.calendar (salary_date)
SELECT date1
  FROM dates;

-- update weekends
UPDATE ei.calendar
   SET is_weekend = true,
	   is_workday = false
WHERE salary_date IN (
 SELECT salary_date
   FROM ei.calendar
  WHERE date_part('dow', salary_date) IN (0, 6) -- Исключаем воскресенье и субботу
);

-- update holidays
UPDATE ei.calendar
   SET is_holiday = true,
	   is_workday = false,
	   is_weekend = false
 WHERE salary_date in (to_date('04-11-2024', 'dd-mm-yyyy')
					  ,to_date('30-12-2024', 'dd-mm-yyyy')
					  ,to_date('31-12-2024', 'dd-mm-yyyy'));

-- update exceptions workday
UPDATE ei.calendar
   SET is_workday = TRUE,
	   is_weekend = false,
	   is_holiday = false
 WHERE salary_date in (to_date('02-11-2024', 'dd-mm-yyyy')
					  ,to_date('28-12-2024', 'dd-mm-yyyy'));

-- truncate table ei.calendar
