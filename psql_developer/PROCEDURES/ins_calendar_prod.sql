CREATE OR REPLACE PROCEDURE :OWNER:.ins_calendar_prod(
	IN p_year text,
	IN p_holiday_list character varying,
	IN p_workday_weekend_list character varying)
LANGUAGE 'plpgsql'
AS $BODY$
-- date generation
BEGIN
--RAISE NOTICE 'p_holiday_list is: %', p_holiday_list;

WITH RECURSIVE dates AS (
 SELECT to_date(''||p_year||'-01-01', 'yyyy-mm-dd') AS date1
 UNION ALL
 SELECT date1 + 1
 FROM dates
 WHERE date1 < to_date(''||p_year||'-12-31', 'yyyy-mm-dd')
)
INSERT INTO :OWNER:.calendar (calendar_date
	                       ,  is_workday)
	                  SELECT date1
	                       , true::boolean
                        FROM dates;
-- update weekends
UPDATE :OWNER:.calendar
   SET is_weekend = true,
	   is_workday = null
WHERE calendar_date IN (
 SELECT calendar_date
   FROM :OWNER:.calendar
  WHERE date_part('dow', calendar_date) IN (0, 6) -- Исключаем воскресенье и субботу
);
-- update holidays
EXECUTE '
  UPDATE :OWNER:.calendar
     SET is_holiday = true,
	     is_workday = null,
	     is_weekend = null
   WHERE to_char(calendar_date, ''dd-mm-yyyy'') in ('||p_holiday_list||')';
-- update exceptions workday
EXECUTE '
UPDATE :OWNER:.calendar
   SET is_workday = true,
	   is_weekend = null,
	   is_holiday = null
 WHERE to_char(calendar_date, ''dd-mm-yyyy'') in ('||p_workday_weekend_list||')';
END;
$BODY$;