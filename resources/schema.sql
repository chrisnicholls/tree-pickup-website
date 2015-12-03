DROP TABLE IF EXISTS `scouts`.`PickupRecord` ;

CREATE TABLE IF NOT EXISTS `scouts`.`PickupRecord` (
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
  PRIMARY KEY (`pickupRecordId`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `scouts`.`PickupDate` ;

CREATE TABLE IF NOT EXISTS `scouts`.`PickupDate` (
  `pickupDateId` INT NOT NULL AUTO_INCREMENT,
  `pickupDate` VARCHAR(20) NOT NULL,
  `openTime` DATETIME NOT NULL,
  `closeTime` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`pickupDateId`))
ENGINE = InnoDB;

INSERT INTO `PickupDate` (`pickupDateId`,`pickupDate`,`openTime`,`closeTime`) VALUES (1,'January 2, 2016',NOW(),'2016-01-01 22:00:00');
INSERT INTO `PickupDate` (`pickupDateId`,`pickupDate`,`openTime`,`closeTime`) VALUES (2,'January 9, 2016',NOW(),'2016-01-09 22:00:00');