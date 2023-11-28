-- Users
INSERT INTO user (role, name, phone, email, address, password)
VALUES
  ('customer', 'John Doe', '1234567890', 'john.doe@example.com', '123 Main St', 'password123'),
  ('seller', 'Jane Seller', '9876543210', 'jane.seller@example.com', '456 Market St', 'password456');

-- Raw Materials
INSERT INTO raw_material (name, price, exp_time, quantity_left)
VALUES
  ('Flour', 5, '2023-12-31 00:00:00', 100),
  ('Sugar', 3, '2023-12-31 00:00:00', 50),
  ('Eggs', 2, '2023-12-31 00:00:00', 75);

-- Recipes
INSERT INTO recipe (name, description)
VALUES
  ('Chocolate Cake', 'A delicious chocolate cake recipe'),
  ('French Bread', 'A classic French bread recipe'),
  ('Blueberry Muffins', 'Homemade blueberry muffins recipe');

-- Buys (Customer purchases recipes)
INSERT INTO buys (user_id, recipe_id, transaction_time, instances, cost_price, selling_price)
VALUES
  (1, 1, '2023-11-01 12:00:00', 2, 10, 15),
  (1, 2, '2023-11-02 14:30:00', 1, 5, 8),
  (1, 3, '2023-11-03 10:00:00', 3, 12, 18);

-- Sells (Seller sells raw materials)
INSERT INTO sells (user_id, raw_material_id, transaction_time, units, price, exp_time, status)
VALUES
  (2, 1, '2023-11-01 10:00:00', 50, 4, '2023-12-31 00:00:00', 'approved'),
  (2, 2, '2023-11-02 09:30:00', 25, 2.5, '2023-12-31 00:00:00', 'approved'),
  (2, 3, '2023-11-03 08:45:00', 30, 1.5, '2023-12-31 00:00:00', 'approved'),
  (2, 1, '2023-11-04 11:00:00', 40, 3.5, '2023-12-31 00:00:00', 'approved'),
  (2, 2, '2023-11-05 12:30:00', 20, 2, '2023-12-31 00:00:00', 'approved'),
  (2, 3, '2023-11-06 09:15:00', 25, 1.25, '2023-12-31 00:00:00', 'approved'),
  (2, 1, '2023-11-07 08:30:00', 35, 4, '2023-12-31 00:00:00', 'approved'),
  (2, 2, '2023-11-08 14:45:00', 15, 2.75, '2023-12-31 00:00:00', 'approved'),
  (2, 3, '2023-11-09 10:20:00', 28, 1.75, '2023-12-31 00:00:00', 'approved'),
  (2, 1, '2023-11-10 11:45:00', 45, 3.25, '2023-12-31 00:00:00', 'approved'),
  (2, 2, '2023-11-11 09:00:00', 22, 2.25, '2023-12-31 00:00:00', 'approved'),
  (2, 3, '2023-11-12 08:15:00', 30, 1.5, '2023-12-31 00:00:00', 'approved');


-- Ingredient (Raw materials required for recipes)
INSERT INTO ingredient (recipe_id, raw_material_id, quantity_required)
VALUES
  (1, 1, 2),
  (1, 2, 1),
  (2, 1, 4),
  (2, 2, 2),
  (2, 3, 1),
  (3, 2, 2),
  (3, 3, 1);
