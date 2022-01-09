DROP TABLE IF EXISTS USER_INFO;
DROP TABLE IF EXISTS MANAGER;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS FLIGHT;
DROP TABLE IF EXISTS BORADINGPASS;

CREATE TABLE USER_INFO (
    User_id INTEGER UNIQUE NOT NULL,
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
	flight_number     INTEGER   UNIQUE NOT NULL,
	date     DATE    NOT NULL,
	company     VARCHAR(20)     NOT NULL,
	arrival_time     DATETIME     NOT NULL,
	departure_time     DATETIME     NOT NULL,
    departure_airport CHAR(20) NOT NULL,
    arrival_airport CHAR(20) NOT NULL,
    price INTEGER NOT NULL,
	PRIMARY KEY (flight_number)
);

CREATE TABLE BORADINGPASS(
	ticket_id     INTEGER     UNIQUE NOT NULL,
	seat_number     VARCHAR(10)    NOT NULL,
	boarding_gate     VARCHAR(10)     NOT NULL,
	boarding_time     DATETIME     NOT NULL,
	terminal     VARCHAR(20)     NOT NULL,  
	Pid     CHAR(20)     NOT NULL,
	p_name     VARCHAR(20)     NOT NULL, 
	flight_number     INTEGER     NOT NULL,
	PRIMARY KEY (ticket_id),
	FOREIGN KEY (Pid) REFERENCES USER_INFO(User_id),
	FOREIGN KEY (flight_number) REFERENCES Flight(flight_number)
);

-- insert USER_INFO
INSERT INTO USER_INFO (User_id, USERNAME, EMAIL, PASSWORD, PASSPORT)
VALUES
    (1, 'dragon', 'ddd@gmail.com', 'dragon123', 'dragon123'),
    (2, 'dragon_guest', 'ddd2@gmail.com', 'dragon456', 'dragon456');

INSERT INTO MANAGER (User_id, PERMISSION)
VALUES
    (1, 10);

-- insert FLIGHT
INSERT INTO FLIGHT (
    flight_number, date, company, arrival_time, departure_time,
    departure_airport, arrival_airport, price
)
VALUES
    (1, '2022/01/15', '長榮航空', '2022-01-09 07:35:00', '2022-01-09 10:30:00', '台北 (TPE)', '曼谷 (BKK)', 2000),
    (2, '2022/01/15', '長榮航空', '2022-01-09 07:40:00', '2022-01-09 12:10:00', '台北 (TPE)', '新加坡 (SIN)', 4000),
    (3, '2022/01/15', '中華航空', '2022-01-09 08:00:00', '2022-01-09 09:55:00', '台北 (TPE)', '香港 (HKG)', 3000);