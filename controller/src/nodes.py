class Node:
    id: str = ""
    name: str = ""
    fields: dict = {}
    labels: list = ["AppNode"]
    label_string: str ## used when generating Cypher queries

    def __init__(self, fields, node_schema = None, labels: list = ["AppNode"]):
        """
        Fields argument must one of the 3 following formats:
        1. [{'n': {'name': 'value', 'id': 'asdf-1234...'}, ...}]    // list containing a single object with an 'n' key
        2. {'n': {'name': 'value', 'id': 'asdf-1234...'}, ...}      // an object with an 'n' key
        3. {'name': 'value', 'id': 'asdf-1234...'}                  // an object with 'name' and 'id' keys
        """

        ##### READ INPUT FIELDS
        if type(fields) == list:
            # if input fields is a list of length 1
            # e.g., [{'n': {'name': 'name'}}]
            self.fields = fields[0]['n']
        elif type(fields) == dict and 'n' in fields.keys():
            # if input fields is a dictionary with variable name
            # e.g., {'n': {'name', 'name'}}
            self.fields = fields['n']
        elif type(fields) == dict and ('name' in fields.keys() or 'id' in fields.keys()):
            # if input fields is a dictionary without variable name
            # e.g., {'name': 'name'}
            self.fields = fields
        else:
            raise ValueError(f"Provided fields don't work: {fields}. The data type provided is {type(fields)}. Make sure the key for node fields is 'n'")

        ##### GENERATE LABEL STRING USED FOR WRITING CYPHER QUERIES
        self.labels = labels
        escaped_labels = [f"`{label}`" for label in labels]
        joined_labels = "&".join(escaped_labels)
        self.labels=f"{joined_labels}"


        ##### VALIDATE INPUT FIELDS
        if 'name' in self.fields:
            self.name = self.fields['name']
        if 'id' in self.fields:
            self.id = self.fields['id']

        if 'id' not in self.fields and 'name' not in self.fields:
            raise KeyError("Node must have id or name field.")

        if node_schema is not None:
            # enforce schema fields based on the label(s)
            pass



class AppNode:
    def __init__(self, fields, node_schema=None):
        ## TBH I don't think this is really necessary, it just might be helpful to distinguish between AppNodes, FunctionNodes, and InvocationNodes in the code.
        pass

class FunctionNode:
    def __init__(self, fields, node_schema=None):
        ## TBH I don't think this is really necessary, it just might be helpful to distinguish between AppNodes, FunctionNodes, and InvocationNodes in the code.
        pass
    
class InvocationNode:
    def __init__(self, fields, node_schema=None):
        ## TBH I don't think this is really necessary, it just might be helpful to distinguish between AppNodes, FunctionNodes, and InvocationNodes in the code.
        pass