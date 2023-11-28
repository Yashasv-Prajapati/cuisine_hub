-- Inserting entries for the 'user' table
INSERT INTO user (role, name, phone, email, address, password)
VALUES
('customer', 'Alice Smith', '1234567890', 'alice@email.com', '123 Main St', 'password123'),
('seller', 'Bob Baker', '9876543210', 'bob@email.com', '456 Oak St', 'securepass'),
('customer', 'Charlie Chef', '5551234567', 'charlie@email.com', '789 Maple St', 'pass1234');

-- Inserting entries for the 'raw_material' table
INSERT INTO raw_material (name, price, exp_time, quantity_left)
VALUES
('Flour', 500, '2023-12-31 00:00:00', 1000),
('Sugar', 300, '2023-12-31 00:00:00', 800),
('Eggs', 200, '2023-12-31 00:00:00', 500),
('Butter', 700, '2023-12-31 00:00:00', 300);

-- Inserting entries for the 'recipe' table
INSERT INTO recipe (name, description)
VALUES
('Chocolate Cake', 'A delicious chocolate cake recipe.'),
('Blueberry Pastry', 'A mouth-watering blueberry pastry recipe.'),
('Whole Wheat Bread', 'Healthy whole wheat bread recipe.');

-- Inserting entries for the 'buys' table
INSERT INTO buys (user_id, recipe_id, transaction_time, instances, cost_price, selling_price)
VALUES
(1, 1, '2023-11-28 12:00:00', 2, 800, 1200),
(1, 2, '2023-11-28 13:30:00', 1, 500, 800),
(2, 1, '2023-11-28 14:45:00', 3, 750, 1100),
(3, 3, '2023-11-28 16:00:00', 2, 600, 1000);

-- Inserting entries for the 'sells' table
INSERT INTO sells (user_id, raw_material_id, transaction_time, units, price, exp_time, status)
VALUES
(2, 1, '2023-11-28 12:30:00', 500, 400, '2024-01-31 00:00:00', 'approved'),
(2, 2, '2023-11-28 14:00:00', 300, 250, '2024-01-31 00:00:00', 'pending'),
(3, 3, '2023-11-28 15:15:00', 200, 180, '2024-01-31 00:00:00', 'using'),
(3, 4, '2023-11-28 16:45:00', 100, 600, '2024-01-31 00:00:00', 'finished');

-- Inserting entries for the 'ingredient' table
INSERT INTO ingredient (recipe_id, raw_material_id, quantity_required)
VALUES
(1, 1, 200),
(1, 2, 150),
(1, 3, 3),
(2, 2, 100),
(2, 3, 2),
(2, 4, 50),
(3, 1, 300),
(3, 3, 5);
