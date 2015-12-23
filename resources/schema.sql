DROP TABLE IF EXISTS `PickupRecord` ;

CREATE TABLE IF NOT EXISTS `PickupRecord` (
  `pickupRecordId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `emailAddress` VARCHAR(45) NULL,
  `streetNumber` VARCHAR(45) NOT NULL,
  `streetName` VARCHAR(45) NOT NULL,
  `neighbourhood` VARCHAR(45) NULL,
  `phoneNumber` VARCHAR(15) NULL,
  `pickupDate` VARCHAR(20) NOT NULL,
  `moneyLocation` VARCHAR(45) NOT NULL,
  `otherInstructions` VARCHAR(100) NULL,
  `dateSubmitted` VARCHAR(45) NOT NULL,
  `source` VARCHAR(32) NOT NULL DEFAULT 'web',
  PRIMARY KEY (`pickupRecordId`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `PickupDate` ;

CREATE TABLE IF NOT EXISTS `PickupDate` (
  `pickupDateId` INT NOT NULL AUTO_INCREMENT,
  `pickupDate` VARCHAR(20) NOT NULL,
  `openTime` DATETIME NOT NULL,
  `closeTime` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`pickupDateId`))
ENGINE = InnoDB;

INSERT INTO `PickupDate` (`pickupDateId`,`pickupDate`,`openTime`,`closeTime`) VALUES (1,'January 2, 2016',NOW(),'2016-01-01 22:00:00');
INSERT INTO `PickupDate` (`pickupDateId`,`pickupDate`,`openTime`,`closeTime`) VALUES (2,'January 9, 2016',NOW(),'2016-01-09 22:00:00');

DROP TABLE IF EXISTS `User`;

CREATE TABLE IF NOT EXISTS `User` (
  `userId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `emailAddress` VARCHAR(30) NOT NULL,
  `password` VARCHAR(1024) NOT NULL,
  PRIMARY KEY (`userId`))
ENGINE = InnoDB;
