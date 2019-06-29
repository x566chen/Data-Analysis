-- PART 2
-- Only Select granted to a casual user
DROP USER IF EXISTS 'casual'@'localhost';
CREATE USER 'casual'@'localhost';
GRANT SELECT ON yelp_db.* TO 'casual'@'localhost'; 
flush PRIVILEGES;

-- Compared with casual user, logged in user are allowed to write a review UID
DROP USER IF EXISTS 'logged_in'@'localhost';
CREATE USER 'logged_in'@'localhost'IDENTIFIED BY '2';
GRANT SELECT ON yelp_db.* TO 'logged_in'@'localhost';
GRANT INSERT, UPDATE ,DELETE ON yelp_db.review TO 'logged_in'@'localhost'; 

-- Enable an analyst to create view
DROP USER IF EXISTS 'analyst'@'localhost';
CREATE USER 'analyst'@'localhost'IDENTIFIED BY '3';
GRANT SELECT ON yelp_db.* TO 'analyst'@'localhost';
GRANT CREATE VIEW ON yelp_db.* TO 'analyst'@'localhost';

-- Enable a developer to do some operations to the database, including creating new table and index
DROP USER IF EXISTS 'developer'@'localhost';
CREATE USER 'developer'@'localhost'IDENTIFIED BY '4';
GRANT SELECT, INSERT, UPDATE ,DELETE ON yelp_db.* TO 'developer'@'localhost';
GRANT CREATE VIEW ON yelp_db.* TO 'developer'@'localhost';
GRANT CREATE ON yelp_db.* TO 'developer'@'localhost';
GRANT INDEX ON yelp_db.* TO 'developer'@'localhost';

-- Enable everything to a host
DROP USER IF EXISTS 'host'@'localhost';
CREATE USER 'host'@'localhost'IDENTIFIED BY '5';
GRANT ALL ON yelp_db.* TO 'host'@'localhost' WITH GRANT OPTION;
