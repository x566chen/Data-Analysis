DROP TABLE if exists hours_day;
create table hours_day(
id int AUTO_INCREMENT, 
business_id varchar(30), 
Monday_start varchar(10),
Monday_end varchar(10),
Tuesday_start varchar(10),
Tuesday_end varchar(10),
Wednesday_start varchar(10),
Wednesday_end varchar(10),
Thursday_start varchar(10),
Thursday_end varchar(10),
Friday_start varchar(10),
Friday_end varchar(10),
Saturday_start varchar(10),
Saturday_end varchar(10),
Sunday_start varchar(10),
Sunday_end varchar(10),
primary key (id),
foreign key (business_id) REFERENCES business (id)
);

insert into hours_day(business_id,
Monday_start,
Monday_end,
Tuesday_start,
Tuesday_end,
Wednesday_start,
Wednesday_end,
Thursday_start,
Thursday_end,
Friday_start,
Friday_end,
Saturday_start,
Saturday_end,
Sunday_start,
Sunday_end)

select business_id,
group_concat(Monday_start) as Monday_start,
group_concat(Monday_end) as Monday_end,
group_concat(Tuesday_start) as Tuesday_start,
group_concat(Tuesday_end) as Tuesday_end,
group_concat(Wednesday_start) as Wednesday_start,
group_concat(Wednesday_end) as Wednesday_end,
group_concat(Thursday_start) as Thursday_start,
group_concat(Thursday_end) as Thursday_end,
group_concat(Friday_start) as Friday_start,
group_concat(Friday_end) as Friday_end,
group_concat(Saturday_start) as Saturday_start,
group_concat(Saturday_end) as Saturday_end,
group_concat(Sunday_start) as Sunday_start,
group_concat(Sunday_end) as Sunday_end 
from 
(select business_id,
case when substr(hours, 1, position('|' in hours)-1) = 'Monday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Monday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Monday' then
substr(hours,position('-' in hours)+1) end as Monday_end,
case when substr(hours, 1, position('|' in hours)-1) = 'Tuesday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Tuesday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Tuesday' then
substr(hours,position('-' in hours)+1) end as Tuesday_end,
case when substr(hours, 1, position('|' in hours)-1) = 'Wednesday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Wednesday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Wednesday' then
substr(hours,position('-' in hours)+1) end as Wednesday_end,
case when substr(hours, 1, position('|' in hours)-1) = 'Thursday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Thursday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Thursday' then
substr(hours,position('-' in hours)+1) end as Thursday_end,
case when substr(hours, 1, position('|' in hours)-1) = 'Friday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Friday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Friday' then
substr(hours,position('-' in hours)+1) end as Friday_end,
case when substr(hours, 1, position('|' in hours)-1) = 'Saturday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Saturday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Saturday' then
substr(hours,position('-' in hours)+1) end as Saturday_end,
case when substr(hours, 1, position('|' in hours)-1) = 'Sunday' then
substr(hours,position('|' in hours)+1, position('-' in hours)-position('|' in hours)-1) end as Sunday_start,
case when substr(hours, 1, position('|' in hours)-1) = 'Sunday' then
substr(hours,position('-' in hours)+1) end as Sunday_end from hours) as h
group by business_id;