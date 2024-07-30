CREATE OR REPLACE PROCEDURE test.run_check_sql(
	IN p_check_id integer,
	IN p_check_date date default date_trunc('day', now()))
LANGUAGE 'plpgsql'
AS $BODY$
  declare
	v_sql_text text;

	v_year  varchar(4)  default  LPAD(CAST(date_part('YEAR', p_check_date) AS varchar(4)), 4, '0');
	v_month varchar(2)  default  LPAD(CAST(date_part('MONTH', p_check_date) AS varchar(2)), 2, '0');
	v_day   varchar(2)  default  LPAD(CAST(date_part('DAY', p_check_date)   AS varchar(2)), 2, '0');
	v_date  varchar(30) default  to_char(p_check_date, 'dd-mm-yyyy hh24:mi:ss');

	v_res bigint;
	record record;
  begin
    for record in (select *
	  			     from test.check_sql
	  				where check_id = p_check_id) loop
      v_sql_text := replace(record.sql_text, ':YEAR:', v_year);
      v_sql_text := replace(v_sql_text, ':MONTH:', v_month);
      v_sql_text := replace(v_sql_text, ':DAY:', v_day);
      v_sql_text := replace(v_sql_text, ':DATE:', v_date);
	  -- RAISE NOTICE 'sql_text is: %', v_sql_text;
	  select count(*) into v_res from test.check_result where check_sql = v_sql_text and check_date = p_check_date;
	  if v_res = 1 then
	    delete from test.check_result where check_sql = v_sql_text and check_date = p_check_date;
--		commit; if autocommit true
	  end if;
	  execute v_sql_text into v_res;
	  insert into test.check_result (check_id
	                              ,  check_suite
		                          ,  check_val
		                          ,  check_sql
		                          ,  check_date)
		         		     select record.check_id
		  	                      , record.check_suite
		                          , v_res::numeric
		                          , v_sql_text
		                          , p_check_date;
	  -- RAISE NOTICE 'v_res is: %', v_res;
	end loop;
--	commit; if autocommit true
  end;
$BODY$;