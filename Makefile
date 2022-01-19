bootstrap:
	poetry install

generate:
	poetry run python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. todo.proto

server:
	ls *.py | entr -r poetry run python server.py
