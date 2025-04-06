generate_proto:
	poetry run python -m grpc_tools.protoc -I./infrastructure/adapters/grpc/protos \
	--python_out=./infrastructure/adapters/grpc/out \
	--pyi_out=./infrastructure/adapters/grpc/out \
	--grpc_python_out=./infrastructure/adapters/grpc/out \
	./infrastructure/adapters/grpc/protos/geo.proto