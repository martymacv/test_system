-- PROCEDURE: aqa.exec_check()

-- DROP PROCEDURE IF EXISTS aqa.exec_check();

CREATE OR REPLACE PROCEDURE aqa.exec_check(
	)
LANGUAGE 'plpgsql'
AS $BODY$
  declare
    v_dq_id numeric;
	record record;
  begin
    for record in select * from aqa.check_sql loop
	  insert into aqa.check_val (dq_id) values (record.dq_id);
	end loop;
  end
$BODY$;
ALTER PROCEDURE aqa.exec_check()
    OWNER TO postgres;
