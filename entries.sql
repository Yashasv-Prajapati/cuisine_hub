-- Users
INSERT INTO user (name, phone, email, address, password) VALUES
('John Doe', '1234567890', 'john@example.com', '123 Main St', 'hashed_password_1'),
('Alice Smith', '9876543210', 'alice@example.com', '456 Oak St', 'hashed_password_2'),
('Bob Johnson', '5551234567', 'bob@example.com', '789 Pine St', 'hashed_password_3');

-- Raw Materials
INSERT INTO raw_material (name, price, transaction_time, exp_time, quantity_left, user_id, status) VALUES
('Flour', 5, '2023-11-01 08:00:00', '2024-11-01 08:00:00', 100, 1, 'approved'),
('Sugar', 3, '2023-11-02 10:00:00', '2024-11-02 10:00:00', 150, 1, 'pending'),
('Eggs', 2, '2023-11-03 12:00:00', '2024-11-03 12:00:00', 50, 2, 'approved');

-- Recipes
INSERT INTO recipe (name, description) VALUES
('Chocolate Cake', 'A delicious chocolate cake recipe'),
('Pancakes', 'Classic pancake recipe');

-- Buys (Customer-Recipe Relationship)
INSERT INTO buys (user_id, recipe_id, transaction_time, instances, cost_price) VALUES
(1, 1, '2023-11-04 14:00:00', 2, 10),  -- John buys Chocolate Cake
(2, 2, '2023-11-05 16:00:00', 1, 5);   -- Alice buys Pancakes

-- Sells (Seller-Raw Material Relationship)
INSERT INTO sells (user_id, raw_material_id, transaction_time) VALUES
(1, 1, '2023-11-06 18:00:00'),  -- John sells Flour
(2, 3, '2023-11-07 20:00:00');  -- Bob sells Eggs

-- is_made_of (Recipe-Raw Material Relationship)
INSERT INTO is_made_of (recipe_id, raw_material_id, quantity_required) VALUES
(1, 1, 3),  -- Chocolate Cake requires 3 units of Flour
(2, 3, 2);  -- Pancakes require 2 units of Eggs
