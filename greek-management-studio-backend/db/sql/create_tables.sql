-- Programmer: Connor Warren
-- Class: CS2300
-- For Final Project
-- Tested in PostgreSQL

CREATE TABLE Organization (
    Name            varchar(max),
    Greek_Letters   varchar(max)    NOT NULL,
    Type            varchar(max)    NOT NULL,

    Primary Key (Name)
);

CREATE TABLE School (
    Name                varchar(max),
    Billing_Address     varchar(max)    NOT NULL,

    Primary Key (Name)
);

CREATE TABLE Chapter (
    Name                varchar(max)    NOT NULL,
    Billing_Address     varchar(max)    NOT NULL,
    Org_name            varchar(max),
    School_Name         varchar(max),
    ID                  int,

    FOREIGN KEY (Org_name) REFERENCES Organization (Name),
    FOREIGN KEY (School_Name) REFERENCES School (Name),
    PRIMARY KEY (ID)
);

CREATE TABLE Member (
    Chapter_ID          int,
    Email               varchar(max),
    Fname               varchar(max)    NOT NULL,
    Lname               varchar(max)    NOT NULL,
    DOB                 date            NOT NULL,
    Member_ID           int             NOT NULL,
    Member_Status       varchar(max)    NOT NULL,
    Is_Chapter_Admin    bool            NOT NULL,
    Phone_Num           varchar(max)    NOT NULL,

    Primary Key (Email),
    Foreign Key (Chapter_ID) References Chapter (ID)
);

CREATE TABLE USER (
    Email       varchar(max),
    Password    varchar(max)    NOT NULL,
    Is_Admin    bool            NOT NULL,

    FOREIGN KEY (Email) REFERENCES Member (Email)
);

CREATE TABLE Bill (
    Chapter_ID      int,
    Bill_ID         UUID,
    Amount          float           NOT NULL,
    Amount_Paid     float           NOT NULL,
    Desc            varchar(max)    NOT NULL,
    Due_Date        datetime        NOT NULL,
    Issue_Date      date            NOT NULL,
    Is_External     bool            NOT NULL,

    FOREIGN KEY (Chapter_ID) REFERENCES Chapter (ID),
    PRIMARY KEY (Bill_ID)
);

CREATE TABLE External_Bill (
    Bill_ID             UUID,
    Chapter_Contact     varchar(max)    NOT NULL,
    Payor_Name          varchar(max)    NOT NULL,
    P_Billing_Address   varchar(max)    NOT NULL,
    P_Email             varchar(max)    NOT NULL,
    P_Phone_Num         varchar(max)    NOT NULL,

    FOREIGN KEY (Bill_ID) REFERENCES Bill (Bill_ID)
);

CREATE TABLE Internal_Bill (
    Bill_ID         UUID,
    Member_Email    varchar(max),

    FOREIGN KEY (Bill_ID) REFERENCES Bill (Bill_ID),
    FOREIGN KEY (Member_Email) REFERENCES Member (Email)
);

CREATE TABLE Payment_Info (
    Member_Email    varchar(max),
    Payment_ID      int,
    Nickname        varchar(max)    NOT NULL,

    FOREIGN KEY (Member_Email) REFERENCES Member (Email),
    PRIMARY KEY (Payment_ID)
);

CREATE TABLE Bank_Account (
    Payment_ID      int,
    Account_Num     int,
    Routing_Num     int,

    FOREIGN KEY (Payment_ID) REFERENCES Bill (Payment_ID),
    PRIMARY KEY (Account_Num, Routing_Num)
);

CREATE TABLE Card (
    Payment_ID      int,
    Card_Num        int,
    Security_Code   int         NOT NULL,
    Exp_Date        varchar     NOT NULL,
    Name            varchar     NOT NULL,

    FOREIGN KEY (Payment_ID) REFERENCES Bill (Payment_ID),
    PRIMARY KEY (Card_Num)
);