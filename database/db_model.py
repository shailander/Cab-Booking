RECORD_TABLE = """

CREATE TABLE IF NOT EXISTS Admin(
    id INTEGER DEFAULT 1,
    active INTEGER DEFAULT 1,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    email_id STRING NOT NULL
    );

CREATE TABLE IF NOT EXISTS cab_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cab_number TEXT NOT NULL,
    seat_capacity INTEGER NOT NULL,
    seat_available INTEGER,
    route TEXT NOT NULL,
    timing TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employee_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS travel_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INT NOT NULL,
    cab_id INT NOT NULL,
    trip_date STRING NOT NULL,
    source STRING NOT NULL,
    destination STRING NOT NULL,
    timing STRING NOT NULL,
    status STRING NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES employee_details(id),
    FOREIGN KEY(cab_id) REFERENCES cab_details(id)
);

CREATE TABLE IF NOT EXISTS trip_time(
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    time INTEGER NOT NULL
    );

"""