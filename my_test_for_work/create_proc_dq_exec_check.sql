-- PROCEDURE: dq.dq_exec_check()

-- DROP PROCEDURE IF EXISTS dq.dq_exec_check();

CREATE OR REPLACE PROCEDURE dq.dq_exec_check(
	)
LANGUAGE 'plpgsql'
AS $BODY$
  declare
    v_dq_id numeric;
	record record;
  begin
    for record in select * from dq.dq_check_sql loop
	  RAISE NOTICE 'Продукт: %', record.dq_id;
	  insert into dq.dq_check_val (dq_id) values (record.dq_id);
	end loop;
  end
$BODY$;
ALTER PROCEDURE dq.dq_exec_check()
    OWNER TO postgres;
