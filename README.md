# ATDx Tool
## Architectural Components
The tool for  providing a data-driven overview of Architectural Technical Debt of software-intensive systems

A complete demo can be found here.

As visualized below, ATDx  consists of the following components:
- **Flask_server**: The ATDx tool is hosted on a Flask Web server. While the tool can be run locallywithout the need of a dedicated Web server, the Flask server allows the ATDx tool to interactwith GitHub repositories and make use of the GitHub Webhook functionality  
- **Controller**: Is in charge of reading the config files, interpret them and setting up the different components
- **Analysis Tool Factory**: This component acts as abstraction mechanism interfacing the ATDxtool with the analysis tool(s) used to gather the AR violations used by ATDxCore(e.g.,Sonar-Cloud, SonarGraph, etc.). This component implements the ‘factory method’ design pattern,where third-party analysis tools can be integrated as external plug-ins. This technical solution allows users to customize the ATDx tool according to their specific needs, while delegating the  interfacing of their used analysis tool to the other components via theAnalysis Tool Factory.
- **Report Generator Factory**: The component Report Generator Factory is responsible for generating the report summarizing the ATDx results. Similarly to the \texttt{Analysis Tool Factory}, this component is implemented according to the factory method design pattern. This allows users to implement report generators which produce their preferred format (\eg Markdown, XML, etc.), without having to spend effort/time on how the created instance needs to interact with the other ATDx tool components. 
- **Portfolio_Data**: Keeps the information that needs to be analysed, and the information required to generate the report
- **AtdxCore**:  It is the component implementing the main business logic of \name. Specifically, this component is responsible for executing the complete ATDx calculation, from the normalization of software metric measurements, to the severity calculation of AR violations, and calculation of ATDD and ATDx values (for more information on the ATDx approach, refer to the original publication~\cite{verdecchia2020atdx}). The ATDx execution can be invoked either by considering an entire software portfolio, or just a software project under analysis, if a dataset of a portfolio is already available.


<p align="center">
<img src="./documentation/Architecture.png" alt="Overview of ATDx" width="500"/>
</p>

## Setting up environment, installation and dependencies
Instructions can be found [here](https://github.com/S2-group/atdx/main/SETUP.md).

## Quick start
To run at the server:
```bash
python3 FlaskServer.py
```

To run at the local machine run:
```bash
python3 Controller.py
```

### Input and output
Example of Input and output files can be found in the `data/examples` directory.



