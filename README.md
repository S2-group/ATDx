# ATDx: A tool for Providing a Data-driven Overview of Architectural Technical Debt in Software-intensive Systems


This repository is a companion page of the following publication:

> Sebastian Ospina, Roberto Verdecchia, Ivano Malavolta and Patricia Lago. ATDx: A tool for Providing a Data-driven Overview of Architectural Technical Debt in Software-intensive Systems. 15th European Conference on Software Architecture (ECSA'21), Växjö, Sweden, 2 July, 2021.

It contains all the material required for running the ATDx tool, including: installation steps, deployment scenarios, and sample input/output data. 

The ATDx companion tool paper can be found [here](https://github.com/S2-group/ATDx/blob/main/ATDx_tool_ECSA21_paper.pdf).

# Demo
[![ATDX demo](https://github.com/S2-group/ATDx/blob/main/demo_image.png)](https://www.youtube.com/watch?v=ULT9fgxuB7E&ab_channel=RobertoVerdecchia "ATDx demo - click to watch")


# Quick start
In order to run the ATDx tool follow these steps:

### Getting started

1. Clone the repository 
   - `git clone https://github.com/S2-group/ATDx`
 
2. If you do not have Python 3.x installed you can get the appropriate version for your OS [here](https://www.python.org/downloads/).

3. Install the additional python packages required:
   - `pip3 install -r requirements.txt`

### Run ATDx Locally

1. Set the configuration files. Namely [configuration.json](/data/configuration.json) and [report_configuration](/data/report_config.json)
    - In order to mine your own issues and execute the `AnalysisTool`, it is necessary to replace the content of `measures` and `counted_issues` paramethers inside the [configuration.json](/data/configuration.json) with the string `"None"`. This way, the program will know that such information isn't given to it.
    - Add an `issues` folder inside the data folder.
   
2. Execute the `Controller.py` script 
   - `python3 Controller.py`
   - This will be displayed: `Please input 1 for single project analysis or 2 for portfolio analysis`
       - If you input `1`.
         - This will be displayed `Please input the name of the Sistem Under Analysis`
           
         - Input the name of the project we want to analyse
        
       - If you input `2`.
            - The analysis will run for all the projects. 

         - Then, `Please input the main configuration file location.` will be displayed. Input the location of the configuration file you want to use.
         - Finally, `Please input the report configuration file location.` will be displayed. Input the location of the report configuration file you want to use.

3. Some of the steps will displayed in the screen, such as mining issues and measures. The results of these steps will be stored inside folder `/data`

### Run ATDx on a Flask server
In order to make use of the GitHub Webhook functionality, ATDx needs to be deployed on a Flask server as documented below:

1. Set up the configuration files. Namely [configuration](/data/configuration.json) and [report_configuration](/data/report_config.json)

2. Set your repository to trigger the events and communicate them to the ATDx tool. A detailed explanation can be found [here.](https://docs.github.com/en/enterprise-server@3.0/developers/webhooks-and-events/webhooks/about-webhooks).

3. Execute the `FlaskServer.py` script 
   - You need to set the following variables in the Flask_server according to [Github authentication requirements](https://docs.github.com/en/rest/guides/basics-of-authentication):
       1. ```app.config['GITHUB_CLIENT_ID']```
       2. ```app.config['GITHUB_CLIENT_SECRET']```
      
   - Once these values have been set up, check that your server has a public IP and add it to the FlaskServer initialization:
      1. ``` app.run(debug=False, host="YOUR_IP_ADDRESS"")```
      
   - Now we can run`python3 FlaskServer.py`

4. Login to the Server
   - In your browser run: ```YOUR_IP_ADDRESS:5000/LOGIN``` (note that 5000 is the default port)
     
      - The browser will redirect you to a Github page where you need to enter user credentials

5. Create a new PR in your Github repository.
    - The analysis will be run automatically

Sample Input and Output Data
---------------
A sample of input and output data is available [here](data/README.md).

# How to cite us
If this study is helping your research, consider to cite it is as follows, thanks!

```
@article{ospina2021atdx,
  title={ATDx: A tool for Providing a Data-driven Overview of Architectural Technical Debt in Software-intensive Systems},
  author={Ospina, Sebastian and Verdecchia, Roberto and Malavolta, Ivano and Lago, Patricia},
  journal={European Conference on Software Architecture},
  year={2021},
  publisher={Springer}
}
```

# ATDx empirical evaluation
The ATDx approach was evaluated by considering two OSS organizations ([Apache](https://www.apache.org/) and [ONAP](https://www.onap.org/)) and 250+ software projects.<br>

The scientific publication resulting from the evaluation is available at this link: https://peerj.com/articles/cs-833 <br>
The replication package of the study is hosted at the following repository: https://github.com/S2-group/ATDx_replication_package

Directory Structure
---------------
This is the root directory of the repository. The directory is structured as follows:

    ATDx
     .
     |
     |--- code/                             Source code of the ATDx tool
     |
     |--- documentation/                    Files used for the README
     |
     |--- data/                             Sample input and output ata of the ATDx tool, i.e. configuration files, issues, measures, rules, etc.
            |
            |--- reports/                   Report generated by the ATDx tool
            |         |
            |         |--- radarchart/      Radarchart generated by the ATDx tool
            |
            |--- issues/                    Sample issues downloaded by the SonarCloud Miner plugin
            |
            |--- examples/                  Sample input of the ATDx tool
 
