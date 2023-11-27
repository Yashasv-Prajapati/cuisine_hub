-- Insert entries into user
INSERT INTO user (role, name, phone, email, address, password) VALUES
    ('customer', 'Customer1', '1234567890', 'customer1@example.com', '123 Main St', 'admin'),
    ('customer', 'yashasav_p', '1234567890', 'yamuprajapati05@gmail.com', '123 Main St', '1234'),
    ('seller', 'Seller1', '9876543210', 'seller1@example.com', '456 Oak Ave', 'root');

-- Insert entries into raw_material
INSERT INTO raw_material (name, price, transaction_time, exp_time, quantity_left, user_id) VALUES
    ('Material1', 50, '2023-11-01 12:00:00', '2024-11-01 12:00:00', 100, 2),
    ('Material2', 75, '2023-11-05 14:30:00', '2024-11-05 14:30:00', 150, 2);

-- Insert entries into recipe
INSERT INTO recipe (name, cost_price, selling_price, available) VALUES
    ('Recipe1', 100, 150, 10),
    ('Recipe2', 120, 180, 15);

-- Insert entries into buys
INSERT INTO buys (user_id, recipe_id, transaction_time, instances, amount_paid) VALUES
    (1, 1, '2023-11-10 10:00:00', 2, 300),
    (1, 2, '2023-11-12 11:30:00', 1, 180);

-- Insert entries into sells
INSERT INTO sells (user_id, raw_material_id, transaction_time, status) VALUES
    (2, 1, '2023-11-02 08:00:00', 'approved'),
    (2, 2, '2023-11-06 09:45:00', 'pending');

-- Insert entries into is_made_of
INSERT INTO is_made_of (recipe_id, raw_material_id, quantity_required) VALUES
    (1, 1, 5),
    (2, 2, 8);
