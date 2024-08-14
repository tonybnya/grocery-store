-- Create the 'gs' database if it does not exists
CREATE DATABASE IF NOT EXISTS `gs`;

-- Select the 'gs' database for use
USE `gs`;

-- Create the 'products' table with the necessary columns and primary key
CREATE TABLE `gs`.`products` (
    `product_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `uom_id` INT NOT NULL,
    `price_per_unit` DOUBLE NOT NULL,
    PRIMARY KEY (`product_id`)
);

-- Create the 'uom' (Unit of Measure) table with the necessary columns and primary key
CREATE TABLE `gs`.`uom` (
    `uom_id` INT NOT NULL AUTO_INCREMENT,
    `uom_name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`uom_id`)
);

-- Add a foreign key constraint on 'uom_id' in the 'products' table to reference 'uom_id' in the 'uom' table
ALTER TABLE `gs`.`products`
ADD CONSTRAINT `fk_uom_id`
FOREIGN KEY (`uom_id`)
REFERENCES `gs`.`uom` (`uom_id`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

-- Create the 'orders' table with the necessary columns and primary key
CREATE TABLE `gs`.`orders` (
    `order_id` INT NOT NULL AUTO_INCREMENT,
    `customer_name` VARCHAR(100) NOT NULL,
    `total` DOUBLE NOT NULL,
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`order_id`)
);

-- Create the 'order_details' table with the necessary columns and constraints
CREATE TABLE `gs`.`order_details` (
    `order_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `quantity` DOUBLE NOT NULL,
    `total_price` DOUBLE NOT NULL,
    PRIMARY KEY (`order_id`),
    INDEX `fk_product_id_idx` (`product_id` ASC),
    CONSTRAINT `fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `gs`.`orders` (`order_id`) ON DELETE NO ACTION ON UPDATE RESTRICT,
    CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `gs`.`products` (`product_id`) ON DELETE NO ACTION ON UPDATE RESTRICT
);
