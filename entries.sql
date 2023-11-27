-- Insert users (seller and customer)
INSERT INTO user (name, phone, email, address, password) VALUES
('Seller1', '1234567890', 'seller1@example.com', 'Seller Address 1', 'seller1pass'),
('Customer1', '9876543210', 'customer1@example.com', 'Customer Address 1', 'customer1pass');

-- Insert raw materials
INSERT INTO raw_material (name, price, exp_time, quantity_left) VALUES
('RawMaterial1', 50, '2023-12-31 23:59:59', 100),
('RawMaterial2', 75, '2023-12-31 23:59:59', 150);

-- Insert recipes
INSERT INTO recipe (name, description) VALUES
('Recipe1', 'Description for Recipe1'),
('Recipe2', 'Description for Recipe2');

-- Insert buys (customer buying recipes)
INSERT INTO buys (user_id, recipe_id, transaction_time, instances, cost_price) VALUES
(2, 1, '2023-11-01 12:30:00', 2, 100),
(2, 2, '2023-11-02 14:45:00', 1, 75);

-- Insert sells (seller selling raw materials)
INSERT INTO sells (user_id, raw_material_id, transaction_time, units, price, exp_time, status) VALUES
(1, 1, '2023-11-03 10:00:00', 50, 50, '2023-12-31 23:59:59', 'approved'),
(1, 2, '2023-11-04 11:15:00', 100, 70, '2023-12-31 23:59:59', 'pending');

-- Insert ingredients (linking recipes with raw materials)
INSERT INTO ingredient (recipe_id, raw_material_id, quantity_required) VALUES
(1, 1, 5),
(1, 2, 3),
(2, 2, 2);
