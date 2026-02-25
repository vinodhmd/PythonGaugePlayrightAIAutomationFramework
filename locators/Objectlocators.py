class Objectlocators:
    """
    Object Repository for Login Page.
    Contains locators for all elements on the login page.
    """
    # ------------------------------------------------------------Login Spec files object Field
    # Username Input Field
    # CSS: input[name='user-name']
    # XPath: //input[@name='user-name']
    USERNAME_INPUT = "input[name='user-name']"
    
    # Password Input Field
    # CSS: input[name='password']
    # XPath: //input[@name='password']
    PASSWORD_INPUT = "input[name='password']"
    
    # Login Button
    # CSS: input[name='login-button']
    # XPath: //input[@name='login-button']
    LOGIN_BUTTON = "input[name='login-button']"

    # Application Logo/Title (for verification)
    APP_LOGO = ".app_logo"
    TITLE = ".title"
    # ------------------------------------------------------------Login Spec files object Field
    # CSS: input[name='user-name']
    # XPath: //input[@name='user-name']
    # Payroll Username Input Field
    # CSS: input[name='user-name']
    # XPath: //input[@name='user-name']
    PAYROLL_USERNAME_INPUT = "input[name='user_name']"
    
    # Payroll Password Input Field
    # CSS: input[name='password']
    # XPath: //input[@name='password']
    PAYROLL_PASSWORD_INPUT = "input[name='password']"
    
    # Payroll Login Button
    # CSS: input[name='login-button']
    # XPath: //input[@name='login-button']
    PAYROLL_LOGIN_BUTTON = "//button[text()='Login']"