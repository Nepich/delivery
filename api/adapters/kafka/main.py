
from api.adapters.kafka.consumer import Consumer


def run():
    consumer = Consumer(
        topics=["basket.confirmed"],
        servers=["localhost:9092"]
    )
    consumer.process()
    

if __name__ == "__main__":
    run()