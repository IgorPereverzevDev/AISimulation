# AISimulation Service Documentation

Welcome to the AISimulation service documentation! This service is meticulously crafted to meet the specifications outlined in the task and offers a suite of four API endpoints that enable interaction with our simulation and machine data.

## API Endpoints

### List Simulations
- **Endpoint:** `GET /simulations`
- **Description:** Returns a list of simulation runs, allowing for sorting by `name`, `creation_date`, or `update_date`, with `creation_date` being the default sort order.
```
http://localhost:8000/simulations?order_by=update_date
Response
[
    {
        "simulation_id": 1,
        "name": "A",
        "machine_id": 102,
        "status": "finished",
        "creation_date": "2024-03-06T08:02:46.295055",
        "update_date": "2024-03-06T08:02:46.295055"
    }
]

```
### One Simulation
- **Endpoint:** `GET /simulation/{simulation_id}`
- **Description:** The ID of the simulation to retrieve details for.
```
http://localhost:8000/simulation/1

Response

{
    "simulation_id": 1,
    "name": "A",
    "machine_id": 102,
    "status": "finished",
    "creation_date": "2024-03-06T08:02:46.295055",
    "update_date": "2024-03-06T08:02:46.295055"
}
```

### List Machines
- **Endpoint:** `GET /machines`
- **Description:** Retrieves a list of machines on which simulations are running. It's possible for simulations to be executed on different machines.
```
http://localhost:8000/machines
Response
[
    {
        "machine_id": 102,
        "name": "Machine A"
    }
]
```
### Create Simulation
- **Endpoint:** `POST /simulation`
- **Description:** Allows the creation of a new simulation. Below is an example JSON request and response:
```
POST http://localhost:8000/simulation
{
  "simulation_id": 1,
  "name": "Sample Simulation",
  "machine_id": 101,
  "status": "pending",
  "creation_date": "2024-03-05T14:30:00",
  "update_date": "2024-03-05T15:00:00",
  "machine": {
    "machine_id": 101,
    "name": "Machine A"
  }
}
Response
{
    "id": 1,
    "status": "finished"
}
``` 

### Get Convergence Data
- **Endpoint:** `GET /converge/{simulation_id}`
- **Description:** Returns convergence data for a specific simulation by seconds and loss in the format specified in the task. Data is retrieved on a logarithmic scale.
```
http://localhost:8000/converge/1
Response
{
    "data": [
        {
            "seconds": 10,
            "loss": 0.042
        },
        {
            "seconds": 20,
            "loss": 0.033
        },
        {
            "seconds": 30,
            "loss": 0.029
        },
        {
            "seconds": 40,
            "loss": 0.027
        },
        {
            "seconds": 50,
            "loss": 0.025
        },
        {
            "seconds": 60,
            "loss": 0.024
        },
        {
            "seconds": 70,
            "loss": 0.023
        },
        {
            "seconds": 80,
            "loss": 0.023
        },
        {
            "seconds": 90,
            "loss": 0.022
        },
        {
            "seconds": 100,
            "loss": 0.022
        }
    ]
}
```

## Docker and Worker Implementation

The service is accompanied by a Docker file and Docker compose for launching the Web, Postgres, Redis, and Celery framework, ensuring ease of setup and execution.

# How It Works

Upon creating a simulation, the task is placed in a queue and in the database with a "pending" status. Subsequently, a worker picks up the task from the queue, changes its status to "running," and begins generating real-time emulation data for loss and seconds (for example it takes about 10s). Upon successful completion of the emulation, the worker records the data in the database and updates the simulation's status to "finished".

# Deployment and Running

To successfully deploy and run the AISimulation service, you will need to have Docker and Python 3.9 installed on your computer. All necessary dependencies are listed in the `requirements.txt` file.

To start the containers, run the following command from the root of the project:

```
docker-compose up --build
```

After launching, you can use Postman to create a simulation with a request to:
```
POST http://localhost:8000/simulation
{
  "simulation_id": 1,
  "name": "Sample Simulation",
  "machine_id": 101,
  "status": "pending",
  "creation_date": "2024-03-05T14:30:00",
  "update_date": "2024-03-05T15:00:00",
  "machine": {
    "machine_id": 101,
    "name": "Machine A"
  }
}
```
# Testing

To run unit tests, use the following command from the root of the project:

```
python -m unittest
```

# Areas for Improvement

## Architectural Improvements:

The API includes the keyword async, but in reality, this does not provide asynchronous computations because other parts of the service are written synchronously. To address this, we can make the code asynchronous in case the number of users increases.
Additional workers are needed to process the queue. RabbitMQ, which is also available in Celery, could be utilized for this purpose.

## Functional Improvements:

Currently, there is the capability to run a single application on two machines, meaning each application is launched with unique machine IDs. However, there is no ability to run the application on another machine that has been previously registered in the database with a unique ID. We can add the ability to process different simulations on different machines by making modifications to the code and synchronizing with the database.
Locks when selecting statuses: Frequent updates to simulation statuses in your application can lead to locks. Consider using optimistic locking for managing concurrent updates or implement retry logic to handle exceptions due to locks.

Handling stuck/failed tasks: For task queues (e.g., with Celery), it's crucial to have mechanisms to detect and recover tasks that haven't completed successfully. 

Approaches include:

Heartbeat mechanisms: Regular "I'm alive" signals from tasks to identify stuck tasks.
Execution timeouts: Setting a maximum execution time after which a task is considered failed.
Retries: Automatically restarting a task if it fails.
Monitoring and alerts: Setting up monitoring systems to notify about a high number of failed or stuck tasks.

## Non-Functional Improvements:
We need to add validation for each request.

More unit tests and integration tests are needed to ensure reliability and robustness.

Error handling across different business scenarios should be enhanced to improve resilience.

Additional logging throughout the code would aid in debugging and monitoring.

Metrics for call volume and service load should be introduced for better observability.

Security policies for different APIs should be implemented to protect sensitive data and functionalities.

Implementing these improvements will enhance the architecture, functionality, and non-functional aspects of the AISimulation service, making it more scalable, reliable, and secure.

All API descriptions can be found in Swagger, documenting all requests and responses. Additionally, tokens required for API calls must be specified.