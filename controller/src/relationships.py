class Relationship:
    rel_type: str
    rel_props: dict = {}
    id_fields: dict = {} # I honestly don't rememebr what this is for

    def __init__(self, start_node, rel_schema):
        ## the rel_props variable is flexible, will be saved as attribute
        """rel_props argument must one of the 3 following formats:
        1. [{'rel_props': {'type': 'value', 'id': 'asdf-1234...'}, ...}]
        2. {'rel_props': {'type': 'value', 'id': 'asdf-1234...'}, ...}
        3. {'type': 'value', 'id': 'asdf-1234...'}
        """

        ##### READ INPUT PROPERTIES


        ##### GENERATE TYPE STRING FOR CYPHER QUERIES


        ##### VALIDATE INPUT PROPERTIES
        pass


    def authorize(self, action: str, current_user) -> bool:
        """Determines if a user is authorized to traverse this Relationship according to their user ID/role and the action they are attempting to perform."""
        ## When developing, set action="test" to get denied access to a node
        if action.lower() == "test":
            return False
        
        ## Admins have access to all nodes
        if 'admin' in current_user.roles:
            return True 
        
        ## Verify user contains role for a given action on a node <-- ultimately this can be done server-side in Neo4j
        if action in self.rel_props.keys():
            allowed_roles = self.rel_props[action]
            if '*' in allowed_roles:
                return True
            
            user_roles = current_user.roles
            for role in user_roles:
                if role in allowed_roles:
                    return True

        ## There may be more advanced authorization logic to come
        
        return False 