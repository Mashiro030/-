DROP TABLE IF EXISTS USER_INFO;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS TicketType;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Passenger;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS BoardingPass;
DROP TABLE IF EXISTS Record;
DROP TABLE IF EXISTS FlightLeg;

CREATE TABLE USER_INFO (
	USERNAME string PRIMARY KEY,
   	EMAIL string,
	PASSWORD string,
    PASSPORT string
);

CREATE TABLE User(
	User_id     CHAR(20)     NOT NULL,
	username     VARCHAR(20)     NOT NULL,
	email     VARCHAR(50)     NOT NULL,
	phone     VARCHAR(20)     NOT NULL,
	PRIMARY KEY (User_id)
);

CREATE TABLE Booking(
	book_id     CHAR(20)     NOT NULL,
	fight_id     CHAR(20)     NOT NULL,
	User_id     CHAR(20)     NOT NULL,
	PRIMARY KEY (book_id),
	FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE Class(
	book_id     CHAR(20)     NOT NULL,
	kind     VARCHAR(20)     NOT NULL,
	PRIMARY KEY (book_id, kind),
	FOREIGN KEY (book_id) REFERENCES Booking(book_id)
);

CREATE TABLE TicketType(
	book_id     CHAR(20)     NOT NULL,
	ticket_type     VARCHAR(20)     NOT NULL,
	PRIMARY KEY (book_id, ticket_type),
	FOREIGN KEY (book_id) REFERENCES Booking(book_id)
);

CREATE TABLE Book(
	User_id     CHAR(20)     NOT NULL,
	book_id     CHAR(20)     NOT NULL,
	Book_time     DATETIME     NOT NULL,
	Book_num     CHAR(20)     NOT NULL,
	PRIMARY KEY (User_id, book_id),
	FOREIGN KEY (book_id) REFERENCES Booking(book_id), 
	FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE Passenger(
	Pid     CHAR(20)     NOT NULL,
	p_name     VARCHAR(20)     NOT NULL,
	p_gender     VARCHAR(20)     NOT NULL, 
	p_mail     VARCHAR(20)     NOT NULL,
	p_address     VARCHAR(20),
	p_birthday     DATE,
	Name     VARCHAR(20)     NOT NULL,
	Country     VARCHAR(20)     NOT NULL,
	Number     CHAR(20)     NOT NULL,
	ExpDate     DATE     NOT NULL,
	User_id     CHAR(20)     NOT NULL,
	PRIMARY KEY (Pid),
	FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE Flight(
	flight_number     CHAR(20)     NOT NULL,
	date     DATE    NOT NULL,
	company     VARCHAR(20)     NOT NULL,
	arrival_time     DATETIME     NOT NULL,
	departure_time     DATETIME     NOT NULL,
	User_id     CHAR(20)     NOT NULL,
	PRIMARY KEY (flight_number),
	FOREIGN KEY (User_id) REFERENCES User(User_id)
);

CREATE TABLE BoardingPass(
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

CREATE TABLE Record(
	rid     CHAR(20)     NOT NULL PRIMARY KEY,
	r_date     DATETIME    NOT NULL,
	price     VARCHAR(10)     NOT NULL,
	num      VARCHAR(10)     NOT NULL,
	is_pay     VARCHAR(10)     NOT NULL,
	book_id     CHAR(20),
	FOREIGN KEY (book_id) REFERENCES Booking(book_id)
);


CREATE TABLE FlightLeg(
	ticket_id     CHAR(20)     NOT NULL,
	Leg_Number     CHAR(20)    NOT NULL,
	Leg_start     VARCHAR(20)     NOT NULL,
	Leg_end      VARCHAR(20)     NOT NULL,   
	PRIMARY KEY (ticket_id, Leg_Number),
	FOREIGN KEY (ticket_id) REFERENCES BoardingPass(ticket_id)
);

-- -- insert user
-- INSERT INTO user (name, pic_path)
-- VALUES (
--     ('unregistered', './none.jpg'),
--     ('AA', './none.jpg'),
--     ('CC', './none.jpg'),
--     ('HA', './none.jpg'),
--     ('SL', './none.jpg'),
--     ('YY', './none.jpg'),
--     ('han', './none.jpg'),
--     ('YR', 'YR/YR.jpg'),
-- );