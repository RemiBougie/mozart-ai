# /docker
Where .env and docker-compose.yml are defined. At a minimum, docker-compose.yml includes the following service containers:
- Controller : *This is the only publicly exposed endpoint*. The Controller/API service that runs Functions and/or queues Functions in the Redis queue. This is also the service that serves HTML/JavaScript to the client
- Redis : A queue service for Functions that need to be run on behalf of other Functions (e.g., an agent invoking a tool)
- Neo4j : The graph database storing the state of the model
- Tool_Call_Consumer : A consumer script that reads from the Redis queue and forwards requests to the Controller

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
    - `config.json` : field definitions for this AppNode. Includes hard-coded definitions that are constant for all instances of this AppNode (e.g., node type and parent type) and variable definitions needed for node creation (e.g., a first_name field for a Person node, variable definitions dynamically populated into child node descriptions, Agent prompts). This also includes default configuration information for initialization (e.g., including the Agent's role for all appropriate tools)
    - `/functions`
        - `/example-function`
            - `example-function.py` : a Function definition for a single unit of work. Can be any coding language, Python used as an example. 
            - `ExampleFunction.tsx` : a collection of components for viewing/interacting with a Function. Some examples include ExampleFunctionPage (for directly interacting with the function), ExampleFunctionCard (for viewing Function outputs when the Function was invoked as a tool for an autonomous Agent), and ExampleFunctionHITL (for a Human-in-the-Loop interface within a chatbot UI).
            - `config.json` : field definitions for this FunctionNode. Includes hard-coded definitions that are constant for all instances of this FunctionNode (e.g., function name and required input schema). Does NOT include variable definitions for node creation because this is handled automatically by the Controller. 



# EXAMPLE FUNCTIONS NEEDED:
- MCP Example
- HITL Example
- GCP Example
- Local Example
- HTTP Example



# FOOD FOR THOUGHT
- Where would a Terraform script live? How does it find and deploy the functions? Does it even need to be a Terraform script, or just CLI commands?
- How should memory work? Doesn't seem like a good idea to have an infinitely growing context...

- The model-views directory acts as a code repository for the app. Every time pushes are made to this repo:
    - The frontend scripts should be rebuilt and redeployed
    - The controller should update its config for the model
    - Any cloud functions should be redeployed

- For HITL purposes: the LLM responds with a tool call, but instead of the tool call invoking a Function, it sends a HITL message to the client. Instead of having the Controller hang until the client responds, it should save the callback_object and current state to the model. To pick up where it left off, the client sends a POST request to the corresponding Function with the run_id. That way, the Controller knows to associate the POST request with an existing run. Here are a few example scenarios:
    - Scenario: what if the human is simply giving an approval for a tool's response? *Solution*: the tool runs, but in the configuration it has a `"post_invocation_approval": true` field. The Controller sees this flag, forwards the response to the human user for approval. If the human wants to make edits, it can do so in the client, which modifies the tool message that gets forwarded to the LLM. 
    - Scenario: what if the human is simply giving an approval to *run* a tool? *Solution*: when the Agent issues a tool_call, the Controller checks if the `"pre_invocation_approval"` field in the Function config is `true`. If so, the Controller sends a message to the human user for permission to run the Function with the provided inputs. The user can edit the inputs before approval, and the modified inputs will be sent to the Function. If the user denies the request, then the tool response is "Agent was not granted permission to run this tool."
    - Scenario: a user other than the requesting user needs to give approval first. For example, if Person A wants to invoke Person B's personal AI assistant, Person B might want to require manual approval before invocation. *Solution*: idk yet, this is a more complicated use case. Maybe instead of the `"approval_required"` field be a boolean, it could be an array of user IDs/roles corresponding to users who are authorized to give approval. The complication comes from sending notifications to users when their approval is requested...
    - Scenario: an Agent wants human input as a tool result. **Solution**: this is just a `"pre_invocation_approval"` use case with empty fields (or hints or default values). A Function will still need to be written that will simply be a passthrough?
    - How do the above scenarios work with MCP servers? 

    **For now**: Example Function config fields requiring pre- or post-invocation approval:
    "pre_invocation_approval": true     // Controller gets permission to run the Function. If denied, replace the tool result with "Agent was not granted permission to run this tool."
    "post_invocation_approval": true    // Controller gets permission to pass the results of a Function to the Agent. Gives the user an opportunity to edit results. 

    **ADVANCED**: Example Function config fields if other users' permissions are required:
    "pre_invocation_approval": ["user_1"]  
    "post_invocation_approval": ["user_1", "user_2"]
    