-- Programmer: Connor Warren
-- Class: CS2300
-- For Database Project
-- Tested in PostgreSQL

-- Create Organization table
CREATE TABLE Organization (
    Name            text,
    Greek_Letters   text    NOT NULL,
    Type            text    NOT NULL, --FIXME ADD CONSTRAINT

    Primary Key (Name)
);

-- Create School table
CREATE TABLE School (
    Name                text,
    Billing_Address     text    NOT NULL,

    Primary Key (Name)
);

-- Create Chapter table
CREATE TABLE Chapter (
    Name                text    NOT NULL,
    Billing_Address     text    NOT NULL,
    Org_Name            text,
    School_Name         text,
    ID                  serial,

    FOREIGN KEY (Org_Name) REFERENCES Organization (Name) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (School_Name) REFERENCES School (Name) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (ID)
);

-- Create User table
CREATE TABLE "user" (
    Email       text,
    Password    text    NOT NULL,
    Is_Admin    bool    NOT NULL DEFAULT False,

    PRIMARY KEY (Email)
);

-- Create Member table
CREATE TABLE Member (
    Chapter_ID          bigint,
    Email               text    UNIQUE,
    Fname               text    NOT NULL,
    Lname               text    NOT NULL,
    DOB                 date    NOT NULL,
    Member_ID           serial  UNIQUE,
    Member_Status       text, --FIXME ADD CONTRAINT
    Is_Chapter_Admin    bool    NOT NULL DEFAULT False,
    Phone_Num           text    NOT NULL,

    Foreign Key (Email) References "user" (Email) ON DELETE CASCADE,
    Foreign Key (Chapter_ID) References Chapter (ID) ON DELETE CASCADE
);

-- Create Bill table
CREATE TABLE Bill (
    Chapter_ID      bigint,
    Bill_ID         UUID,
    Amount          float           NOT NULL,
    Amount_Paid     float           NOT NULL DEFAULT 0,
    "desc"          text            NOT NULL DEFAULT '',
    Due_Date       	timestamp       NOT NULL,
    Issue_Date      date            NOT NULL DEFAULT CURRENT_DATE,
    Is_External     bool            NOT NULL,

    FOREIGN KEY (Chapter_ID) REFERENCES Chapter (ID) ON DELETE CASCADE,
    PRIMARY KEY (Bill_ID)
);

-- Create External_Bill table
CREATE TABLE External_Bill (
    Bill_ID             UUID,
    Chapter_Contact     text    NOT NULL,
    Payor_Name          text    NOT NULL,
    P_Billing_Address   text    NOT NULL,
    P_Email             text    NOT NULL,
    P_Phone_Num         text    NOT NULL,

    FOREIGN KEY (Bill_ID) REFERENCES Bill (Bill_ID) ON DELETE CASCADE
);

-- Create Internal_Bill table
CREATE TABLE Internal_Bill (
    Bill_ID         UUID,
    Member_Email    text,

    FOREIGN KEY (Bill_ID) REFERENCES Bill (Bill_ID) ON DELETE CASCADE,
    FOREIGN KEY (Member_Email) REFERENCES Member (Email) ON DELETE CASCADE
);

-- Create Payment_Info table
CREATE TABLE Payment_Info (
    Member_Email    text        NOT NULL,
    Payment_ID      serial,
    Nickname        text,

    FOREIGN KEY (Member_Email) REFERENCES Member (Email) ON DELETE CASCADE,
    PRIMARY KEY (Payment_ID)
);

-- Create BankAccount table
CREATE TABLE Bank_Account (
    Payment_ID      int         NOT NULL,
    Account_Num     int,
    Routing_Num     int,

    FOREIGN KEY (Payment_ID) REFERENCES Payment_Info (Payment_ID) ON DELETE CASCADE,
    PRIMARY KEY (Account_Num, Routing_Num)
);

-- Create Card table
CREATE TABLE Card (
    Payment_ID      int         NOT NULL,
    Card_Num        int,
    Security_Code   int         NOT NULL,
    Exp_Date        varchar     NOT NULL,
    Name            varchar     NOT NULL,

    FOREIGN KEY (Payment_ID) REFERENCES Payment_Info (Payment_ID) ON DELETE CASCADE,
    PRIMARY KEY (Card_Num)
);


INSERT INTO Organization (Name, Greek_Letters, Type)
    VALUES ('Lambda Chi Alpha', 'LCA', 'Social'),
    ('Chi Omega', 'XO', 'Social'),
    ('Dog Chi Alpha', 'DCA', 'Professional'),
    ('Cat Omega', 'CO', 'Professional');

