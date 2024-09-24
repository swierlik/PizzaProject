CREATE TABLE `Customer` (
  `CustomerID` integer PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Gender` varchar(255),
  `Birthdate` date,
  `PhoneNumber` varchar(255),
  `Address` varchar(255),
  `Username` varchar(255),
  `Password` varchar(255),
  `PizzasOrderedCount` integer,
  `role` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Pizza` (
  `PizzaID` integer PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Description` text,
  `Price` decimal(10,2),
  `IsVegetarian` boolean,
  `IsVegan` boolean
);

CREATE TABLE `Ingredient` (
  `IngredientID` integer PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Cost` decimal(10,2)
);

CREATE TABLE `Drink` (
  `DrinkID` integer PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Price` decimal(10,2)
);

CREATE TABLE `Dessert` (
  `DessertID` integer PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `Price` decimal(10,2)
);

CREATE TABLE `Orderr` (
  `OrderID` integer PRIMARY KEY AUTO_INCREMENT,
  `CustomerID` integer,
  `OrderDate` timestamp,
  `OrderStatus` varchar(255),
  `EstimatedDeliveryTime` timestamp,
  `TotalPrice` decimal(10,2),
  `DiscountApplied` boolean,
  `DeliveryPersonID` integer
);

CREATE TABLE `OrderItem` (
  `OrderItemID` integer PRIMARY KEY AUTO_INCREMENT,
  `OrderID` integer,
  `ItemType` varchar(255) COMMENT 'Pizza, Drink, Dessert',
  `ItemID` integer,
  `Quantity` integer,
  `Price` decimal(10,2)
);

CREATE TABLE `DiscountCode` (
  `DiscountCodeID` integer PRIMARY KEY AUTO_INCREMENT,
  `Code` varchar(255),
  `Description` text,
  `IsRedeemed` boolean,
  `ExpiryDate` date
);

CREATE TABLE `CustomerDiscount` (
  `CustomerID` integer,
  `DiscountCodeID` integer
);

CREATE TABLE `DeliveryPerson` (
  `DeliveryPersonID` integer PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(255),
  `AssignedPostalCode` varchar(255),
  `IsAvailable` boolean
);

CREATE TABLE `Delivery` (
  `DeliveryID` integer PRIMARY KEY AUTO_INCREMENT,
  `OrderID` integer,
  `DeliveryPersonID` integer,
  `DeliveryStatus` varchar(255),
  `DeliveryTime` timestamp
);

CREATE TABLE `EarningsReport` (
  `ReportID` integer PRIMARY KEY AUTO_INCREMENT,
  `Month` integer,
  `Year` integer,
  `TotalEarnings` decimal(10,2),
  `Region` varchar(255),
  `GenderFilter` varchar(255),
  `AgeFilter` varchar(255)
);

CREATE TABLE `PizzaIngredient` (
  `PizzaID` integer,
  `IngredientID` integer
);

ALTER TABLE `Order` ADD FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`);

ALTER TABLE `Order` ADD FOREIGN KEY (`DeliveryPersonID`) REFERENCES `DeliveryPerson` (`DeliveryPersonID`);

ALTER TABLE `OrderItem` ADD FOREIGN KEY (`OrderID`) REFERENCES `Order` (`OrderID`);

ALTER TABLE `CustomerDiscount` ADD FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`);

ALTER TABLE `CustomerDiscount` ADD FOREIGN KEY (`DiscountCodeID`) REFERENCES `DiscountCode` (`DiscountCodeID`);

ALTER TABLE `Delivery` ADD FOREIGN KEY (`OrderID`) REFERENCES `Order` (`OrderID`);

ALTER TABLE `Delivery` ADD FOREIGN KEY (`DeliveryPersonID`) REFERENCES `DeliveryPerson` (`DeliveryPersonID`);

ALTER TABLE `OrderItem` ADD FOREIGN KEY (`ItemID`) REFERENCES `Pizza` (`PizzaID`);

ALTER TABLE `OrderItem` ADD FOREIGN KEY (`ItemID`) REFERENCES `Drink` (`DrinkID`);

ALTER TABLE `OrderItem` ADD FOREIGN KEY (`ItemID`) REFERENCES `Dessert` (`DessertID`);

ALTER TABLE `PizzaIngredient` ADD FOREIGN KEY (`PizzaID`) REFERENCES `Pizza` (`PizzaID`);

ALTER TABLE `PizzaIngredient` ADD FOREIGN KEY (`IngredientID`) REFERENCES `Ingredient` (`IngredientID`);
