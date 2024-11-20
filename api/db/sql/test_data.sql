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


    