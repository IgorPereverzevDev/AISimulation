from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, MagicMock

from schemas.models_simulation import Simulation, Machine
from service.simulation_service import SimulationService


class TestSimulationService(TestCase):

    def test_create_simulation(self):
        expected_id = 456
        expected_status = 'running'
        simulation_name = 'Test Simulation'
        machine_id = 123
        simulation = Simulation(
            simulation_id=expected_id,
            name=simulation_name,
            machine_id=machine_id,
            status=expected_status,
            creation_date=datetime.now(),
            update_date=datetime.now(),
            machine=Machine(machine_id=machine_id, name="Machine Name")
        )

        mock_fetch_one = MagicMock()
        mock_fetch_one.__enter__.return_value = (456, 'running')
        mock_fetch_one.__exit__.return_value = (456, 'running')

        with patch('service.simulation_service.fetch_one', return_value=mock_fetch_one), \
                patch('service.simulation_service.insert_update_one') as mock_insert_update_one, \
                patch('service.simulation_service.run_simulation_on_machine') as mock_run_simulation_on_machine:
            mock_insert_update_one.return_value = None
            result = SimulationService.create_simulation(simulation)

            mock_run_simulation_on_machine.assert_called_once_with(simulation.simulation_id)
            assert result == {"id": expected_id, "status": expected_status}

    def test_get_machines(self):
        machines = [[1, 'Machine 1']]
        expected_machine = [{"machine_id": 1, "name": 'Machine 1'}]
        with patch('service.simulation_service.fetch_all') as mock_get_db_connection:
            mock_get_db_connection.return_value.__enter__.return_value = machines
            result = SimulationService.get_machines()
            mock_get_db_connection.assert_called_once_with("SELECT id, name FROM machines")
            assert result == expected_machine

    def test_get_converge_graph(self):
        simulation_id = 1
        mock_data = [
            (10, 0.1),
            (20, 0.2),
            (30, 0.3),
        ]
        expected_graph_data = {
            "data": [
                {"seconds": 10, "loss": 0.1},
                {"seconds": 20, "loss": 0.2},
                {"seconds": 30, "loss": 0.3},
            ]
        }
        with patch('service.simulation_service.fetch_all') as mock_get_db_connection:
            mock_get_db_connection.return_value.__enter__.return_value = mock_data
            result = SimulationService.get_converge_graph(simulation_id)
            query = "SELECT seconds, loss FROM convergence_data WHERE simulation_id = %s ORDER BY seconds;"
            mock_get_db_connection.assert_called_once_with(query, [simulation_id])
            self.assertEqual(result, expected_graph_data)

    def test_get_simulations_pending_status(self):
        simulations = [('1', 'simulation1', '101', 'pending', '2024-03-05T21:16:03.326919',
                        '2024-03-05T21:16:03.326919')]
        with patch('service.simulation_service.fetch_all') as mock_get_db_connection:
            mock_get_db_connection.return_value.__enter__.return_value = simulations
            simulations = SimulationService.get_simulations()
            mock_get_db_connection.assert_called_once_with("SELECT id, name, machine_id, status, "
                                                           "creation_date, update_date "
                                                           "FROM simulations ORDER BY creation_date")
            self.assertEqual(len(simulations), 1)
            self.assertEqual(simulations[0]['simulation_id'], '1')

    def test_get_simulations_no_status(self):
        with patch('service.simulation_service.fetch_all') as mock_get_db:
            SimulationService.get_simulations()
            mock_get_db.assert_called_once_with("SELECT id, name, machine_id, status, creation_date, update_date "
                                                "FROM simulations ORDER BY creation_date")

    def test_get_simulations_with_status(self):
        with patch('service.simulation_service.fetch_all') as mock_get_db:
            SimulationService.get_simulations(status="running")
            mock_get_db.assert_called_once_with("SELECT id, name, machine_id, status, creation_date, update_date "
                                                "FROM simulations WHERE status = %s ORDER BY creation_date")

    def test_get_simulations_order_by(self):
        with patch('service.simulation_service.fetch_all') as mock_get_db:
            SimulationService.get_simulations(order_by="name")
            mock_get_db.assert_called_once_with("SELECT id, name, machine_id, status, creation_date, update_date "
                                                "FROM simulations ORDER BY name")

    def test_get_simulations_order_by_update_date(self):
        with patch('service.simulation_service.fetch_all') as mock_get_db:
            SimulationService.get_simulations(order_by="update_date")
            mock_get_db.assert_called_once_with("SELECT id, name, machine_id, status, creation_date, update_date "
                                                "FROM simulations ORDER BY update_date")

    def test_get_simulations_invalid_order_by(self):
        with patch('service.simulation_service.fetch_all') as mock_get_db:
            SimulationService.get_simulations(order_by="invalid_column")
            mock_get_db.assert_called_once_with(
                "SELECT id, name, machine_id, status, creation_date, update_date "
                "FROM simulations ORDER BY creation_date")

    def test_get_simulation_detail_found(self):
        with patch('service.simulation_service.fetch_one') as mock_get_db:
            mock_get_db.return_value.__enter__.return_value = (
                1, 'Test Simulation', 101, 'finished', '2024-03-06T07:14:11.361426', '2024-03-06T07:14:11.361426')
            simulation_detail = SimulationService.get_simulation_detail(1)
            self.assertEqual(simulation_detail, {
                "simulation_id": 1,
                "name": "Test Simulation",
                "machine_id": 101,
                "status": "finished",
                "creation_date": '2024-03-06T07:14:11.361426',
                "update_date": '2024-03-06T07:14:11.361426'
            })
