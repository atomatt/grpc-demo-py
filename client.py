import grpc
import logging
import sys

import todo_pb2
import todo_pb2_grpc


def list_cmd(todo, *args):
    r = todo.List(todo_pb2.Empty())
    logging.info(r)


def add_cmd(todo, description, *args):
    r = todo.Add(todo_pb2.AddRequest(
        description=description,
    ))
    logging.info(r)


def complete_cmd(todo, task, completed='true', *args):
    r = todo.Complete(todo_pb2.CompleteRequest(
        task=task,
        completed=completed.lower()[0] in ['y', 't'],
    ))
    logging.info(r)


cmd = {
    'list': list_cmd,
    'add': add_cmd,
    'complete': complete_cmd,
}


def main(cmd_name, *args):
    channel = grpc.insecure_channel('localhost:50051')
    todo = todo_pb2_grpc.TodoStub(channel)
    cmd[cmd_name](todo, *args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(*sys.argv[1:])

