CREATE TABLE `Customer` (
  `CustomerID` integer PRIMARY KEY,
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
  `PizzaID` integer PRIMARY KEY,
  `Name` varchar(255),
  `Description` text,
  `Price` decimal,
  `IsVegetarian` boolean,
  `IsVegan` boolean
);

CREATE TABLE `Ingredient` (
  `IngredientID` integer PRIMARY KEY,
  `Name` varchar(255),
  `Cost` decimal
);

CREATE TABLE `Drink` (
  `DrinkID` integer PRIMARY KEY,
  `Name` varchar(255),
  `Price` decimal
);

CREATE TABLE `Dessert` (
  `DessertID` integer PRIMARY KEY,
  `Name` varchar(255),
  `Price` decimal
);

CREATE TABLE `Order` (
  `OrderID` integer PRIMARY KEY,
  `CustomerID` integer,
  `OrderDate` timestamp,
  `OrderStatus` varchar(255),
  `EstimatedDeliveryTime` timestamp,
  `TotalPrice` decimal,
  `DiscountApplied` boolean,
  `DeliveryPersonID` integer
);

CREATE TABLE `OrderItem` (
  `OrderItemID` integer PRIMARY KEY,
  `OrderID` integer,
  `ItemType` varchar(255) COMMENT 'Pizza, Drink, Dessert',
  `ItemID` integer,
  `Quantity` integer,
  `Price` decimal
);

CREATE TABLE `DiscountCode` (
  `DiscountCodeID` integer PRIMARY KEY,
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
  `DeliveryPersonID` integer PRIMARY KEY,
  `Name` varchar(255),
  `AssignedPostalCode` varchar(255),
  `IsAvailable` boolean
);

CREATE TABLE `Delivery` (
  `DeliveryID` integer PRIMARY KEY,
  `OrderID` integer,
  `DeliveryPersonID` integer,
  `DeliveryStatus` varchar(255),
  `DeliveryTime` timestamp
);

CREATE TABLE `EarningsReport` (
  `ReportID` integer PRIMARY KEY,
  `Month` integer,
  `Year` integer,
  `TotalEarnings` decimal,
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
