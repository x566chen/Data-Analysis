-- business
delete from business where is_open = 0;
#delete from business where id not in(select distinct business_id from hours where `hours_day` is not null and `hours` <>'');

-- average stars show much different from review table
drop view  if exists stars_review;
create view stars_review as 
(SELECT AVG(review.stars) avg_stars, review.business_id 
FROM  review, business 
WHERE review.business=business.id 
GROUP BY review.business_id);

delete from business 
where id = ANY(SELECT distinct business_id as vid 
FROM stars_review 
WHERE stars_review.business_id = business.id AND abs(business.stars - stars_review.avg_stars)> 0.5); 

-- count of review be smaller than that of review table, modify according to review
drop view if exists review_bnum;
CREATE VIEW review_bnum AS
(SELECT count(review.business_id) review_n, review.business_id
FROM  review, business
WHERE review.business_id =business.id
GROUP BY review.business_id);

update business,review_bnum
set business.review_count = case when ( business.review_count < review_bnum.review_n) then review_bnum.review_n else business.review_count END
where review_bnum.business_id= business.id;

-- user
delete from user WHERE YEAR(yelping_since) < 2004;
delete FROM user WHERE YEAR(yelping_since) >2018;

-- average stars show much difference from review table
drop view if exists stars_user;
CREATE VIEW stars_user AS 
(SELECT AVG(review.stars) avg_stars, review.user_id 
FROM  review, user 
WHERE review.user_id =user.id 
GROUP BY review.user_id);


delete from user 
where id = any(SELECT distinct user.id as id 
FROM stars_user 
WHERE stars_user.user_id = user.id AND abs(user.average_stars - stars_user.avg_stars)> 0.5);


-- count of reviews written by user cannot be smaller than data in review table
drop view if exists review_num;
CREATE VIEW review_num AS
(SELECT count(review.user_id) review_n, review.user_id
FROM  review, user
WHERE review.user_id =user.id
GROUP BY review.user_id);

update user,review_num
set user.review_count = case when ( user.review_count < review_num.review_n) then review_num.review_n else user.review_count END
where review_num.user_id= user.id;

-- friend
delete from friend where friend_id not in (select id from user);
delete from friend where user_id not in (select id from user);

-- elite_years
delete from elite_years where user_id not in (select id from user);
delete FROM elite_years WHERE CONVERT(year USING utf8) < 2004;
delete FROM elite_years WHERE CONVERT(year USING utf8) > 2018;

-- attribute
delete from attribute where business_id not in (select id from business);

-- checkin
delete from checkin where business_id not in (select id from business);

-- photo
delete from photo where business_id not in (select id from business);

-- category
delete from category where business_id not in (select id from business);

-- hours_day
delete from hours_day where business_id not in (select id from business);

-- tip
delete from tip where business_id not in (select id from business);
delete from tip where user_id not in (select id from user);
delete FROM tip WHERE YEAR(date) < 2004;
delete FROM tip WHERE YEAR(date) > 2018;

-- review
delete from review where business_id not in (select id from business);
delete from review where user_id not in (select id from user);
delete FROM review WHERE YEAR(date) < 2004;
delete FROM review WHERE YEAR(date) > 2018;

