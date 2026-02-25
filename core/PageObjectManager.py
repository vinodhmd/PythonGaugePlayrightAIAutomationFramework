"""
Page Object Manager - Centralized management for all page objects
Provides a common pattern for creating and accessing page object instances
"""
class PageObjectManager:
    """
    Singleton manager for all page objects in the framework.
    Ensures only one instance of each page object exists during test execution.
    """
    _instances = {}
    
    @classmethod
    def get_page(cls, page_class):
        """
        Get or create a page object instance.
        Args:
            page_class: The page object class to instantiate
        Returns:
            Instance of the requested page object class
        Example:
            login_page = PageObjectManager.get_page(LoginPage)
            employee_page = PageObjectManager.get_page(EmployeeCreation)
        """
        class_name = page_class.__name__
        if class_name not in cls._instances:
            cls._instances[class_name] = page_class()
        return cls._instances[class_name]
    
    @classmethod
    def reset_page(cls, page_class):
        """
        Reset a specific page object instance.
        Useful when you need to reinitialize a page.
        Args:
            page_class: The page object class to reset
        """
        class_name = page_class.__name__
        if class_name in cls._instances:
            del cls._instances[class_name]
    
    @classmethod
    def reset_all(cls):
        """
        Reset all page object instances.
        Typically called in hooks (e.g., before_scenario or after_scenario).
        """
        cls._instances.clear()
