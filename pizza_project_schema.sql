CREATE TABLE `customerdiscount` (
  `CustomerID` int NOT NULL,
  `DiscountCodeID` int NOT NULL,
  PRIMARY KEY (`CustomerID`,`DiscountCodeID`),
  KEY `DiscountCodeID` (`DiscountCodeID`),
  CONSTRAINT `customerdiscount_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`),
  CONSTRAINT `customerdiscount_ibfk_2` FOREIGN KEY (`DiscountCodeID`) REFERENCES `discountcode` (`DiscountCodeID`)
);

CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Gender` varchar(255) DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `PhoneNumber` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `PostalCode` varchar(255) DEFAULT NULL,
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `PizzasOrderedCount` int DEFAULT NULL,
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `IsNext10Discount` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `Username` (`Username`)
);

CREATE TABLE `delivery_persons` (
  `DeliveryPersonID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `PostalCode` varchar(255) DEFAULT NULL,
  `IsAvailable` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`DeliveryPersonID`)
);

CREATE TABLE `discountcode` (
  `DiscountCodeID` int NOT NULL AUTO_INCREMENT,
  `Code` varchar(255) NOT NULL,
  `Description` text,
  `IsRedeemed` tinyint(1) NOT NULL,
  `ExpiryDate` date NOT NULL,
  `DiscountPercentage` decimal(10,2) NOT NULL,
  PRIMARY KEY (`DiscountCodeID`)
);

CREATE TABLE `ingredients` (
  `IngredientID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Price` decimal(10,0) NOT NULL,
  `IsVegetarian` tinyint(1) DEFAULT NULL,
  `IsVegan` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`IngredientID`)
);

CREATE TABLE `item_ingredients` (
  `ItemID` int NOT NULL,
  `IngredientID` int NOT NULL,
  PRIMARY KEY (`ItemID`,`IngredientID`),
  KEY `IngredientID` (`IngredientID`),
  CONSTRAINT `item_ingredients_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `items` (`ItemID`),
  CONSTRAINT `item_ingredients_ibfk_2` FOREIGN KEY (`IngredientID`) REFERENCES `ingredients` (`IngredientID`)
);

CREATE TABLE `items` (
  `ItemID` int NOT NULL AUTO_INCREMENT,
  `ItemType` varchar(255) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Price` decimal(10,2) NOT NULL,
  `IsVegetarian` tinyint(1) DEFAULT NULL,
  `IsVegan` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ItemID`)
);

CREATE TABLE `order_items` (
  `OrderItemID` int NOT NULL AUTO_INCREMENT,
  `OrderID` int NOT NULL,
  `ItemTypeID` varchar(50) NOT NULL,
  `ItemID` int NOT NULL,
  `Quantity` int NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`OrderItemID`),
  KEY `OrderID` (`OrderID`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`OrderID`)
);

CREATE TABLE `orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `OrderDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `OrderStatus` varchar(255) NOT NULL,
  `EstimatedDeliveryTime` datetime DEFAULT NULL,
  `TotalPrice` decimal(10,2) NOT NULL,
  `DiscountApplied` tinyint(1) DEFAULT NULL,
  `IsGrouped` tinyint(1) DEFAULT NULL,
  `DeliveryPersonID` int DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `CustomerID` (`CustomerID`),
  KEY `DeliveryPersonID` (`DeliveryPersonID`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`DeliveryPersonID`) REFERENCES `delivery_persons` (`DeliveryPersonID`)
);