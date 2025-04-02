create database if not exists inventory;

use inventory ;

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(255),
    customer_id VARCHAR(255),
    product_id VARCHAR(255),
    order_date DATETIME,
    order_status VARCHAR(50),
    quantity INT,
    price DECIMAL(10, 2),
    lastmodified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (order_id)
);


CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    lastmodified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);



CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    lastmodified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);


INSERT INTO orders (order_id, customer_id, product_id, order_date, order_status, quantity, price) VALUES
('ORD001', 'CUST028', 'PROD023', '2023-08-16 00:56:14', 'Pending', 2, 35.02),
('ORD002', 'CUST030', 'PROD006', '2023-08-16 03:03:08', 'Completed', 1, 48.71),
('ORD003', 'CUST008', 'PROD019', '2023-08-02 09:45:02', 'Completed', 5, 67.06),
('ORD004', 'CUST011', 'PROD010', '2023-08-26 13:47:32', 'Pending', 2, 20.59),
('ORD005', 'CUST024', 'PROD012', '2023-08-16 08:10:25', 'Completed', 1, 59.01),
('ORD006', 'CUST012', 'PROD001', '2023-08-16 19:00:48', 'Pending', 2, 27.91),
('ORD007', 'CUST030', 'PROD025', '2023-08-16 09:07:55', 'Pending', 2, 50.78),
('ORD008', 'CUST002', 'PROD027', '2023-08-12 22:37:38', 'Completed', 1, 91.26),
('ORD009', 'CUST012', 'PROD014', '2023-08-02 00:12:48', 'Pending', 2, 66.55) ;


INSERT IGNORE INTO customers (customer_id, first_name, last_name, email, address, phone_number)
VALUES 
('CUST028', 'Bob', 'Garcia', 'bob.garcia@example.com', '620 Broadway, Chicago', '+19628708430'),
('CUST030', 'John', 'Johnson', 'john.johnson@example.com', '298 Main St, Los Angeles', '+13129313691'),
('CUST008', 'Grace', 'Brown', 'grace.brown@example.com', '265 Highland Ave, Houston', '+11674183789'),
('CUST011', 'Charlie', 'Williams', 'charlie.williams@example.com', '920 Broadway, Chicago', '+12408540485'),
('CUST024', 'Frank', 'Miller', 'frank.miller1@example.com', '599 Second St, New York', '+19681906827'),
('CUST012', 'Eva', 'Garcia', 'eva.garcia@example.com', '543 Broadway, Houston', '+16171168327'),
('CUST002', 'Alice', 'Brown', 'alice.brown@example.com', '436 Main St, New York', '+12561270936'),
('CUST020', 'Charlie', 'Brown', 'charlie.brown@example.com', '577 Second St, New York', '+12220022538'),
('CUST010', 'John', 'Miller', 'john.miller@example.com', '171 Broadway, New York', '+16445041435'),
('CUST021', 'Frank', 'Davis', 'frank.davis1@example.com', '784 Second St, Phoenix', '+11228327530'),
('CUST013', 'David', 'Johnson', 'david.johnson@example.com', '564 Second St, Houston', '+14130497970'),
('CUST003', 'Charlie', 'Smith', 'charlie.smith@example.com', '950 Main St, Houston', '+16830870480'),
('CUST015', 'David', 'Williams', 'david.williams@example.com', '928 Main St, Houston', '+13202186662'),
('CUST009', 'Frank', 'Davis', 'frank.davis@example.com', '553 Highland Ave, Phoenix', '+15511440032');



INSERT INTO products (product_id, product_name, category, price, stock_quantity) VALUES
('PROD023', 'Monitor', 'Office Equipment', 993.13, 316),
('PROD006', 'Headphones', 'Electronics', 984.35, 15),
('PROD019', 'Smartphone', 'Office Equipment', 768.08, 346),
('PROD010', 'Keyboard', 'Electronics', 414.3, 186),
('PROD012', 'Camera', 'Electronics', 393.0, 391),
('PROD001', 'Printer', 'Electronics', 407.29, 145),
('PROD025', 'Tablet', 'Office Equipment', 928.22, 371),
('PROD027', 'Laptop', 'Office Equipment', 325.73, 350),
('PROD014', 'Camera', 'Electronics', 768.01, 128),
('PROD004', 'Smartwatch', 'Office Equipment', 442.78, 100),
('PROD018', 'Monitor', 'Electronics', 552.71, 451),
('PROD008', 'Headphones', 'Accessories', 611.23, 76) ;


-- drop table Products ;

-- select * from orders ;

-- select * from customers ;

-- select * from products ; 
