# /src/api/traffic_control.py, create API endpoints that allow traffic operators to issue commands manually. 
# These endpoints integrate with the feedback manager to adjust traffic devices on demand.

from fastapi import APIRouter, HTTPException
from feedback.feedback_manager import handle_feedback_action

router = APIRouter()

@router.post("/control/traffic_light")
async def manual_traffic_light_control(light_id: str, action: str):
    try:
        handle_feedback_action("traffic_light", light_id=light_id, action=action)
        return {"status": "success", "message": f"Traffic light {light_id} set to {action}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/control/reroute")
async def manual_reroute(vehicle_id: str, new_route: str):
    try:
        handle_feedback_action("reroute", vehicle_id=vehicle_id, new_route=new_route)
        return {"status": "success", "message": f"Vehicle {vehicle_id} rerouted to {new_route}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/control/emergency_clearance")
async def emergency_clearance(affected_lights: list):
    try:
        handle_feedback_action("emergency", affected_lights=affected_lights)
        return {"status": "success", "message": "Emergency clearance activated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
