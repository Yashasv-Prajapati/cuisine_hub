CREATE PROCEDURE `login` (
	IN u_email VARCHAR(50),
    IN u_role VARCHAR(10),
    OUT hashed_password VARCHAR(500)
    )
BEGIN
	-- Check if the provided email and role match a user
    DECLARE user_exists INT;
    
    SELECT COUNT(*) INTO user_exists
    FROM user
    WHERE email = u_email AND role = u_role;

    IF user_exists > 0 THEN
        -- If the user exists, get the hashed password
        SELECT password INTO hashed_password
        FROM user
        WHERE email = u_email AND role = u_role;
    ELSE
        -- If no matching user is found, set hashed_password to NULL
        SET hashed_password = NULL;
    END IF;
END


CREATE PROCEDURE `register`(in u_name varchar(50), in u_email varchar(50), in u_password varchar(500), in u_phone varchar(15), in u_address varchar(100), in u_role varchar(10) )
BEGIN
	DECLARE email_count INT;

    SELECT COUNT(*) INTO email_count
    FROM user
    WHERE email = u_email;

    IF email_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email already in use';
    ELSE
		insert into user (role, name, phone, email, address, password)
		values (u_role, u_name, u_phone, u_email, u_address, u_password);
	END IF;
END

CREATE PROCEDURE `request_to_sell`(
    IN u_name VARCHAR(50),
    IN u_email VARCHAR(50),
    IN u_role VARCHAR(10),
    IN rm_name VARCHAR(50),
    IN rm_price INT,
    IN rm_exp_time TIMESTAMP,
    IN rm_quantity_left INT)
BEGIN
	declare seller_id int;
    declare raw_material_id int;
    
	-- Check if the user has the required role (seller)
    IF u_role != 'seller' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Only sellers are allowed to create selling requests';
    END IF;
    
    -- find seller
    select id into seller_id
    from user where
    user.email = u_email AND
    user.name=u_name AND
    user.role=u_role;

    -- find raw material id
    select id into raw_material_id
    from raw_material where
    raw_material.name = rm_name

    -- Check if the raw material and seller exists
    IF (raw_material_id IS NOT NULL AND seller_id IS NOT NULL) THEN
        INSERT INTO sells (user_id, raw_material_id,exp_time, transaction_time, units, status, price)
        VALUES (seller_id, raw_material_id, rm_exp_time, NOW(), rm_quantity_left, 'pending', rm_price);
    ELSE -- one of them don't exist
        IF raw_material_id IS NULL THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Raw material with the provided name does not exist';
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Seller with the provided email does not exist';
        END IF;
        
    END IF;
    
END

CREATE PROCEDURE `get_recipes`()
BEGIN
	SELECT id,name, description FROM recipe;
END

CREATE PROCEDURE `place_order` (
    IN u_name VARCHAR(50),
    IN u_email VARCHAR(50),
    IN u_role VARCHAR(10),
    IN u_recipe_id INT,
    IN u_quantity INT,
    IN u_amount_paid INT
    )
BEGIN
	DECLARE u_id INT;
    DECLARE r_available INT;

    -- Step 1: Get user ID based on email
    SELECT id INTO u_id
    FROM user
    WHERE email = u_email;

    -- Check if the user exists
    IF u_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User with the provided email does not exist';
    ELSE
        -- Step 2: Check if the user role matches the provided role
        SELECT role INTO @user_role
        FROM user
        WHERE id = u_id;

        IF u_role != @user_role THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'User role does not match the provided role';
        ELSE
            -- Step 3: Get recipe available quantity
            SELECT available INTO r_available
            FROM recipe
            WHERE id = u_recipe_id;

            -- Check if the recipe exists and has sufficient available quantity
            IF r_available IS NULL OR u_quantity > r_available THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Invalid recipe or insufficient available quantity';
            ELSE
                -- Step 4: Insert order record
                INSERT INTO buys (user_id, recipe_id, transaction_time, instances, amount_paid)
                VALUES (u_id, u_recipe_id, NOW(), u_quantity, u_amount_paid);

                -- Step 5: Update recipe available quantity
                UPDATE recipe
                SET available = r_available - u_quantity
                WHERE id = u_recipe_id;
            END IF;
        END IF;
    END IF;
END

CREATE PROCEDURE add_raw_materials_to_recipe(IN p_recipe_id INT, IN p_raw_material_name VARCHAR(255), IN p_quantity INT)
BEGIN
    DECLARE v_raw_material_id INT;
    
    -- Check if raw material already exists
    SELECT id INTO v_raw_material_id FROM raw_material WHERE name = p_raw_material_name LIMIT 1;

    -- If raw material does not exist, add it to the raw_material table
    IF v_raw_material_id IS NULL THEN
        INSERT INTO raw_material (name) VALUES (p_raw_material_name);
        SET v_raw_material_id = LAST_INSERT_ID();
    END IF;

    -- Add raw material to the ismadeof table
    INSERT INTO ingredient (recipe_id, raw_material_id, quantity_required)
    VALUES (p_recipe_id, v_raw_material_id, p_quantity);
END

CREATE PROCEDURE add_recipe(IN p_recipe_name VARCHAR(255),IN p_recipe_descr VARCHAR(255))
BEGIN
    DECLARE v_recipe_id INT;
    
    -- Check if the recipe already exists
    SELECT id INTO v_recipe_id FROM recipe WHERE name = p_recipe_name LIMIT 1;
    
    -- If the recipe does not exist, add it to the recipe table
    IF v_recipe_id IS NULL THEN
        INSERT INTO recipe (name,description) VALUES (p_recipe_name, p_recipe_descr);
        SET v_recipe_id = LAST_INSERT_ID();
    END IF;
END
