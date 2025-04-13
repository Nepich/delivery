generate_proto:
	poetry run python -m grpc_tools.protoc -I./infrastructure/adapters/grpc/protos \
	--python_out=./infrastructure/adapters/grpc/out \
	--pyi_out=./infrastructure/adapters/grpc/out \
	--grpc_python_out=./infrastructure/adapters/grpc/out \
	./infrastructure/adapters/grpc/protos/geo.proto

generate_kafka:
	poetry run python -m grpc_tools.protoc -I./api/adapters/kafka/protos \
	--python_out=./api/adapters/kafka/out \
	--pyi_out=./api/adapters/kafka/out \
	./api/adapters/kafka/protos/contract.proto

generate_producer:
	poetry run python -m grpc_tools.protoc -I./infrastructure/adapters/kafka/protos \
	--python_out=./infrastructure/adapters/kafka/out \
	--pyi_out=./infrastructure/adapters/kafka/out \
	./infrastructure/adapters/kafka/protos/kafka_contract.proto