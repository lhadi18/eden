![alt text](edenlogo.jpg)

# Table of Contents
- [What is Sahana Eden?](#what-is-sahana-eden)
- [Getting Started](#getting-started)
- [Reporting Bugs](#reporting-bugs)
- [Contribute](#contribute)
- [Contact Us](#contact-us)


# What is Sahana Eden?
[Sahana Eden](https://eden.sahanafoundation.org/wiki/What) is an Open Source Humanitarian Platform which can be used to provide solutions for Disaster Management, Development, and Environmental Management sectors. It is supported by the [Sahana Software Foundation](http://sahanafoundation.org/).



# Getting Started

## ⚠️ Alert
At present, the end-user version of Sahana Eden is unavailable beacuse it is not currently maintained.

However, the developer version of Sahana Eden is fully operational. Developers can access the system for testing, customization, and maintenance purposes through the development environment. Technical users and contributors can continue using and modifying the system as needed.

We are actively working on resolving the issues with the end-user version to ensure that all functionalities are restored. Updates on the progress will be shared regularly.

<br>

## Prerequisites

Before installing, please ensure you have the following softwares installed:
- Python
```html
    python --version
```

- Pip
```html
    pip --version
```

- Git
```html
    git --version
```
<br>

## Installation
### 1. Install Web2py

Clone the Web2py Repository by running this command in your terminal:
```html
    git clone https://github.com/web2py/web2py.git
```


### 2. Unzip the zip files 

### 3. Install the required packages
```html
    pip install lxml reportlab shapely xlrd xlwt python-dateutil
```

### 4. Navigate to the applications directory
```html
    cd web2py/applications
```

### 5. Clone the Sahana Eden Repository
```html
    git clone https://github.com/sahana/eden.git
```

### 6. Navigate to the web2py directory
```html
    cd ..
```

### 7. Run the web2py.py 
```html
    python web2py.py
```
<br>

## Configurations
### 1. Set up admin password
When the dialog box opens, enter your admin password.

### 2. Generate your 000_config.py
Upon running Eden for the first time, 000_config.py is generated.

### 3. Navigate to the models directory
```html
    cd web2py/applications/eden/models
```

### 4. Edit 000_config.py
Delete or comment out the line: (`FINISHED_EDITING_CONFIG_FILE = False`)

<br>

## Reporting Bugs
1. **Account Setup**: 
   - Register for a free GitHub account and log in.

2. **Search Existing Issues**: 
   - Visit the [Eden Issue Tracker](https://github.com/sahana/eden/issues).
   - Use the search bar and labels dropdown to check if your bug is already reported.
   - Ensure the search includes open issues (`is:open`).

3. **Reporting Bugs**: 
   - Verify the bug hasn’t been reported or fixed (check commit logs if needed).
   - Provide clear and detailed steps to reproduce the problem.
   - Specify the template used for testing.
   - Include screenshots for clarity when necessary.
   - If you encounter a ticket, copy and paste the traceback into your report instead of just the ticket ID.

By following these guidelines, you ensure efficient communication and resolution of issues.

For more information, click [here](https://eden.sahanafoundation.org/wiki/BugReportingGuidelines).

<br> 

## Contribute
We can always use help from:

- [Developers](https://eden.sahanafoundation.org/wiki/Develop)
    - [Blueprints](https://eden.sahanafoundation.org/wiki/BluePrint) - functionality that we would like to see implemented
    - [Developer Guidelines](https://eden.sahanafoundation.org/wiki/DeveloperGuidelines)
- [Testers](https://eden.sahanafoundation.org/wiki/Testing)
    - [Bug Reporting Guidelines](https://eden.sahanafoundation.org/wiki/BugReportingGuidelines)
- Bug Marshals
    - [Patch Reviewing Guidelines](https://eden.sahanafoundation.org/wiki/PatchReviewingGuidelines)
- Newsletter Report Writers
- Documenters
- [Translators](https://eden.sahanafoundation.org/wiki/UserGuidelines/Localisation)
- [Designers](https://eden.sahanafoundation.org/wiki/Design)
- [SysAdmin](https://eden.sahanafoundation.org/wiki/SysAdmin)
- [GIS Specialists](https://eden.sahanafoundation.org/wiki/GIS)

If you want to get started straight away you can pick a task to work on:
- [Code Tasks](https://eden.sahanafoundation.org/wiki/Contribute/Code)
- [Documentation Tasks](https://eden.sahanafoundation.org/wiki/Contribute/Documentation)
- [Outreach Tasks](https://eden.sahanafoundation.org/wiki/Contribute/Outreach)
- [Quality Assurance (QA) Tasks](https://eden.sahanafoundation.org/wiki/Contribute/QA)
- [User Interface (UI) Tasks](https://eden.sahanafoundation.org/wiki/Contribute/UI)

Or go ahead and pick one of our [Easy Bugs](http://eden.sahanafoundation.org/report/18) to fix

Please sign the [Contributor's License Agreement](http://bit.ly/SSF-eCLA).

## Contact Us
You can get in touch with the Sahana Eden Community immediately though our [Google Group](https://groups.google.com/g/sahana-eden).




