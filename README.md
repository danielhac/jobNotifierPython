# Job Notifier
This Python/Flask application extracts job information, intelligently stores them in a database without duplicates and finally sends an E-mail upon new findings.

Two daily synchronous AWS Lambdas are deployed to execute the applications.

## Used Technologies

### `Python`
An interpreted, high-level, general-purpose programming language.
### `Flask`
A lightweight WSGI web application framework and REST API.
### `DynamoDB`
Scalable NoSQL database.
### `Boto3`
Amazon Web Services (AWS) SDK for Python for Lambdas, DynamoDB, etc.
### `Asyncio`
Used as a foundation for multiple Python asynchronous frameworks that provide high-performance network and web-servers, database connection libraries, distributed task queues, etc.
### `Selenium`
Suite of tools for automating web browsers & web scraping. 
### `ThreadPoolExecutor`
Executor subclass that uses a pool of threads to execute calls asynchronously.
### `Smtplib`
Defines an SMTP client session object that can be used to send mail to any Internet machine with an SMTP or ESMTP listener daemon.