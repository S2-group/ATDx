# ATDx: A tool for Providing a Data-driven Overviewof Architectural Technical Debt in Software-intensive Systems


This repository is a companion page of:

> Sebastian Ospina, Roberto Verdecchia, Ivano Malavolta and Patricia Lago. ATDx: A tool for Providing a Data-driven Overview of Architectural Technical Debt in Software-intensive Systems. Submitted for review at ECSA’21: 15th European Conference on Software Architecture, Växjö, Sweden, 2 July, 2021 (ECSA’21), 5 pages.

It contains all the material required for replicating our analysis and execute new ones, including: the installation steps, the input data, and different ways to run it. 
Some additional results, not included in the paper for the sake of space, are also provided.



Example Results and Data
---------------
The result example as well as the data we used for our analysis are available [here](data/README.md).


Quick start
---------------
In order to replicate the experiment follow these steps:

### Getting started

1. Clone the repository 
   - `git clone https://github.com/ICSE19-FAST-R/FAST-R`
 
2. If you do not have python3 installed you can get the appropriate version for your OS [here](https://www.python.org/downloads/).

3. Install the additional python packages required:
   - `pip3 install -r requirements.txt`

### Run ATDx Locally

1. Set the configuration files. Namely [configuration.json](/data/configuration.json) and [report_configuration](/data/report_config.json)

2. Execute the `Controller.py` script 
   - `python3 Controller.py`
   - This will be displayed: `Please input 1 for single project analysis or 2 for portfolio analysis`
       - We input `1`.
         - This will be displayed `Please input the name of the Sistem Under Analysis`
           
         - Then we should input the name of the project we want to analyse
        
       - We input `2`.
            - The analysis will run for all the projects. 

         - Then, `Please input the main configuration file location.` will be displayed. So you must input the location of the configuration file you want.
         - Finally, `Please input the report configuration file location.` will be displayed. So you must input the location of the report configuration file you want.

3. Some of the steps are displayed in the screen, such as mining Issues and measures. And the results are stored inside folder `/data`

### Run ATDx on a Flask server
In order to make use of the GitHub Webhook functionality, ATDx needs to be deployed on a Flask server as documented below:

1. Set the configuration files. Namely [configuration](/data/configuration.json) and [report_configuration](/data/report_config.json)

2. set your repository to trigger the events and communicate it so to the ATDx tool. A detailed explanation can be found [here.](https://docs.github.com/en/enterprise-server@3.0/developers/webhooks-and-events/webhooks/about-webhooks).

3. Execute the `FlaskServer.py` script 
   - You need to set the following variables in the Flask_server according to [Github authentication requirements](https://docs.github.com/en/rest/guides/basics-of-authentication):
       1. ```app.config['GITHUB_CLIENT_ID']```
       2. ```app.config['GITHUB_CLIENT_SECRET']```
      
   - Once these values have been set up, check that your server has a public IP and add it to the FlaskServer initialization:
      1. ``` app.run(debug=False, host="YOUR_IP_ADDRESS"")```
      
   - Now we can run`python3 FlaskServer.py`

4. Login to the Server
   - In your browser run: ```YOUR_IP_ADDRESS:5000/LOGIN``` (note that 5000 is the default port)
     
      -The browser will redirect you to a Github page where you need to enter user credentials

5. Create a new PR in your Github repository.
    - The analysis will be run automatically

Directory Structure
---------------
This is the root directory of the repository. The directory is structured as follows:

    ATDx
     .
     |
     |--- data/                             Input of the algorithm, i.e. configuration files, issues, measures, rules. And a Comment example
     |      |
     |      |--- reports/                   Report generated by the algorithm.
     |      |         |
     |      |         |--- radarchart/      Radarchart generated by the algorthm
     |      |
     |      |--- issues/                    Dowloaded issues by the algorithm
     |      |
     |      |--- examples/                  Input examples for the algorthm to run
     |      
     |--- code/                             Implementation of the algorithms and scripts to execute the experiments.
     |
     |--- Documentation/                    Files used for the README
  
