import uvicorn
from fastapi import FastAPI, Query, HTTPException, Path
from service.simulation_service import SimulationService
from schemas.models_simulation import Simulation, SimulationStatus

app = FastAPI()


@app.get("/simulations")
async def get_simulations(status: SimulationStatus = None,
                          order_by: str = Query("creation_date", pattern="^(name|creation_date|update_date)$")):
    try:
        return SimulationService.get_simulations(status=status, order_by=order_by)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/simulations/{simulation_id}")
async def get_simulation_detail(simulation_id: int =
                                Path(..., description="The ID of the simulation to retrieve details for")):
    simulation_detail = SimulationService.get_simulation_detail(simulation_id)
    if simulation_detail:
        return simulation_detail
    else:
        raise HTTPException(status_code=404, detail="Simulation not found")


@app.get("/machines")
async def get_machines():
    try:
        return SimulationService.get_machines()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulation")
async def create_simulation_endpoint(simulation: Simulation):
    try:
        return SimulationService.create_simulation(simulation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/converge/{simulation_id}")
async def get_converge_graph(simulation_id: int):
    try:
        graph_data = SimulationService.get_converge_graph(simulation_id)
        if not graph_data['data']:
            raise HTTPException(status_code=404, detail="Simulation not found or no convergence data available")
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
