```plantuml
@startuml
actor Client as client
participant Telegram as telegram
participant Server as server
queue Redis as redis
database PostgreSQL as postgres
participant Celery as celery
participant "Crypto exchange" as crypto_exchange

== Predicting ==
celery -> postgres : getting a schedule\nof periodic tasks
celery -> crypto_exchange : getting course values\naccording to the schedule
celery -> celery : rate predicting
celery -> redis : prediction record

== Getting prediction for the near future ==
client -> telegram : Message: prediction request
telegram -> server : HTTP request: GET /prediction/
server -> redis : getting a prediction\nfor the near future
server -> telegram : HTTP response: prediction\nfor the near future
telegram -> client : Message: prediction for the\nlast time interval
@enduml
```