\c code_challenge

DROP TABLE favorites;
DROP INDEX reviews_continuation_token_idx;
DROP INDEX reviews_date_idx;
DROP TABLE reviews;

\c postgres

DROP DATABASE code_challenge;
DROP USER challenger;