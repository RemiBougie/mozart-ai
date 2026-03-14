import redis
import time
import requests
import json

r = redis.Redis(host='redis', port=6379, db=0)

def consume():
    group = 'tool_consumers'
    consumer = f'consumer-{time.time()}'

    try:
        r.xgroup_create('tool_call_stream', group, mkstream=True, id='0')
    except redis.exceptions.ResponseError:
        pass # already exists

    print("Consumer started!")

    while True:
        res = r.xreadgroup(
            groupname=group,
            consumername = consumer,
            streams={'tool_call_stream': '>'},
            count=5,
            block=5000
        )
        if not res:
            continue

        for stream_name, messages in res:
            for message_id, message in messages:
                # print(f"Processing document {message[b'tool_call_id'].decode()}")
                tool_call = json.loads(message[b'tool_call'].decode())
                tool_call_id = tool_call['tool_call_id']
                tool_name = tool_call['tool_name']
                input = tool_call['input']
                # tool_call_id = message[b'tool_call_id'].decode()
                # tool_name = message[b'tool_name'].decode()
                # input = message[b'input'].decode()

                try:
                    callback_object = json.loads(message[b'callback_object'].decode())
                    auth = message[b'mockAuth'].decode()
                    run_id = message[b'run_id'].decode()
                    invoked_by = message[b'invoked_by'].decode()
                    wait_on = json.loads(message[b'wait_on'].decode())

                    print(f"Data received by tool-call-consumer: {message}")
                    print(f"Callback object received by tool-call-consumer: {callback_object}")
                    print(f"Auth header received by tool-call-consumer: {auth}")
                    print(f"Run_id: {run_id}")
                    print(f"Invoked by executor: {invoked_by}")
                    print(f"Wait on: {wait_on}")

                    data = {
                        "input": input,
                        "futures_id": tool_call_id,
                        "callback_object": callback_object,
                        "wait_on": wait_on
                    }

                    print(f"Data going to executor: {json.dumps(data, indent=2)}")

                    ## Send input and callback object to tool:
                    controller_url = f"http://controller:8000/root?executor={tool_name}&by_id=True&invoked_by={invoked_by}&run_id={run_id}"
                    response = requests.post(
                        url=controller_url,
                        headers={
                            'MockAuth': auth
                        },
                        json=data
                    )
                    print(f"response from controller: {response}")
                except Exception as e:
                    print(f"There was an error reading/sending the data: {e}")
                    pass #for now...

                r.xack('tool_call_stream', group, message_id)
                print(f"Acknowledged {message_id}")

                # data = {
                #         "node_type": "Document",
                #         "fields": {
                #             "id": message_id,
                #             "name": input["name"],
                #             "file_id": input["file_id"],
                #             "file_location": input["file_location"]
                #         }
                #     }
                
                # print(f"Input of type {type(input)}to send to tool {tool_name} via controller: {json.dumps(input, indent=2)}")
                # print(f"Callback object of type {type(callback_object)} for tool: {json.dumps(callback_object, indent=2)}")


                
            

                # Send document information to controller
                # controller_url = 'http://controller:8000/create-node/project/documents' # will be more dynamic later
                # response = requests.post(
                #     url=controller_url,
                #     headers={
                #         'MockAuth': 'remi:user,admin'
                #     },
                #     json=data 
                # )
                
                # print(f"response from controller: {response}")


if __name__ == "__main__":
    print(f"Starting consumer...")
    consume()