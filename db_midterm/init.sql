DROP TABLE IF EXISTS USER_INFO;
DROP TABLE IF EXISTS MANAGER;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS RECORD;
DROP TABLE IF EXISTS FLIGHT;
DROP TABLE IF EXISTS BOARDINGPASS;

CREATE TABLE USER_INFO (
    User_id INTEGER PRIMARY KEY,
	USERNAME VARCHAR(30),
   	EMAIL VARCHAR(30),
	PASSWORD VARCHAR(30),
    PASSPORT VARCHAR(30)
);

CREATE TABLE MANAGER (
    User_id INTEGER UNIQUE,
	PERMISSION INTEGER, -- 1 ~ 10, the higher the more permissions
    FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE BOOKING(
	book_id     INTEGER PRIMARY KEY,
	flight_number     CHAR(20)     NOT NULL,
	User_id     INTEGER     NOT NULL,
	p_firstname  CHAR(20),
	p_lastname  CHAR(20),
	country  CHAR(20),
	p_passport  CHAR(20),
	p_class CHAR(20),
	ticket_type CHAR(20),
	gender CHAR(20),
	birthdate DATE,
	expdate DATE,
	FOREIGN KEY (User_id) REFERENCES User(User_id)
	FOREIGN KEY (flight_number) REFERENCES FLIGHT(flight_number)
);

CREATE TABLE RECORD (
	TRANSACTION_TIME DATETIME,
	PID INTEGER,
	SALE_PRICE INTEGER
);

CREATE TABLE FLIGHT(
	flight_number     INTEGER PRIMARY KEY,
	date     DATE,
	company     VARCHAR(20)     NOT NULL,
	arrival_time     DATETIME     NOT NULL,
	departure_time     DATETIME     NOT NULL,
    departure_airport CHAR(20) NOT NULL,
    arrival_airport CHAR(20) NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE BOARDINGPASS(
	ticket_id     INTEGER PRIMARY KEY,
	seat_number     VARCHAR(10)    NOT NULL,
	boarding_gate     VARCHAR(10)     NOT NULL,
	boarding_time     DATETIME     NOT NULL,
	terminal     VARCHAR(20)     NOT NULL,  
	Pid     CHAR(20)     NOT NULL,
	flight_number     INTEGER     NOT NULL,
	FOREIGN KEY (Pid) REFERENCES USER_INFO(User_id),
	FOREIGN KEY (flight_number) REFERENCES Flight(flight_number)
);

-- insert USER_INFO
INSERT INTO USER_INFO (User_id, USERNAME, EMAIL, PASSWORD, PASSPORT)
VALUES
    (1, 'dragon', 'ddd@gmail.com', 'dragon123', 'dragon123'),
    (2, 'dragon_guest', 'ddd2@gmail.com', 'dragon456', 'dragon456'),
	(3, 'guest', 'paravex462@vinopub.com', 'guest', 'guest123');

-- INSERT INTO USER_INFO (User_id, USERNAME, EMAIL, PASSWORD, PASSPORT)
-- VALUES
--     (5, 'guest2', 'harot59152@veb34.com', 'guest123', 'guest123');

INSERT INTO MANAGER (User_id, PERMISSION)
VALUES
    (1, 10);

-- insert FLIGHT
INSERT INTO FLIGHT (
    flight_number, date, company, arrival_time, departure_time,
    departure_airport, arrival_airport, price
)
VALUES
    (1, '2022/01/15', '長榮航空', '2022-01-09 07:35:00', '2022-01-09 10:30:00', '台北 (TPE)', '曼谷 (BKK)', 4000),
    (2, '2022/01/15', '長榮航空', '2022-01-09 07:40:00', '2022-01-09 12:10:00', '台北 (TPE)', '新加坡 (SIN)', 8500),
    (3, '2022/01/15', '中華航空', '2022-01-09 09:00:00', '2022-01-09 09:55:00', '台北 (TPE)', '香港 (HKG)', 3000),
    (4, '2022/01/15', '中華航空', '2022-01-09 10:15:00', '2022-01-09 13:20:00', '台北 (TPE)', '曼谷 (BKK)', 4500),
    (5, '2022/01/15', '長榮航空', '2022-01-09 15:30:00', '2022-01-09 20:00:00', '台北 (TPE)', '新加坡 (SIN)', 8000),
    (6, '2022/01/15', '中華航空', '2022-01-09 18:00:00', '2022-01-09 19:00:00', '台北 (TPE)', '香港 (HKG)', 2000);

-- insert booking
INSERT INTO BOOKING (
    flight_number, User_id, p_firstname, p_lastname, country,
	p_passport, p_class, ticket_type, gender, birthdate, expdate
)
VALUES
    (
		1, 5, 'CHIU', ' CHAO-MIN', 'TW',
		'112345670', 'bussiness_class', 'traval', 'male', '2022-01-03', '2022-01-20'
	);

INSERT INTO BOARDINGPASS (
    seat_number, boarding_gate, boarding_time, terminal, Pid, flight_number
)
VALUES
    (
		'46A', 'D4/19', '2022-01-09 07:40:00', 'T1', 1, 1
	);