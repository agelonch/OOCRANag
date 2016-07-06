from heatclient.client import Client
from time import sleep


def credentials(token, user_id):
    heat = Client('1', endpoint="http://147.83.118.228:8004/v1/"+str(user_id), token=token)
    return heat


def create_stack(name, file, token, user_id):
    heat = credentials(token, user_id)
    template = open(file, 'r')
    stack = heat.stacks.create(stack_name=name, template=template.read(), parameters={})
    uid = stack['stack']['id']

    stack = heat.stacks.get(stack_id=uid).to_dict()
    while stack['stack_status'] == 'CREATE_IN_PROGRESS':
        print "INFO: Creating stack."
        stack = heat.stacks.get(stack_id=uid).to_dict()
        sleep(10)

    if stack['stack_status'] == 'CREATE_COMPLETE':
        print "INFO: Stack succesfully created."
    else:
        raise Exception("INFO: Stack fall to unknow status: {}".format(stack))


def delete_stack(name, token, user_id):
    heat = credentials(token, user_id)
    stack = heat.stacks.get(name)
    heat.stacks.delete(stack.parameters['OS::stack_id'])
    print "INFO: Default stack deleted."


def list(token, user_id):
    heat = credentials(token, user_id)
    stacks = heat.stacks.list()
    while True:
        try:
            stack = stacks.next()
            print stack.stack_name + " (" + stack.id + "): " + stack.stack_status
        except StopIteration:
            break
