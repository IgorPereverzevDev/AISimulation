-- Create machines table
CREATE TABLE machines
(
    id   INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


-- Create simulations table
CREATE TABLE simulations
(
    id            INTEGER PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    machine_id    INTEGER,
    status        VARCHAR(50)  NOT NULL CHECK (status IN ('pending', 'running', 'finished')),
    creation_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    update_date   TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    FOREIGN KEY (machine_id) REFERENCES machines (id)
);

-- Create convergence_data table
CREATE TABLE convergence_data
(
    id            SERIAL PRIMARY KEY,
    simulation_id INTEGER NOT NULL,
    seconds       INTEGER NOT NULL,
    loss          FLOAT   NOT NULL,
    FOREIGN KEY (simulation_id) REFERENCES simulations (id)
);