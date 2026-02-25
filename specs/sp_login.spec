<Scenario Outline>
# Swag Labs Login Web Application
<Scenario Outline>

## Successful Login with Credentials
Tags: TC001,smoke,endtoendtesting
* Navigate to the application
* Login with credentials "standard_user" and "secret_sauce"

## Login with Excel Data - Row Based
Tags: TC002,regression
* Navigate to the application
* Login with test data from row "2"

## Swag Labs Login with Read Excel and get Tags TC003 Data 
Tags: TC003,regression,smoke,endtoendtesting
* Navigate to the application
* Login with Swag Labs
* verify the title of the page