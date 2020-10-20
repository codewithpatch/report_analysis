# report_analysis
Analyze Team Reports for audit

## Table of Contents
[Setting Environment Variables](#setting-up-environment)
[Running the Script](#running-the-script)
[Implementation](#implementation)
[Setting Up settings.py](#setting-up-settingspy)
[Update Date of Run](#update-date-of-run)



<a name="environment"></a>

## Setting up Environment
1. Using command line, install `requirements.txt` from the root directory
```shell script
pip install -r requirements.txt
```

<a name="run"></a>

## Running the Script
1. from the root directory run `main.py`
```shell script
python main.py
```

<a name="implmentation"></a>

## Implementation

<a name="implmentation"></a>
1. The script will process reports, that is dated on previous working day.
2. Excel outputs will go to the output dir `./output` separated in each report folder.

<a name="run-date"></a>
### Setting Up settings.py
You can change the following configuration in settings.py
1. Date of run
2. Set which reports to run
3. Set What team should be inluded in the report analysis
4. Set up directory paths
    - Root directory - **NEVER CHANGE ROOT DIRECTORY**
    - Report source directory
    - Output directory

**NOTE**: If you will make changes on the directory names, make sure that it exists in your root directory

#### Update Date of Run 