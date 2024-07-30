create or replace procedure ei.forecast_income_for_the_year_ahead(
	p_base_salary FLOAT)
LANGUAGE 'plpgsql'
AS $BODY$
  declare
	v_salary_date DATE;
	v_salary FLOAT;
	record record;
  begin
    for record in (select * 
	  			     from ei.calendar 
	                where salary_date >= date_trunc('day', NOW())
	                  and (DATE_PART('DAY', salary_date) = 5
	  				   or DATE_PART('DAY', salary_date) = 20)
	  				  -- and DATE_PART('YEAR', salary_date) = 2024
	                order by salary_date) loop
	  select max(salary_date) into v_salary_date from ei.calendar where is_workday = true and salary_date between record.salary_date - 15 and record.salary_date;
	  select split_month(case when DATE_PART('DAY', v_salary_date) > 15 then DATE_PART('MONTH', v_salary_date) else DATE_PART('MONTH', v_salary_date) - 1 end) into v_salary;
	  v_salary := case when DATE_PART('DAY', v_salary_date) > 15 then v_salary * p_base_salary else (1 - v_salary) * p_base_salary end;
	  insert into ei.income (salary_date, salary) values (v_salary_date, v_salary);
	end loop;
  end
$BODY$;

-- call forecast_income_for_the_year_ahead(280000.00)

-- select now()
	
create or replace function ei.split_month(
	p_month FLOAT
) returns FLOAT
LANGUAGE 'plpgsql'
AS $BODY$
	declare
		v_over FLOAT;
		v_part FLOAT;
		v_res FLOAT;
	begin
		select count(salary_date) into v_over from ei.calendar where is_workday = true and date_trunc('month', salary_date) = to_date('01-'||to_char(p_month,'fm00')||'-2024', 'dd-mm-yyyy');
		select count(salary_date) into v_part from ei.calendar where is_workday = true and date_trunc('month', salary_date) = to_date('01-'||to_char(p_month,'fm00')||'-2024', 'dd-mm-yyyy') and date_trunc('day', salary_date) <= to_date('15-'||to_char(p_month,'fm00')||'-2024', 'dd-mm-yyyy');
		v_res := v_part/v_over;
		return v_res;
	end
$BODY$;

-- select split_month(7)
-- DROP FUNCTION split_month(integer)
-- select count(salary_date) from ei.calendar where is_workday = true and date_trunc('month', salary_date) = to_date('01-'||to_char(11,'fm00')||'-2024', 'dd-mm-yyyy') and date_trunc('day', salary_date) <= to_date('15-'||to_char(11,'fm00')||'-2024', 'dd-mm-yyyy')