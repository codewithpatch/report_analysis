# report_analysis
Analyze Team Reports for audit

## Table of Contents
1. [Setting Environment Variables](#setting-up-environment)
2. [Running the Script](#running-the-script)
3. [Implementation](#implementation)
    1. [Setting Up settings.py](#setting-up-settingspy)
        1. [Update Date of Run](#update-date-of-run)
        2. [Setting up Team](#setting-up-team)
        3. [Setting up Reports to Run](#setting-up-reports-to-run)
    2. [Pipeline Class](#pipeline-class)
        1. [Architecture of Pipeline Class](#architecture-of-pipeline-class)
        2. [Other attributes and methods in pipeline class](#other-attributes-and-methods-in-pipeline-class)
        3. [Creating new Report or Pipeline class](#creating-new-report-or-pipeline-class)
    3. [ReportReader Class](#reportreader-class)
        1. [Usage](#usage)
        2. [Attributes and Methods of ReportPath Class](#attributes-and-methods-of-reportpath-class)
    4. [ReportPath Class](#reportpath-class)
        1. [Usage](#usage)
        2. [Attributes and Methods of ReportPath Class](#attributes-and-methods-of-reportpath-class)


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
### Setting up settings.py
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
In `settings.py`, the default date of run is date today. The automation will process all data dated the previous weekday.
```python
from datetime import date
```

```python
DATE = date.today()
```

You may set the date of run to different date. 

For example, you want to run the automation on October 12 2020, Monday.

```python
DATE = date(2020, 10, 12)
``` 

The automation will process all data on previous working day. October 9 2020, Friday.

#### Setting up Team
In `settings.py`, `TEAMS` variable sets which team will be included in the report analyais. If you want to add or remove team, just set it up from the list.
```python
TEAMS = ['BONDS', 'EQD STRUCT', 'FXMM', 'FUNDING']
```

**NOTES**:
1. Teams that is in the list, should have it's corresponding folder in the reports directory.
2. Lookup for folder name is **CASE SENSITIVE**. Team name in the list **should match the exact folder name**.

#### Setting up Reports to Run
You may decide what reports to run in `settings.py`.
1. **RUN ALL REPORTS**
    ```python
    RUN_ALL = True
    ```
2. If you want to run only specific reports, Change `RUN_ALL` to `False` and set your report as `1` or `0` in `REPORTS` dictionary.
    1. `1` -> automation will run the report
    2. `0` -> automation will not run the report
        Example: If you want to only run, `ExceptionRecords` and `MissingInMX` reports;
        ```python
        RUN_ALL = False
        
        REPORTS = {
            'ExceptionRecords': 1,
            'Matched': 0,
            'MISMATCH': 0,
            'MissingInMX': 1,
            'MissingInSAA': 0,
            'UnclassifiedException': 0,
        }
        ```
3. To run specific report in the `REPORTS` dict, it has a counterpart setup in `main.py`.
    1. Go to `main.py` and add the pipeline class of the specific report in `pipes` array and make sure **IMPORT THAT PIPELINE CLASS from `pipelines` module**.
        ```python
        from pipelines.exception_records import ExceptionRecordsPipeline
        from pipelines.matched import MatchedPipeline
        from pipelines.mismatch import MismatchPipeline
        from pipelines.mx import MissingInMXPipeline
        from pipelines.saa import MissingInSaaPipeline
        from pipelines.unclassified_exception import UnclassifiedExceptionPipeline
       
        pipes = [
            ExceptionRecordsPipeline,
            MismatchPipeline,
            UnclassifiedExceptionPipeline,
            MatchedPipeline,
            MissingInSaaPipeline,
            MissingInMXPipeline
        ]
       ```

### Pipeline Class
Every reports that is being run has its corresponding Pipeline Class in `pipelines` module.

Each reports is separated in different py file in `pipelines` directory, with filename representing it's report name.

Example of the report string, and how to import into `main.py`:
1. `ExceptionRecords` report is in `./pipelines/exception_records.py` with a pipeline class `ExceptionRecordsPipeline`.
   ```python
   from pipelines.exception_records import ExceptionRecordsPipeline
   ```
2. `MissingInMX` report is in `./pipelines/mx.py` with a pipeline class `MissingInMXPipeline`.
   ```python
   from pipelines.mx import MissingInMXPipeline
   ```
3. `MissingInSAA` report is in `./pipelines/saa.py` with a pipeline class `MissingInSaaPipeline`.
   ```python
   from pipelines.saa import MissingInSaaPipeline
   ```

#### Architecture of Pipeline Class
1. `main.py` calls and runs the pipeline class in the following order: For this example we will use `MissingInSaaPipeline`
    1. Initialize the pipeline class
        1. This will initialize the class and runs the `__init__` method from the class.
            ```python
            pipeline = MissingInSaaPipeline()
            ```
        2. Initialization includes:
            1. Inheritance of `ReportReader` class which gives us the ability to read report for our specific pipeline class.
            2. Being able to generate a dateframe for the `MASTER` report which can be accessed through `self.master_df`
            3. Generate a consolidated report dataframe from each team through `self.consolidated_df`
            4. Set the `Comments` and `Team` columns of `self.master_df` dataframe to empty or `nan` values.
            
    2. Run `self.process_df()` method:
        ```python
        pipeline.process_df()
        ```
       1. `process_df` method will now process the `self.master_df` which is the master report dataframe read the the `ReportReader` class.
            
            Process includes:
            1. `self.__add_comment` - applied to the `self.master_df` and loop through it's row using `apply` method of `pandas Dataframe` class.
            
                Comments will be matched with the consolidated report and perform matching if a row in `self.master_df` is in `self.consolidated_df`.
            
            2. `self.__add_team` - applied to the `self.master_df` and loop through it's row using `apply` method of `pandas Dataframe` class and look for the Team name in `consolidated_df`.
            
    3. Run `self.end_process()` method:
       ```python
       pipeline.endprocess()
       ```
   1. `end_process` method is going to export the processed data: `consolidated_df`, and `no_comments_df` from `step iii.` - `self.process_df(self)` and write it to excel file int `OUT_DIR` -> `./output/`
    
       The output filename consist of `report_name`, `date_of_process`, and the df type: `consolidated_df` or `no_comments_df`.
       
       ```
       Example:
       1. filename:
            "ExceptionRecords_16Oct2020_consolidated.xlsx"
       2. output directory:
            "./output/ExceptionRecords/"
       3. filepath:
            "./output/ExceptionRecords/ExceptionRecords_16Oct2020_consolidated.xlsx"
       ```
      
#### Other attributes and methods in pipeline class
1. `self.no_comments_df()` - This is a property attribute that generates a dataframe of rows with no comments from the `master_df`.

#### Creating new Report or Pipeline class
In `template.py` from the pipelines module, it consist the basic template of the pipeline class.

In order to create new pipeline for your new report:
1. Copy `template.py` and rename the py file into filename that represents your report or part of your report.
2. Change `TemplatePipeline` into the name of your report.
3. Set the class attribute `report` to your report name.

    Example - Your report name is `MyNewReport`:
    ```python
   class MyNewReport:
       report = "MyNewReport"
   ```
4. Set criteria in `__add_comment` and `__add_team` method of which columns you want to match your `master_df` with `consolidated_df` on looking up comments and team.
    ```python
   criteria = {
        'ColumnName1': df['ColumnName1'],
        'ColumnName2': df['ColumnName2']
   } 
   ```
5. Set your new pipeline class in `settings.py` and `main.py` to run your new report. Refer to [Setting up Reports to Run](#setting-up-reports-to-run) section of this documentation.
   
**NOTE**:
- This will only do the most basic matching and look up of comments for reports.
- If there are special cases for your new report, you might need to add code somewhere in the pipeline class to implement the special cases.

### ReportReader Class
`ReportReader` is a class in utils module which reader your report for you.

#### Usage
1. To instantiate the `ReportReader` class, you need to pass in `report` as parameter which is your report name. 
    ```python
    reader = ReportReader('MissingInMX')
    ```

    **NOTE: Always make your report name the same as your report folder name CASE SENSITIVE**

2. `self.master_df` - This will return you a dataframe of the master of the report you passed in instantiating the class.
    ```
    df = reader.master_df
    ```
   
3. `self.consolidated_df` - This will return you a dataframe of the consolidated report for all the teams that is set up in `settings.py`. Reference: [Setting Up Team](#setting-up-team)

4. `self.read_report()` - This will return you a dateframe of one report
    
    Parameters:
    1. `team: str`
        - Required parameter
        - This will tell the class to read the reports for the specific `team` that you passed in.
        - The report that will be read is whichever report you passed in to ReportPath class as instance parameter.
        ```python
        df = reader.read_report(team='BONDS')
        ```
    2. `any_file: Optional[bool]`
        - Optional parameter
        - if you set `any_file` to true, it will make the ReportReader class read any filename in the `team` directory regardless of the `report` name
        ```python
        df = reader.read_report(team='BONDS', any_file=True)
        ```
    3. `filename: Optional[str]`
        - Optional paramater
        - This will make the ReportReader class to read the `filename` that you passed as parameter. If `filename` is not found, the automation will fail and stop.
        
### ReportPath Class
`ReportPath` is a class that gives you the paths, filenames, and globs information for a specific report and team.

ReportPath class is going to look for the specific excel file that you will need to read.

#### Usage
1. To instantiate the ReportPath Class, you need to pass the following parameters:
    1. `report: str` - Report name
        - Required parameter
        - This will specify which `report` directory you are looking for.
        
    2. `team: str` - Team name
        - Required parameter
        - This will specify which `team` directory you are looking for.
    
    ```python
    rpath = ReportPath(report='MissingInMX', team='BONDS')
    ```
    
    3. `any_file: Optional[bool]`
        - Optional parameter
        - default is `False`
        - If you passed this parameter, it will disregard the report name as glob and just look for any excel files that is in the `team` directory
        - **NOTE**: Your team directory must only have one excel file. If the script found 0 or more than 1 excel file in the directory, you will get an error and the automation will fail.
        - You might only need to use this for special cases of your report
        ```python
        rpath = ReportPath(report='MissingInMX', team='BONDS', any_file=True)
        ```
        
    4. `filename: Optional[str]`
        - Optional parameter
        - If you passed this parameter, it will disregard the report name as glob, and just look for the specific `filename` that you passed in the class instance.
        ```python
        rpath = ReportPath(report='MissingInMX', team='BONDS', filename='specific_filename.xlsx')
        ```

#### Attributes and Methods of ReportPath Class
1. `self.process_date` - returns the previous working date from the date of run in string format
    ```python
    adate = rpath.process_date # Example result: '16 Oct 2020'
    ```
   
2. `self.glob_path` - returns the glob path that you can use for `glob.glob(path)` method of finding filenames in directory. The glob is **CASE INSENSITIVE** when looking for excel files.
    ```python
    glob_path = rpath.glob_path 
   # Output: '/Users/pluggle/Documents/Github/report_analysis/src/BONDS/201016/[Mm][Ii][Ss][Ss][Ii][Nn][Gg][Ii][Nn][Mm][Xx]*.xlsx'
    ```
   
3. `self.filepath` - returns the absolute path of our file
    - you can use this on `read_report` method of the [ReportReader Class](#reportreader-class).
   ```python
   filepath = rpath.filepath
   # Output: '/Users/pluggle/Documents/Github/report_analysis/src/BONDS/201016/MissingInMX.xlsx'
   ```

4. `self.dir` - returns the directory of `report` and `team` that you passed in.
    ```python
   directory = rpath.dir
   # Output: '/Users/pluggle/Documents/Github/report_analysis/src/BONDS/201016'
   ```

5. `self.glob_filename` - returns the filename parth of your `globpath`. Again, this glob filename is **CASE INSENSITIVE** in looking for filenames of the excel files.
    ```python
   glob_fn = rpath.glob_filename
   # Output: '[Mm][Ii][Ss][Ss][Ii][Nn][Gg][Ii][Nn][Mm][Xx]*.xlsx'
   ```