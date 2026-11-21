
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

LINK for my video: https://youtu.be/QTTktYRznvI