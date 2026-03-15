from uuid import uuid4
import json
import jsonschema

class Controller:
    def __init__(self, model_schema: dict, config: dict):
        self.model_schema = model_schema
        self.root_node = self.get_or_create_root_node()


    ###############################################################################################################################
    ########################       HELPER METHODS                  ###############################################################
    ###############################################################################################################################
    
    def get_node_schema(self, node_type):
        """Retrieve JSON schema for a given node type."""
        pass

    def get_rel_schema(self, rel_type):
        """Retrieve JSON schema for a given relationship type."""

    def validate_args(self, args_schema: dict, input_args: dict):
        """Validate the arguments passed to an executor"""
        try:
            jsonschema.validate(instance=input_args, schema=args_schema)
            return
        except json.JSONDecodeError as e:
            # logger.error(f"Error decoding Executor Args Schema: {e}")
            raise json.JSONDecodeError(f"Error parsing Executor Args Schema: {e}")
        except jsonschema.ValidationError as e:
            # logger.error(f"Provided input does not match Excecutor Args Schema: {e}")
            raise jsonschema.ValidationError(f"Invalid input args. Should be {json.dumps(args_schema, indent=2)}")
        except jsonschema.SchemaError as e:
            # logger.error(f"The provided args schema in the executor is invalid: {e}")
            raise jsonschema.SchemaError(f"The provided args schema in the executor is invalid: {e}")

    def loop_check(self, function_node, run_id: str, limit: int = 5):
        """Determine if the FunctionNode has been invoked too many times for the given run."""

        ## Implement later
        return False
    








    #################################################################################################################
    #############   NODE AND RELATIONSHIP MANAGEMENT   ##############################################################
    #################################################################################################################

    def get_or_create_root_node(self):
        """Create the admin application root AppNode if it does not exist. Return the node."""
        pass

    def get_or_create_user_root(self):
        """Create a userRoot for a given user if one doesn't exist yet. Will initially not be connected to any AppNodes in the graph model."
        
        Returns the userRoot node."""
        pass

    async def create_app_node():
        """Add an AppNode to the model as a child of the AppNode specified by explicit path or ID."""
        ################## FIELD VALIDATION
        ## Get AppNode schema for the requested AppNode type
        ## Make sure input fields conform to the schema


        ################## GRAPH TRAVERSAL
        ## Traverse the graph to get the parent AppNode, either by explicit path or ID
            # (if unauthorized, throw an error)


        ################## MODEL VALIDATION
        ## Ensure the requested AppNode has the correct parent type
        ## Ensure there isn't an existing AppNode under the same parent with the same name? <-- I don't think this is necessary anymore because there will be a GUID associated with it


        ################## APP NODE CREATION
        ## Add the requested AppNode to the graph model as well as all Functions associated with the AppNode
        pass

    def give_role_access(self):
        """
        Add the provided entity to a specific allowlist on a relationship, giving the entity access to the target node via its parent node. 
        
        The entity can be specified by user ID, user role, Function ID, or Function role."""
        pass

    def connect_nodes(self):
        """Connect two AppNodes with a relationship. The default relationship is CONTAINS but can be changed."""
        pass

    def delete_node(self):
        """
        Delete a node found at a given path (if authorized) and all children nodes.
        
        Does not delete child nodes that have other AppNodes pointing to it.
        """
        pass

    def delete_all_nodes(self):
        """
        Allows an admin user to delete all nodes (except for the root node) in the graph model. 

        Useful for development or demonstration purposes.
        """
        pass

    def write_invocation_node(self):
        """Store the results of a Function call in an InvocationNode in the model. Its parent can be either a FunctionNode or another InvocationNode.

        If the ID of an existing InvocationNode is given, the previous value will be overwritten. 
        """
        pass







    ###############################################################################################################################
    ###########  GRAPH TRAVERSAL/EXPLORATION  #####################################################################################
    ###############################################################################################################################

    def traverse_graph_by_path(self):
        """Traverse the graph model by the explicit path, checking authorization at every relationship."""
        pass

    def traverse_graph_by_id(self):
        """
        Traverse the graph model by finding the shortest path between the userRoot and FunctionNode with the specified ID, checking authorization at every relationship.
        (This was "get_executor_by_id" in old version)
        """
        pass

    def get_app_node(self):
        """Retrieve a given AppNode, either by explicit path or ID. Optionally retrieve all authorized FunctionNodes associated with this AppNode."""
        pass

    def find_shortest_paths(self):
        """
        Find the shortest path(s) between two nodes on the graph. 

        Low priority.
        """
        pass

    def get_all_child_nodes(self, start_node):
        """Retrieve all nodes underneath the starting node."""

        def get_children(start_node, node_list):
            """Recursively find all children on the node"""
            pass

        pass

    def list_functions(self, parent_node):
        """Get all authorized FunctionNodes hanging off of a parent node."""
        pass

    def get_tools(self, parent_node):
        """Get all authorized AppNodes and FunctionNodes hanging off parent_node"""

        def get_functions_and_children(parent_node, nodes_and_functions: list, node_list):
            """Recursively gather child AppNodes and FunctionNodes, compiling them in to a Set."""
            pass

        pass

    def get_invocation_nodes_by_run_id(self):
        """
        Retrieve all InvocationNodes that have run_id equal to the given run_id.
        InvocationNodes are reachable from Executor nodes the user is authorized to access.
        Returns a list of InvocationNode properties (as dicts) for JSON serialization.
        """
        pass







    ###############################################################################################################################
    ###############################        FUNCTION HANDLING        ###############################################################
    ###############################################################################################################################

    def join_message_lists(self, raw_messages: list):
        """
        Returns a list of all unique messages from the raw_messages list, removing duplicates.
        This is used when multiple Tools are called in parallel, each with a list of messages to send back to the Function that called them.
        """
        pass

    async def run_function_node(
        self,
        futures_id: str = None,
        run_id: str = None
        ):
        """Traverse graph model via URL or ID (if authorized) and run the requested Function"""

        ## futures_id is the ID of the node to be created with this execution
        if futures_id is None:
            futures_id = str(uuid4())

        ## run_id is the ID of the entire flow triggered by the user
        if run_id is None:
            run_id = str(uuid4())


        ################## AUTHORIZATION AND FUNCTION NODE RETRIEVAL
        ## Two ways of getting Executors: Either directly by ID or via explicit path


        ################## INPUT VALIDATION
        ## Validate input arguments against FunctionNode schema


        ################## INFINITE LOOP CHECK
        ## Check to make sure 2+ Functions aren't stuck calling each other in an infinite loop


        ################## HISTORY RETRIEVAL
        ## Get all InvocationNodes relevant to this Function execution. context_id helps distinguish between multiple threads of the same Function


        ################## TOOL RETRIEVAL
        ## Traverse the graph model to find all Functions (Tools) the user and Function roles have permission to use


        ################## CHECK IF THIS FUNCTION IS WAITING ON ANY TOOLS TO FINISH


        ################## FUNCTION CLIENT INSTANTIATION
        ## local
        ## http/https
        ## GCP
        ## Eventually Azure and AWS


        ################## RUN THE FUNCTION


        ################## CALLBACK OBJECT HANDLING AND TOOL CALLING
        ## If the Function has requested a Tool Call, add the Function to the Callback Object and send Tool Messages to the Redis queue for later processing


        ################## MODEL UPDATE
        ## Write results to the graph model
        pass