# /docker
Where .env and docker-compose.yml are defined. At a minimum, docker-compose.yml includes the following service containers:
- Controller : the Controller/API service that runs Functions and/or queues Functions in the Redis queue. This is also the service that serves HTML/JavaScript to the client
- Redis : a queue service for Functions that need to be run on behalf of other Functions (e.g., an agent invoking a tool)
- Neo4j : the graph database storing the state of the model
- Tool_Call_Consumer : a consumer script that reads from the Redis queue and forwards requests to the Controller

Other database containers can be added to the docker-compose.yml if local solutions are needed (e.g., CouchDB, Elasticsearch, MCP servers, etc.)

# /controller
The Controller manages authentication, client streaming, logging, tool calling, and controls the model. 
- `api.py` : a FastAPI application that creates new AppNodes, creates new relationships, manages users, handles GET/POST/PUT/DELETE requests to FunctionNodes, etc.
- `auth.py` : handles user authentication
- `clients.py` : several Client Object definitions for invoking Functions in different locations. Functions may be executed locally, in the cloud, or on a separate hosted server. 
- `controller.py` : the object that controls the model by executing Cypher queries and handles tool calling in the Redis queue. 
- `logger.py` : logs interactions in the Controller. ERROR, WARNING, DEBUG, INFO.
- `run_stream.py` : handles streaming to the client. Used mostly with autonomous agent flows invoking multiple Functions as tools. 

# /model-views
## /common
Node and relationship definitions used throughout the model that are not application specific
- `/nodes` : definitions for utility nodes
    - `function.json` : schema definition for fields needed in a Function node
    - `invocation.json` : schema definition for an Invocation of a Function node (this might need to be defined at the function level because each Function might produce a different output schema?)
    - `userRoot.json` : schema definition for a userRoot node. i.e., where a particular user can begin their graph traversal. For example, Admin users have their UserRoot point to the application Root node. 
- `/relationships` : definitions for relationships
    - `CONTAINS.json` : schema definition for a CONTAINS relationship between two AppNodes.
    - `HAS_FUNCTION.json` : schema definition for a HAS_FUNCTION relationship between an AppNode and a child FunctionNode. 

## /app
Node, relationship, functions, and view definitions that are application specific. A generic example is shown below:
- `/example-node`
    - `ExampleNode.tsx` : the general layout for this AppNode, where views for child Functions are rendered as child components within this layout. 
    - `config.json` : field definitions for this AppNode. Includes hard-coded definitions that are constant for all instances of this AppNode (e.g., node type and parent type) and variable definitions needed for node creation (e.g., a first_name field for a Person node, variable definitions dynamically populated into child node descriptions, Agent prompts)
    - `/functions`
        - `/example-function`
            - `example-function.py` : a Function definition for a single unit of work. Can be any coding language, Python used as an example. 
            - `ExampleFunction.tsx` : a collection of components for viewing/interacting with a Function. Some examples include ExampleFunctionPage (for directly interacting with the function), ExampleFunctionCard (for viewing Function outputs when the Function was invoked as a tool for an autonomous Agent), and ExampleFunctionHITL (for a Human-in-the-Loop interface within a chatbot UI).
            - `config.json` : field definitions for this FunctionNode. Includes hard-coded definitions that are constant for all instances of this FunctionNode (e.g., function name and required input schema). Does NOT include variable definitions for node creation because this is handled automatically by the Controller. 



# 

## EXAMPLES NEEDED:
- MCP Example
- HITL Example
- GCP Example
- Local Example
- HTTP Example



## FOOD FOR THOUGHT
- Where would a Terraform script live? How does it find and deploy the functions? Does it even need to be a Terraform script, or just CLI commands?