-- Inserts
INSERT INTO orders (order_id, customer_id, product_id, order_date, order_status, quantity, price, is_deleted) VALUES
('ORD010', 'CUST008', 'PROD006', '2024-01-02 10:15:00', 'Pending', 1, 45.00, FALSE),
('ORD011', 'CUST012', 'PROD010', '2024-01-05 11:45:00', 'Completed', 3, 20.00, FALSE),
('ORD012', 'CUST030', 'PROD019', '2024-01-10 09:30:00', 'Pending', 2, 78.00, FALSE);

-- Updates
UPDATE orders SET order_status = 'Katappa', quantity = 777 WHERE order_id = 'ORD010';
UPDATE orders SET order_status = 'Katappa', quantity = 777 WHERE order_id = 'ORD011';

-- Inserts
INSERT INTO customers (customer_id, first_name, last_name, email, address, phone_number, is_deleted) VALUES
('CUST031', 'Sam', 'Taylor', 'sam.taylor@example.com', '111 First St, Boston', '+12005550111', FALSE),
('CUST032', 'Lily', 'Evans', 'lily.evans@example.com', '222 Oak St, Denver', '+13005550222', FALSE),
('CUST033', 'Harry', 'Potter', 'harry.potter@example.com', '4 Privet Drive, Surrey', '+14005550333', FALSE);

-- Updates
UPDATE customers SET address = 'Shaitan Gali', phone_number = '+10000000000' WHERE customer_id = 'CUST012';
UPDATE customers SET email = 'updated.bob@example.com' WHERE customer_id = 'CUST028';


-- Inserts
INSERT INTO products (product_id, product_name, category, price, stock_quantity, is_deleted) VALUES
('PROD030', 'Bluetooth Speaker', 'Electronics', 150.00, 80, FALSE),
('PROD031', 'VR Headset', 'Gaming', 299.99, 25, FALSE),
('PROD032', 'Graphics Card', 'Computer Hardware', 499.99, 60, FALSE);

-- Updates
UPDATE products SET stock_quantity = 9999 WHERE product_id = 'PROD006';
UPDATE products SET price = 9999 WHERE product_id = 'PROD019';
