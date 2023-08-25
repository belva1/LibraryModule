/* put database initialization script here */

-- for example
CREATE ROLE myuserl WITH ENCRYPTED PASSWORD 'raiders9)' LOGIN;
COMMENT ON ROLE myuserl IS 'docker user for tests';

CREATE DATABASE librarydb OWNER myuserl;
COMMENT ON DATABASE librarydb IS 'docker db for tests owned by docker user';
