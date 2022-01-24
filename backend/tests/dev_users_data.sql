DO
$do$
BEGIN
    -- Создание энама доступных пермишенов
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'permission_type') THEN
        CREATE TYPE permission_type AS ENUM ('right:full', 'right:view');
    END IF;

    -- Создание таблицы юзеров
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL,
        username VARCHAR(50) UNIQUE,
        email VARCHAR(50) UNIQUE,
        bio VARCHAR(500),
        hashed_password VARCHAR,
        permission VARCHAR,
        PRIMARY KEY (id)
    );

    -- Создание первого юзера
    IF NOT EXISTS (SELECT 1 FROM users) THEN
        INSERT INTO users (username, email, bio, hashed_password, permission)
            VALUES (
                'admin', 
                'admin@brawlstars.com', 
                'I`ve seen things you people wouldn`t believe... Attack ships on fire off the shoulder of Orion... I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, like tears in rain... Time to die.', 
                '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b', 
                'right:full'
            );
    END IF;
END
$do$