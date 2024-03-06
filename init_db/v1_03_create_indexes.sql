CREATE INDEX CONCURRENTLY idx_simulations_status ON simulations (status);
CREATE INDEX CONCURRENTLY idx_simulations_creation_date ON simulations (creation_date);
CREATE INDEX CONCURRENTLY idx_simulations_update_date ON simulations (update_date);
CREATE INDEX CONCURRENTLY idx_convergence_data_simulation_id ON convergence_data (simulation_id);
