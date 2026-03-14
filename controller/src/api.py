import asyncio
import json
import os
import shutil

from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    Form, 
    Header, 
    Query, 
    HTTPException, 
    Depends)
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import Optional, Literal, List, Annotated, Union
from datetime import datetime

## from logger import logger

## from auth import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # make sure this is consistent! Probably should be dynamic/configurable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



################# Pydantic models used to validate incoming HTTP request bodies ##############

class CreateNodeRequest(BaseModel):
    node_type: str
    description: str
    fields: Optional[dict]

class GrantAccessRequest(BaseModel):
    user_id: str

class ConnectNodesRequest(BaseModel):
    start_node_path: str
    target_node_path: str
    relationship_props: Optional[dict] = {'type': 'CONTAINS'}
    bidirectional: Optional[bool] = False

class FunctionRequest(BaseModel):
    input: Union[str, dict, list]
    futures_id: Optional[str] = None
    callback_object: Optional[list] = None
    wait_on: Optional[List[str]] = []


############################### Authentication ##############################################
class User(BaseModel):
    user_id: str
    roles: List[str] = [""]
    # user_root_node: 


async def get_current_user():
    pass





####################################### HTTP ENDPOINTS ######################################

@app.get('/heartbeat')
async def mock_response():
    # logger.info("Received request: GET /heartbeat")
    return {'status': 'ok'}



# ----------- MODEL MANAGEMENT ------------------

@app.post('/create-node/{path:path}')
async def create_new_node():
    """If the user has the correct permissions at the parent node, add a new child AppNode to the parent"""
    pass


@app.post('/connect-nodes/{path:path}')
async def connect_nodes():
    """Create a relationship between a userRoot and an AppNode"""
    pass


@app.post('/grant-access')
async def grant_access():
    """Add a user ID/role OR an Agent role to the list of permitted users/roles to traverse an edge""" 
    pass

@app.post('/find-connection')
async def find_connection():
    """Find the shortest path between a userRoot and an AppNode with the proper permissions"""
    pass

@app.delete('/root/delete-all')
async def clear_graph():
    """Allow an admin user to clear all data from a graph. This is mostly for development/demonstration purposes."""
    pass

@app.delete('/root/{path:path}')
async def delete_node():
    """Delete an AppNode and all of its children (except for children with other AppNodes pointing to it)"""
    pass


@app.get('/by_id')
async def get_invocation_nodes_by_run_id(
    run_id: str = Query(..., description="The run_id to retrieve InvocationNodes for"),
):
    """Get all InvocationNodes (i.e., all Function calls) associated with a particular request/thread. """
    pass


# --------- FUNCTION INVOCATION AND STREAMING ----------
@app.post('/root/{path:path}')
async def run_function():
    """Run a function, either by its relative path or its UID"""
    pass

@app.get('/stream')
async def stream_run_events(
    run_id: str = Query(..., description="The run_id to stream events for"),
):
    """SSE endpoint: streams events pushed when POST /root/{path} completes with this run_id"""
    pass


