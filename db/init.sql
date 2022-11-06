CREATE DATABASE sukirai;
use sukirai;
CREATE TABLE comment_data(
    person VARCHAR(16) NOT NULL,
    cid INT NOT NULL,
    ref INT,
    support BOOL NOT NULL,
    comment VARCHAR(1024) NOT NULL
);
ALTER DATABASE sukirai CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE comment_data ADD ctime varchar(30);