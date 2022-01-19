import concurrent.futures
import logging

import grpc
from grpc_reflection.v1alpha import reflection

import todo_pb2
import todo_pb2_grpc


tasks = [{
    'id': '1',
    'description': 'Task #1',
}, {
    'id': '2',
    'description': 'Task #2',
}]


class TodoServicer(todo_pb2_grpc.TodoServicer):

    def List(self, request, context):
        return todo_pb2.ListResponse(
            tasks=[todo_pb2.Task(**task) for task in tasks],
        )

    def Add(self, request, context):
        tasks.append({
            'id': str(len(tasks) + 1),
            'description': request.description,
        })
        return todo_pb2.AddResponse(
            task=todo_pb2.Task(**tasks[-1]),
        )

    def Complete(self, request, context):
        task = next(t for t in tasks if t['id'] == request.task)
        task['completed'] = request.completed
        return todo_pb2.CompleteResponse(
            task=todo_pb2.Task(**task),
        )


def main():
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(max_workers=25),
    )
    server.add_insecure_port('localhost:50051')

    reflection.enable_server_reflection([
        reflection.SERVICE_NAME,
        todo_pb2.DESCRIPTOR.services_by_name['Todo'].full_name,
    ], server)

    todo_pb2_grpc.add_TodoServicer_to_server(TodoServicer(), server)

    server.start()
    logging.info("grpc server started")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
