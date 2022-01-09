DROP TABLE IF EXISTS USER_INFO;
DROP TABLE IF EXISTS MANAGER;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS FLIGHT;
DROP TABLE IF EXISTS BORADINGPASS;

CREATE TABLE USER_INFO (
    User_id INTEGER UNIQUE,
	USERNAME string PRIMARY KEY,
   	EMAIL string,
	PASSWORD string,
    PASSPORT string
);

CREATE TABLE MANAGER (
    User_id INTEGER UNIQUE,
	PERMISSION INTEGER, -- 1 ~ 10, the higher the more permissions
    FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE BOOKING(
	book_id     CHAR(20)     NOT NULL,
	fight_id     CHAR(20)     NOT NULL,
	User_id     INTEGER     NOT NULL,
	PRIMARY KEY (book_id),
	FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE FLIGHT(
	flight_number     CHAR(20)     NOT NULL,
	date     DATE    NOT NULL,
	company     VARCHAR(20)     NOT NULL,
	arrival_time     DATETIME     NOT NULL,
	departure_time     DATETIME     NOT NULL,
	User_id     INTEGER     NOT NULL,
	PRIMARY KEY (flight_number),
	FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE BORADINGPASS(
	ticket_id     CHAR(20)     NOT NULL,
	seat_number     VARCHAR(10)    NOT NULL,
	boarding_gate     VARCHAR(10)     NOT NULL,
	boarding_time     DATETIME     NOT NULL,
	terminal     VARCHAR(20)     NOT NULL,  
	Pid     CHAR(20)     NOT NULL,    
	p_name     VARCHAR(20)     NOT NULL, 
	flight_number     CHAR(20)     NOT NULL,
	PRIMARY KEY (ticket_id),
	FOREIGN KEY (Pid) REFERENCES Passenger(Pid),
	FOREIGN KEY (flight_number) REFERENCES Flight(flight_number)
);

-- insert user
INSERT INTO USER_INFO (User_id, USERNAME, EMAIL, PASSWORD, PASSPORT)
VALUES
    (1, 'dragon', 'ddd@gmail.com', 'dragon123', 'dragon123'),
    (2, 'dragon_guest', 'ddd2@gmail.com', 'dragon456', 'dragon456');

INSERT INTO MANAGER (User_id, PERMISSION)
VALUES
    (1, 10);