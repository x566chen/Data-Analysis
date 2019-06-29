-- check hours_day index
  (SELECT id
   FROM hours_day
     LEFT JOIN `business`
       ON hours_day.business_id= `business`.`id`
   WHERE `business`.`id` IS NULL
  );

-- check category index
SELECT * FROM category where substr(business_id,1,1) = 'X';
  
-- check attribute index
SELECT * FROM attribute where substr(business_id,1,1) = 'X';

-- check checkin index
SELECT * FROM checkin where substr(business_id,1,1) = '7';

-- check tip index
SELECT * FROM tip where user_id='blrWvPePSv87aU9hV1Zd8Q';
SELECT * FROM tip where business_id='k7WRPbDd7rztjHcGGkEjlw';

-- check photo index
SELECT * FROM photo where substr(business_id,1,1) = 'X';
  
-- check review index
select count(distinct business_id) from review;
select count(distinct user_id) from review;

-- check friend index
select count(distinct friend_id) from friend;
select count(distinct user_id) from friend;


-- check elite_years
select count(distinct user_id) from elite_years;