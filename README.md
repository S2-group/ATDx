# ATDx
The tool for  providing a data-driven overview of Architectural Technical Debt of software-intensive systems

A complete demo can be found here.

As visualized below, ATDx  consists of the following components:
- **Flask_server**:
- **Controller**: Is in charge of reading the config files, interpret them and setting up the different components
- **Factories**: These components have been skipped in the diagram. They simply build on top of the Report_gen and analysis_tool in such a way that these can vary.
- **Portfolio_Data**: Keeps the information that needs to be analysed, and the information required to generate the report
- **Atdx**: It simply is a static implementation that changes the content of the Portfolio after analysing its content
- **Analysis_tool**: 
- **Report_gen**: 

<p align="center">
<img src="./documentation/Architecture.jpg" alt="Overview of ATDx" width="500"/>
</p>

## Setting up environment, installation and dependencies
Instructions can be found [here](https://github.com/S2-group/ATDx/blob/Demo_1/SETUP.md).

## Quick start
To run an experiment, run:
```bash
python3 Flask_server.py
```
Example configuration files can be found in the subdirectories of the `examples` directory.

## Structure
### config.json
A JSON config that contains the location of the different attributes that are required for the execution of the analysis.
This file should have this attributes filled in:

   ```json
   {
       "tool": "SonarCloud",
       "save_intermediate_steps": true,
       "rules_location": "ar_rules.json",
       "projects_location": "projects.json",
       "measures": "measures.json" ,
       "files_suffix": "new_files"
   }
   ```
### report_config.json
A JSON config that contains the "settings" for the report that is being generated.
This file should have this attributes filled in:
   ```json
   {
       "report": "Markdown",
       "store": 0,
       "max_number_class": "5",
       "max_number_projects": "3"
   }
   ```

