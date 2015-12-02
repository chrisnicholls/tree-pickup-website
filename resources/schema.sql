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