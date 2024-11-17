-- Programmer: Connor Warren
-- Class: CS2300
-- For Database Project
-- Tested in PostgreSQL

CREATE TABLE Organization (
    Name            text,
    Greek_Letters   text    NOT NULL,
    Type            text    NOT NULL,

    Primary Key (Name)
);

CREATE TABLE School (
    Name                text,
    Billing_Address     text    NOT NULL,

    Primary Key (Name)
);

CREATE TABLE Chapter (
    Name                text    NOT NULL,
    Billing_Address     text    NOT NULL,
    Org_name            text,
    School_Name         text,
    ID                  int,

    FOREIGN KEY (Org_name) REFERENCES Organization (Name),
    FOREIGN KEY (School_Name) REFERENCES School (Name),
    PRIMARY KEY (ID)
);

CREATE TABLE Member (
    Chapter_ID          int,
    Email               text,
    Fname               text    NOT NULL,
    Lname               text    NOT NULL,
    DOB                 date            NOT NULL,
    Member_ID           int             NOT NULL,
    Member_Status       text    NOT NULL,
    Is_Chapter_Admin    bool            NOT NULL,
    Phone_Num           text    NOT NULL,

    Primary Key (Email),
    Foreign Key (Chapter_ID) References Chapter (ID)
);

CREATE TABLE "user" (
    Email       text,
    Password    text    NOT NULL,
    Is_Admin    bool            NOT NULL,

    FOREIGN KEY (Email) REFERENCES Member (Email)
);

CREATE TABLE Bill (
    Chapter_ID      int,
    Bill_ID         UUID,
    Amount          float           NOT NULL,
    Amount_Paid     float           NOT NULL,
    "desc"            text    NOT NULL,
    Due_Date       	timestamp        NOT NULL,
    Issue_Date      date            NOT NULL,
    Is_External     bool            NOT NULL,

    FOREIGN KEY (Chapter_ID) REFERENCES Chapter (ID),
    PRIMARY KEY (Bill_ID)
);

CREATE TABLE External_Bill (
    Bill_ID             UUID,
    Chapter_Contact     text    NOT NULL,
    Payor_Name          text    NOT NULL,
    P_Billing_Address   text    NOT NULL,
    P_Email             text    NOT NULL,
    P_Phone_Num         text    NOT NULL,

    FOREIGN KEY (Bill_ID) REFERENCES Bill (Bill_ID)
);

CREATE TABLE Internal_Bill (
    Bill_ID         UUID,
    Member_Email    text,

    FOREIGN KEY (Bill_ID) REFERENCES Bill (Bill_ID),
    FOREIGN KEY (Member_Email) REFERENCES Member (Email)
);

CREATE TABLE Payment_Info (
    Member_Email    text,
    Payment_ID      int,
    Nickname        text    NOT NULL,

    FOREIGN KEY (Member_Email) REFERENCES Member (Email),
    PRIMARY KEY (Payment_ID)
);

CREATE TABLE Bank_Account (
    Payment_ID      int,
    Account_Num     int,
    Routing_Num     int,

    FOREIGN KEY (Payment_ID) REFERENCES Payment_Info (Payment_ID),
    PRIMARY KEY (Account_Num, Routing_Num)
);

CREATE TABLE Card (
    Payment_ID      int,
    Card_Num        int,
    Security_Code   int         NOT NULL,
    Exp_Date        varchar     NOT NULL,
    Name            varchar     NOT NULL,

    FOREIGN KEY (Payment_ID) REFERENCES Payment_Info (Payment_ID),
    PRIMARY KEY (Card_Num)
);