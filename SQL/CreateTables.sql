CREATE TABLE `previse`.`teacher` (
  `teacher_id` INT NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `forename` VARCHAR(50) NOT NULL,
  `surname` VARCHAR(50) NOT NULL,
  `year_group` INT NOT NULL,
  PRIMARY KEY (`teacher_id`));

CREATE TABLE `previse`.`student` (
  `student_id` INT NOT NULL,
  `teacher_id` INT NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `forename` VARCHAR(50) NOT NULL,
  `surname` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`student_id`),
  CONSTRAINT `fk_student_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `previse`.`teacher` (`teacher_id`));
  