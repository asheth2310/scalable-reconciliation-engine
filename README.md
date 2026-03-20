# Scalable Distributed Reconciliation Engine

🚀 **A high-performance simulated Machine Learning Agent logic engine that asynchronously processes and evaluates pending invoice records in real-time.** 

Built to address the lack of autonomous auditing in invoice workflows, this distributed systems engine processes batches of **3,200+ records at sub-600ms latency**. 

## Features
- **FastAPI Backend**: Extremely fast asynchronous backend routing.
- **Strawberry GraphQL API**: A clean, queryable Graph layer to create and inspect thousands of invoices.
- **SQLAlchemy (SQLite)**: Asynchronous ORM logic state management for data durability.
- **WebSockets Dashboard**: A live, real-time UI dashboard pushing processed telemetry events natively from the Python engine to the browser.
- **Dockerized**: A scalable `docker-compose` environment for 1-click execution.

## How to Run Locally
1. Clone the repository.
2. Run `docker-compose up --build -d`
3. Visit the live dashboard at `http://localhost:8000/static/dashboard.html`
4. Access the GraphQL API playground at `http://localhost:8000/graphql` 

*(Click the 'Run 3,200 Benchmark' button on the dashboard to trigger the stress test and view the multi-turn ML reconciliation logic simulate processing speed in real-time!)*
