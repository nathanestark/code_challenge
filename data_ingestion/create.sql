CREATE USER challenger WITH PASSWORD 'abcd1234';
CREATE DATABASE code_challenge;
GRANT ALL PRIVILEGES ON DATABASE code_challenge TO challenger;
\c code_challenge

CREATE TABLE reviews (
	id SERIAL UNIQUE NOT NULL,  /* Separate the data ID from 'public' ID used in API */
	review_id VARCHAR(22) UNIQUE NOT NULL, /* Length: 22 */
	user_id VARCHAR(22),        /* Length: 22 */
	business_id VARCHAR(22),    /* Length: 22 */
	stars FLOAT,                /* 1.0 -> 5.0 */
	useful INT,                 /* -1 -> 1241 */
	funny INT,                  /* 0 -> 1290 */
	cool INT,                   /* -1 -> 506 */
	text VARCHAR,               /* Length: 1 -> 5000 */
	date TIMESTAMP,
	continuation_token VARCHAR(56) /* Continuation token index (stringified date + review_id) */
);
CREATE INDEX reviews_continuation_token_idx ON reviews (date, continuation_token);
GRANT ALL ON reviews TO challenger;
GRANT ALL ON SEQUENCE reviews_id_seq TO challenger;


CREATE TABLE favorites (
    id SERIAL UNIQUE NOT NULL,
    review_id INT,               /* Points to the DB ID, not the 'public' ID */
    FOREIGN KEY (review_id) REFERENCES reviews(id)
);
GRANT ALL ON favorites TO challenger;
GRANT ALL ON SEQUENCE favorites_id_seq TO challenger;
