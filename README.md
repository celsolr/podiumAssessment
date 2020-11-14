## Podium Assessment

This project is a QA engineer assignment for Podium. It consists of a suite of 5 tests for general validations targeting https://www.podium.com.


### Technologies

  - Docker
  - Python
  - Selenium


### Pre-requisites

For local execution:

* Python3
* Docker
* Selenium

For execution using the Dockerfile, the only pre-requisite is having Docker installed.

### Execution

Local execution:
- Clone this repository in your computer 
- Navigate to the Tests folder
- Execute the tests.py file

```sh
$ git clone https://github.com/celsolr/podiumAssessment.git
$ cd podiumAssessment/Tests
$ python3 tests.py
```

For execution on a Docker container:

-Clone this repository in your computer
-Navigate to the project root folder - podiumAssessment
-Execute the command 'docker build -t podiumtest . && docker run -it podiumtest'

```sh
$ git clone https://github.com/celsolr/podiumAssessment.git
$ cd podiumAssessment
$ docker build -t podiumtest . && docker run -it podiumtest
```
