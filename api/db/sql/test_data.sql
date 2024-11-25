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