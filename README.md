# 🩺 HealthCheck Pro

### Smart Website Monitoring and Automated CI System

HealthCheck Pro is a Python-based website monitoring system that checks the availability, HTTP status, and response time of multiple websites.

The project also demonstrates DevOps practices by using Git, GitHub, automated testing, and GitHub Actions for Continuous Integration (CI).

---

## 📌 Project Overview

Websites and online services need to be continuously monitored to ensure that they are available and responding properly.

HealthCheck Pro automatically checks configured websites and reports:

- Website availability
- HTTP status code
- Response time
- Slow websites
- Down websites
- Historical monitoring data
- HTML monitoring dashboard

The project uses GitHub Actions to automatically execute automated tests whenever new code is pushed to the main branch.

---

## 🎯 Objectives

The main objectives of HealthCheck Pro are:

1. Monitor the availability of websites.
2. Measure website response time.
3. Identify unavailable or slow websites.
4. Maintain monitoring history.
5. Generate an HTML monitoring dashboard.
6. Implement automated software testing.
7. Demonstrate Continuous Integration using GitHub Actions.

---

## ✨ Features

### Website Monitoring
Checks multiple websites and determines whether they are UP, SLOW, or DOWN.

### Response Time Monitoring
Measures how long each website takes to respond.

### HTTP Status Detection
Records HTTP status codes such as:

- 200 - Successful request
- 404 - Not Found
- 500 - Server Error

### Monitoring History
Stores monitoring results in a CSV file.

### HTML Dashboard
Generates a simple visual dashboard containing website status, response time, and observed uptime.

### Automated Testing
The project contains automated tests for:

- Website availability
- Website failure handling
- Response time measurement

### Continuous Integration
GitHub Actions automatically runs the tests whenever code is pushed to the `main` branch.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Git | Version control |
| GitHub | Source code hosting |
| GitHub Actions | Continuous Integration |
| Python unittest | Automated testing |
| HTML/CSS | Monitoring dashboard |
| CSV | Monitoring history |

---

## 🏗️ System Architecture

```text
                Developer
                    |
                    v
              Python Source Code
                    |
                    v
                   Git
                    |
                    v
                 GitHub
                    |
                    v
            GitHub Actions
                    |
          +---------+---------+
          |                   |
          v                   v
     Setup Python        Run Tests
                              |
                              v
                         Test Results
                              |
                     +--------+--------+
                     |                 |
                     v                 v
                   PASS              FAIL
                     |
                     v
                  Success