import logging
import math
import os

from celery import Celery
from config.db_connection import insert_update_one
from time import sleep

celery_app = Celery('AISimulation', broker=os.getenv('CELERY_BROKER_URL'))
logging.basicConfig(level=logging.INFO)


@celery_app.task
def run_simulation_on_machine(simulation_id):
    update_simulation_status(simulation_id, 'running')
    try:
        # Simulate real-time data generation
        for i in range(10):
            generate_convergence_data(simulation_id, i)
            sleep(1)  # Consider optimizing this for production use
    except Exception as e:
        logging.error(f"Error during simulation for simulation_id {simulation_id}: {e}")
        update_simulation_status(simulation_id, 'pending')
    else:
        update_simulation_status(simulation_id, 'finished')


def update_simulation_status(simulation_id, status):
    try:
        query = "UPDATE simulations SET status = %s WHERE id = %s"
        params = [status, simulation_id]
        insert_update_one(query, params)
        logging.info(f"Updated simulation status to '{status}' for simulation_id: {simulation_id}.")
    except Exception as e:
        logging.error(f"Failed to update status for simulation_id {simulation_id}: {e}")


def generate_convergence_data(simulation_id, iteration):
    try:
        seconds = 10 + iteration * 10
        alfa = 0.1
        b = 1
        loss = alfa / (math.log(seconds + b))
        loss = max(0, min(loss, 1.0))
        loss = round(loss, 3)
        query = "INSERT INTO convergence_data (simulation_id, seconds, loss) VALUES (%s, %s, %s)"
        params = [simulation_id, seconds, loss]
        insert_update_one(query, params)
        logging.info(f"Generated convergence data for simulation_id: {simulation_id}.")
    except Exception as e:
        logging.error(f"Failed to generate convergence data for simulation_id {simulation_id}: {e}")
