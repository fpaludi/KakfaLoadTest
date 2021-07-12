# Load Test Event based services

This dummy project shows a way of run a load tests over an async service that consume and produce events.

## Start project
Ir order to run the project you will need docker and docker-compose installed.
Then run:

```
make start_project
```

## Run the test

### Build service image
```bash
make build_dev
```

### Run service
```bash
make run_dev
make create_topics
```

### Run Load test
```bash
cd src
locust -f locust_files/load_test.py --csv=example --csv-full-history
```
Then access to **localhost:8089** and configure locust and load tests as you want

### Analyze results
Then you need to analyze the **example_stats_history.csv** file

TODO: create scripts to analyze file

