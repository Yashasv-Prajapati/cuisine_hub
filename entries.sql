-- Inserting users
INSERT INTO user (name, phone, email, address, password) VALUES
('John Doe', '1234567890', 'john.doe@example.com', '123 Main St', 'password123'),
('Alice Smith', '9876543210', 'alice.smith@example.com', '456 Oak St', 'securepass'),
('Bob Johnson', '5551234567', 'bob.johnson@example.com', '789 Pine St', 'strongpassword');

-- Inserting raw materials
INSERT INTO raw_material (name, price, exp_time, quantity_left) VALUES
('Flour', 5, '2023-12-31', 100),
('Sugar', 3, '2023-12-31', 150),
('Eggs', 2, '2023-12-31', 50),
('Milk', 4, '2023-12-31', 75);

-- Inserting recipes
INSERT INTO recipe (name, description) VALUES
('Chocolate Cake', 'A delicious chocolate cake recipe.'),
('Blueberry Pancakes', 'Fluffy pancakes with fresh blueberries.');

-- Inserting buys
INSERT INTO buys (user_id, recipe_id, transaction_time, instances, cost_price) VALUES
(1, 1, '2023-11-01 12:00:00', 2, 15),
(2, 2, '2023-11-02 14:30:00', 1, 8);

-- Inserting sells
INSERT INTO sells (user_id, raw_material_id, transaction_time, units, price, exp_time, status) VALUES
(1, 1, '2023-11-03 10:00:00', 10, 50, '2023-12-15', 'pending'),
(3, 2, '2023-11-04 11:45:00', 5, 15, '2023-12-20', 'approved');

-- Inserting ingredients
INSERT INTO ingredient (recipe_id, raw_material_id, quantity_required) VALUES
(1, 1, 300), -- Chocolate Cake needs 300g of Flour
(1, 2, 200), -- Chocolate Cake needs 200g of Sugar
(1, 3, 4),   -- Chocolate Cake needs 4 Eggs
(1, 4, 150), -- Chocolate Cake needs 150ml of Milk
(2, 1, 200), -- Blueberry Pancakes need 200g of Flour
(2, 2, 100), -- Blueberry Pancakes need 100g of Sugar
(2, 3, 2),   -- Blueberry Pancakes need 2 Eggs
(2, 4, 100); -- Blueberry Pancakes need 100ml of Milk
