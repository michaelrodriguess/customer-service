CREATE TABLE IF NOT EXISTS customers (
    id CHAR(26) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE UNIQUE INDEX customer_email_idx on customers(email);