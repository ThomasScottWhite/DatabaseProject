INSERT INTO Organization (Name, Greek_Letters, Type)
    VALUES ("Lambda Chi Alpha", "LCA", "Social"),
    ("Chi Omega", "XO", "Social"),
    ("Dog Chi Alpha", "DCA", "Professional"),
    ("Cat Omega", "CO", "Professional");

INSERT INTO School (Name, Billing_Address)
    VALUES ("MST", "Rolla, MO"),
    ("SLU", "St. Louis, MO"),
    ("MIZZOU", "California, CA"),
    ("University of Tokyo", "Japan, MO");

INSERT INTO Chapter (Name, Billing_Address, Org_Name, School_Name)
    VALUES ("ADZ", "Rolla, MO", "Lambda Chi Alpha", "MST"),
    ("EK", "Rolla, MO", "Chi Omega", "MST"),
    ("DOG", "St. Louis, MO", "Dog Chi Alpha", "SLU"),
    ("AAZ", "Boston, MA", "Lambda Chi Alpha", "MIZZOU");

INSERT INTO "user" (Email, Password, Is_Admin)
    VALUES ("hank@hankmail.com", "Hark", TRUE),
    ("admin@admin.admin", "admin", FALSE),
    ("dog@dogmail.com", "Bark", FALSE),
    ("cat@catmail.com", "Snark", FALSE),
    ("defaultdan@hotmail.com", "Dan", FALSE),
    ("defaultmam@hotmail.com", "Mam", FALSE),
    ("dude@hotmail.com", "Dude", FALSE),
    ("oatmeal@hotmail.com", "Brother", FALSE),
    ("budgetcostco@hotmail.com", "Good Savings", FALSE),
    ("badhabits@hotmail.com", "Good", FALSE);

INSERT INTO Member (Chapter_ID, Email, Fname, Lname, DOB, Is_Chapter_Admin, Phone_Num)
    VALUES (1, "admin@admin.admin", "Fadmin", "Ladmin", 2000-01-01, True, "555-555-5555");