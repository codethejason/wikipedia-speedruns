import pymysql
# Probably want to do this at some point
# http://jan.kneschke.de/projects/mysql/order-by-rand/

DB_NAME='wikipedia_speedruns'

TABLES={}

TABLES['prompts']=(
'''
CREATE TABLE IF NOT EXISTS `prompts` (
    `prompt_id` INT NOT NULL AUTO_INCREMENT,
    `start` VARCHAR(255) NOT NULL,
    `end` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`prompt_id`) 
);
''')

TABLES['runs']=(
'''
CREATE TABLE IF NOT EXISTS `runs` (
    `run_id` INT NOT NULL AUTO_INCREMENT,
    `start_time` TIMESTAMP(3) NOT NULL,
    `end_time` TIMESTAMP(3) NOT NULL,
    `path` TEXT NOT NULL,
    `prompt_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`run_id`),
    FOREIGN KEY (`prompt_id`) REFERENCES `prompts`(`prompt_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
);
''')

TABLES['users']=(
'''
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL UNIQUE,
    `hash` CHAR(60) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `email_confirmed` BOOLEAN NOT NULL DEFAULT 0,
    `admin` BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (`user_id`)
);
''')

def create_tables(cursor):
    for table in TABLES:
        cursor.execute(TABLES[table])

conn = pymysql.connect(user='user', host='127.0.0.1',
                            database=DB_NAME)

with conn.cursor() as cursor:
    create_tables(cursor)
    conn.commit()
    conn.close()
