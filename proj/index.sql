-- Query to verify business id in table hours
-- TABLES WITH BUSINESS
ALTER TABLE `hours_day` ADD INDEX `idx_hours_day_businessid` (`business_id`) USING BTREE;

-- Query to verify business id in table category
ALTER TABLE `category` ADD INDEX `idx_category_businessid` (`business_id`) USING BTREE;

-- Query to verify business id in table attribute
ALTER TABLE `attribute` ADD INDEX `idx_attribute_businessid` (`business_id`) USING BTREE;

-- Query to verify business id in table check in
ALTER TABLE `checkin` ADD INDEX `idx_checkin_businessid` (`business_id`) USING BTREE;

-- Query to verify business id in table tip
ALTER TABLE `tip` ADD INDEX `idx_tip_businessid` (`business_id`) USING BTREE;

-- Query to verify business id in table photo
ALTER TABLE `photo` ADD INDEX `idx_photo_businessid` (`business_id`) USING BTREE;

-- Query to verify business id in review
ALTER TABLE `review` ADD INDEX `idx_review_businessid` (`business_id`) USING BTREE;

-- TABLES WITH USER
-- Query to verify user id in review
ALTER TABLE `review` ADD INDEX `idx_review_userid` (`user_id`) USING BTREE;

-- Query to verify user id in friend
ALTER TABLE `friend` ADD INDEX `idx_friend_userid` (`user_id`) USING BTREE;

-- Query to verify user id in table elite_years
ALTER TABLE `elite_years` ADD INDEX `idx_elite_years_userid` (`user_id`) USING BTREE;

-- Query to verify user id in table tip
ALTER TABLE `tip` ADD INDEX `idx_tip_userid` (`user_id`) USING BTREE;

-- CHECK SELF-CONSISTENCY IN THE TABLE FRIEND WHICH HAS INFORMATION ABOUT USER.
ALTER TABLE `friend` ADD INDEX `idx_friendid_userid` (`friend_id`) USING BTREE;