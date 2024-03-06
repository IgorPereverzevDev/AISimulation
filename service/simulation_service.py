import logging

from config.db_connection import fetch_all, insert_update_one, fetch_one
from worker.celery_worker import run_simulation_on_machine

logging.basicConfig(level=logging.INFO)


class SimulationService:

    @staticmethod
    def get_simulation_detail(simulation_id):
        query = "SELECT id, name, machine_id, status, creation_date, update_date " \
                "FROM simulations WHERE id = %s;"
        params = [simulation_id]
        simulation_json = {}
        with fetch_one(query, params) as simulation:
            if simulation:
                simulation_json = {"simulation_id": simulation[0],
                                   "name": simulation[1],
                                   "machine_id": simulation[2],
                                   "status": simulation[3],
                                   "creation_date": simulation[4],
                                   "update_date": simulation[5]}
                logging.info(f"Retrieved simulation record by id: {simulation_id}.")
            return simulation_json

    @staticmethod
    def get_simulations(status=None, order_by="creation_date"):
        query = "SELECT id, name, machine_id, status, creation_date, update_date FROM simulations"
        params = []

        if status:
            query += " WHERE status = %s"
            params.append(status)

        valid_order_columns = ['name', 'creation_date', 'update_date']
        if order_by in valid_order_columns:
            query += f" ORDER BY {order_by}"
        else:
            query += " ORDER BY creation_date"

        with fetch_all(query) as simulations:
            if simulations:
                simulations = [{"simulation_id": item[0],
                                "name": item[1],
                                "machine_id": item[2],
                                "status": item[3],
                                "creation_date": item[4],
                                "update_date": item[5]
                                } for item in simulations]
                logging.info(f"Retrieved simulations: {len(simulations)} records.")
            return simulations or []

    @staticmethod
    def get_machines():
        query = "SELECT id, name FROM machines"
        with fetch_all(query) as machines:
            if machines:
                machines = [{"machine_id": item[0], "name": item[1]} for item in machines]
                logging.info(f"Retrieved machines: {len(machines)} records.")
            return machines or []

    @staticmethod
    def create_simulation(simulation):
        check_query_machines = "SELECT id FROM machines WHERE id = %s;"
        check_params_machines = [simulation.machine.machine_id]

        with fetch_one(check_query_machines, check_params_machines) as result:
            machine_id = result

        if not machine_id:
            machine_query = "INSERT INTO machines (id, name) VALUES (%s, %s);"
            machine_params = [simulation.machine.machine_id, simulation.machine.name]
            insert_update_one(machine_query, machine_params)
            logging.info(f"Inserted missing machine_id: {simulation.machine.machine_id} into machines table.")
        insert_query = "INSERT INTO simulations (id, name, machine_id, status) VALUES (%s, %s, %s, 'pending');"
        insert_params = [simulation.simulation_id, simulation.name, simulation.machine.machine_id]
        insert_update_one(insert_query, insert_params)
        logging.info(f"Inserted simulation_id: {simulation.simulation_id} into simulations table.")

        # run simulation and generate random mock data
        run_simulation_on_machine(simulation.simulation_id)

        query = "SELECT id, status FROM simulations WHERE id = %s;"
        params = [simulation.simulation_id]
        with fetch_one(query, params) as rows:
            if rows:
                logging.info(f"Simulation result for id {rows[0]}: {rows[1]}")
                return {"id": rows[0], "status": rows[1]}
            return None

    @staticmethod
    def get_converge_graph(simulation_id):
        query = "SELECT seconds, loss FROM convergence_data WHERE simulation_id = %s ORDER BY seconds;"
        params = [simulation_id]
        with fetch_all(query, params) as rows:
            if rows:
                logging.info(f"Retrieved convergence data for simulation_id {simulation_id}: {len(rows)} records.")
                graph_data = [{"seconds": row[0], "loss": row[1]} for row in rows]
                return {"data": graph_data}
            return {"data": []}
