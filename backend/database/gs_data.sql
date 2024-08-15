-- Insert records into the 'uom' table
INSERT INTO `gs`.`uom` (`uom_name`) VALUES ('kg');
INSERT INTO `gs`.`uom` (`uom_name`) VALUES ('each');

-- Insert records into the 'products' table
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('toothpaste', 2, 1200);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('rice', 1, 400);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('meat', 1, 3000);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('fish', 1, 3500);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('broiler chicken', 2, 5000);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('sugar (powder)', 1, 500);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('sugar (pieces)', 2, 1000);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('oil (bottle)', 2, 1000);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('soap', 2, 350);
INSERT INTO `gs`.`products` (`name`, `uom_id`, `price_per_unit`) VALUES ('domestic gas (12kg bottle)', 2, 6500);

-- Insert records into the 'orders' table
INSERT INTO `gs`.`orders` (`customer_name`, `total`, `date`) VALUES ('Tony', 2000, '2024-08-13 00:00:00');

-- Insert records into the 'order_details' table
INSERT INTO `gs`.`order_details` (`order_id`, `product_id`, `quantity`, `total_price`) VALUES (1, 1, 2, 2400);

-- Join products with units of measure (uom) tables
SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name FROM products INNER JOIN uom ON products.uom_id=uom.uom_id;
