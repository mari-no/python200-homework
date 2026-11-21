Part 1: Warmup — Cloud Concepts

Cloud Concepts Question 1
What is the core economic model of cloud computing, and how does it differ from owning your own servers?

Cloud computing uses a pay-as-you-go model: you rent computing resources and pay for what you use instead of buying and maintaining your own servers. This reduces upfront costs and lets you scale resources when needed.

Cloud Concepts Question 2
What is the difference between vertical scaling and horizontal scaling? Give a concrete example of when you might choose each.

Vertical scaling means making one machine more powerful, for example, adding more RAM or upgrading its GPU. You would choose it when one machine needs more resources to handle a task.

Horizontal scaling means adding more machines and distributing the workload between them. You would choose it when an application needs to handle more users or process more data.

Scenarios:
1. A web app that normally handles 1,000 users per day suddenly needs to handle 100,000 after a viral product launch. Horizontal scaling — adding more machines to handle the sudden increase in users.
2. A data scientist's model training job is running too slowly, and they want a machine with a faster GPU and more RAM.  Vertical scaling — upgrading the machine with a faster GPU and more RAM.
3. A data pipeline that processes 10 files per run now needs to process 10,000 files per run, and the work can be split across machines. Horizontal scaling — distributing the 10,000 files across multiple machines.

Cloud Concepts Question 3
Classification:
Gmail — SaaS: You use an application managed entirely by Google.
Azure Virtual Machines — IaaS: You rent virtual machines but manage the operating system and software.
AWS S3 — IaaS: It provides cloud storage infrastructure, while you manage your data and access configuration.
GitHub Codespaces — PaaS: It provides a managed development environment where you can write and run your code.
Snowflake — BaaS: It provides a managed data platform for storing and analyzing data without managing the underlying infrastructure.
Supabase — BaaS: It provides managed backend services such as databases, authentication, and storage.
Definitions:
- IaaS (Infrastructure as a Service): Provides virtual machines, storage, and networking. The developer manages the operating system, software, and applications. Example: Azure Virtual Machines.
- PaaS (Platform as a Service): Provides a managed platform for running applications. The developer mainly manages the code and its configuration. Example: GitHub Codespaces.
- SaaS (Software as a Service): Provides ready-to-use software over the internet. The provider manages almost everything, and the user simply uses the application. Example: Gmail.

Cloud Concepts Question 4
A managed data platform like Databricks or Snowflake provides ready-to-use tools for data processing and analytics on top of cloud infrastructure. Compared to using AWS or GCP directly, it is easier and faster to set up because much of the infrastructure is managed for you. However, you have less flexibility and may pay more for the convenience.

Cloud Concepts Question 5
The cloud isn't the right tool for every problem.
If your dataset fits comfortably on a single machine and you do not have massive compute demands, local processing is often faster and cheaper. This is often the best approach when setting up an initial prototype.

Part 2: Warmup — Cloud Landscape

Cloud Landscape Question 1
The three hyperscalers are:
1. Amazon Web Services (AWS): AWS offers the broadest range of cloud services and is commonly used by large enterprises, startups, and organizations that need flexible cloud infrastructure.
2. Google Cloud Platform (GCP): GCP specializes in data analytics and machine learning and is often used by organizations working with large datasets and AI.
3. Microsoft Azure: Azure is strong in enterprise and government environments because of its integration with Windows, Active Directory, and Microsoft 365.

Cloud Landscape Question 2
Three reasons for switching from Azure to Supabase:
1. Access: Supabase is easier to set up because students can create their own accounts without waiting for organizational invitations or configuring a tenant.
2. Pedagogical fit: Supabase uses a relational database, which helps students learn SQL and data management skills that are useful in many data-related jobs.
3. Pipeline coherence: Supabase allows students to store raw and enriched data in separate related tables, making the ETL pipeline easier to understand, inspect, and debug.
I think choosing a cloud tool should depend not only on its features but also on accessibility, cost, ease of use, and how well it fits the project's goals. The most popular or powerful tool is not necessarily the best choice for every project.

Cloud Landscape Question 3
1. You need to store 10 TB of image files and retrieve them by filename from any machine. - Object storage — AWS S3: It can store large amounts of image files and make them accessible from different machines.
2. You need to run an ML training job on a GPU for four hours, then shut it down.-Compute — AWS EC2: You can rent a GPU-enabled virtual machine for an ML training job and shut it down when the job is finished.
3. You need to host a web API that automatically scales up when traffic spikes and scales down when it quiets.-Serverless compute — Google Cloud Run: It can host a web API and automatically scale based on incoming traffic.
4. You need to send structured data to a large language model and get a text response back.
-LLM API — OpenAI API: It allows you to send structured data to a large language model and receive a text response.
Cloud Landscape Question 4
I would build a weather data analysis project that collects weather information from an external API, stores it in a database, and uses an ML model to predict weather conditions.

Possible technology stack:
- Google Cloud BigQuery: Analyze large amounts of weather data.
- Supabase (PostgreSQL): Store raw weather data and ML predictions.
- OpenAI API: Generate natural-language summaries of weather patterns.
I think consolidating everything under one provider could simplify account management, security, billing, and integration. However, I would give up the flexibility to choose the best service for each task and might miss out on specialized features offered by other providers.

Part 3: Project

Step 5: Confirm
My Supabase project was sussesfully set up, and 2 tables were created.


Part B

Scenario A — Lightweight compute: A t3.micro EC2 instance (1 vCPU, 1 GB RAM), on-demand pricing, running 8 hours per day, 5 days per week (approximately 160 hours per month). Use the US East (N. Virginia) region.


For t3.micro 160 hours/month the price is:
Monthly cost
1.66 USD
Total 12 months cost
19.92 USD
Includes upfront cost
On-Demand instances (monthly): 12.653333 USD

Scenario B — Heavy analytics workload: A p3.2xlarge EC2 instance (8 vCPU, 1 V100 GPU), running 24/7 for the full month (730 hours); an RDS db.m5.large instance (2 vCPU, 8 GB RAM); and an S3 Standard storage bucket with 1 TB of data. Use US East (N. Virginia).
For p3x2large:
Instance: 3.06/Hour
Monthly: 2233.80/Month
RDS db.m5.large
vCPU: 2
Memory: 8 GiB
1 instance(s) x 0.6 USD hourly x 730 hours in a month = 438.0000 USD (RDS Custom for SQL Server)
RDS Custom instance(s) cost (monthly): 438.00 USD

Storage amount: 1 TB x 1024 GB in a TB = 1024 GB
Pricing calculations
1 instances x 1,024 GB x 0.23 USD = 235.52 USD (Storage Cost)
Storage Cost: 235.52 USD
Total Storage cost (monthly): 235.52 USD

Total: 2907.32

I was surprised by how much more expensive heavy analytics workload is compared to lightweight compute. The comparison shows that GPU instances are worth the cost for demanding workloads such as machine learning training and heavy data processing, but they would be unnecessary and wasteful for simple applications or everyday tasks.