INSERT INTO School (Name, Billing_Address)
    VALUES ('MST', 'Rolla, MO'),
    ('SLU', 'St. Louis, MO'),
    ('MIZZOU', 'California, CA'),
    ('University of Tokyo', 'Japan, MO');

INSERT INTO Chapter (Name, Billing_Address, Org_Name, School_Name)
    VALUES ('ADZ', 'Rolla, MO', 'Lambda Chi Alpha', 'MST'),
    ('EK', 'Rolla, MO', 'Chi Omega', 'MST'),
    ('DOG', 'St. Louis, MO', 'Dog Chi Alpha', 'SLU'),
    ('AAZ', 'Boston, MA', 'Lambda Chi Alpha', 'MIZZOU');

INSERT INTO "user" (Email, Password, Is_Admin)
    VALUES ('hank@hankmail.com', 'Hark', TRUE),
    ('admin@admin.admin', 'admin', FALSE),
    ('dog@dogmail.com', 'Bark', FALSE),
    ('cat@catmail.com', 'Snark', FALSE),
    ('defaultdan@hotmail.com', 'Dan', FALSE),
    ('defaultmam@hotmail.com', 'Mam', FALSE),
    ('dude@hotmail.com', 'Dude', FALSE),
    ('oatmeal@hotmail.com', 'Brother', FALSE),
    ('budgetcostco@hotmail.com', 'Good Savings', FALSE),
    ('badhabits@hotmail.com', 'Good', FALSE);

INSERT INTO Member (Chapter_ID, Email, Fname, Lname, DOB, Is_Chapter_Admin, Member_Status, Phone_Num)
    VALUES (1, 'admin@admin.admin', 'admin', 'Ladmin', '2000-01-01', TRUE,'FIXME', '555-555-5555'),
    (1, 'dog@dogmail.com', 'dog', 'doggy', '2000-01-01', FALSE, 'FIXME', '777-777-7777'),
    (1, 'cat@catmail.com', 'cat', 'kitty', '2000-01-01', FALSE, 'FIXME', '888-888-8888'),
    (1, 'defaultdan@hotmail.com', 'default', 'dan', '2000-01-01', FALSE, 'FIXME', '888-888-8888'),
    (2, 'defaultmam@hotmail.com', 'default', 'mam', '2000-01-01', TRUE, 'FIXME', '888-888-8888'),
    (2, 'dude@hotmail.com', 'dude', 'ultradude', '2000-01-01', FALSE, 'FIXME', '888-888-8888'),
    (2, 'oatmeal@hotmail.com', 'oat', 'meal', '2000-01-01', FALSE, 'FIXME', '888-888-8888'),
    (2, 'budgetcostco@hotmail.com', 'cost', 'costco', '2000-01-01', FALSE, 'FIXME', '888-888-8888'),
    (3, 'badhabits@hotmail.com', 'bad', 'babits', '2000-01-01', TRUE, 'FIXME', '888-888-8888');


INSERT INTO Bill (Chapter_ID, Bill_ID, Amount, Amount_Paid, "desc", Due_Date, Issue_Date, Is_External)
    VALUES (1, '2990e7d7-281f-4716-9609-6848ebcdecaf', 10, 0, 'No description', '2024-01-02 00:00:00', '2024-01-01', FALSE),
    (1, '20ddc4ad-da2b-4cd4-9e87-05d15890c466', 10, 0, 'No description', '2024-01-02 00:00:00', '2024-01-01', TRUE);

--No member paying?
INSERT INTO External_Bill (Bill_ID, Chapter_Contact, Payor_Name, P_Billing_Address, P_Email, P_Phone_Num)
    VALUES ('20ddc4ad-da2b-4cd4-9e87-05d15890c466', 'FIXME', 'FIXME', 'FIXME', 'fix@me.com', 'FIX-ME1-2345');

INSERT INTO Internal_Bill (Bill_ID, Member_Email)
    VALUES ('2990e7d7-281f-4716-9609-6848ebcdecaf', 'dog@dogmail.com');

--Make payment ID serial?
INSERT INTO Payment_Info (Member_Email, Nickname)
    VALUES ('dog@dogmail.com', 'Dogpal'),
    ('cat@catmail.com', 'catpal');

INSERT INTO Bank_Account (Payment_ID, Account_Num, Routing_Num)
    VALUES (1, 123456789, 987654321);    

--Exp_Date should have constraint maybe?
INSERT INTO Card (Payment_ID, Card_Num, Security_Code, Exp_Date, Name)
    VALUES (2, 13579, 024, 07-27, 'mastercat');