-- success
ALTER TABLE hours ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;

ALTER TABLE checkin ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;

ALTER TABLE tip ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;
ALTER TABLE tip ADD FOREIGN KEY ( user_id ) REFERENCES user ( id ) ;

ALTER TABLE review ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;
ALTER TABLE review ADD FOREIGN KEY ( user_id ) REFERENCES user ( id ) ;

-- success
ALTER TABLE photo ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;

ALTER TABLE friend ADD FOREIGN KEY ( user_id ) REFERENCES user ( id ) ;
##ALTER TABLE friend ADD FOREIGN KEY ( friend_id ) REFERENCES user ( id ) ;

ALTER TABLE elite_years ADD FOREIGN KEY ( user_id ) REFERENCES user ( id ) ;

ALTER TABLE category ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;

ALTER TABLE attribute ADD FOREIGN KEY ( business_id ) REFERENCES business ( id ) ;