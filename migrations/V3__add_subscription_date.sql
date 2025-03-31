-- V3__add_subscription_date.sql

ALTER TABLE subscribers
ADD COLUMN subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP; 