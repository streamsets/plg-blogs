create or replace TABLE SALES (
	INVOICEID NUMBER(38,0) NOT NULL,
	STORE VARCHAR(100) NOT NULL,
	DEPARTMENT VARCHAR(100) NOT NULL,
	SSN VARCHAR(100) NOT NULL,
	CUSTOMERNAME VARCHAR(100) NOT NULL,
	GENDER VARCHAR(10) NOT NULL,
	ADDRESS VARCHAR(100) NOT NULL,
	CITY VARCHAR(100) NOT NULL,
	STATE VARCHAR(2) NOT NULL,
	POSTALCODE NUMBER(38,0),
	PAYMENTTYPE VARCHAR(100) NOT NULL,
	CARDNUMBER VARCHAR(100),
	QUANTITY NUMBER(38,0),
	PRODUCTPRICE NUMBER(38,2),
	TOTAL NUMBER(38,2),
	PRODUCT VARCHAR(100) NOT NULL,
	SALEDATE DATE,
	SALETIME TIME(0),
	primary key (INVOICEID)
);