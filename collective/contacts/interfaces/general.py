from zope.interface import Interface, Attribute

class ITable(Interface):
    """ List items in a table with custom columns
    """
    
    def columns():
        """ Returns a list of column headers
        """
        
    def rows():
        """ Returns a list of rows containing a dictionary holding
        
            object: the object itself
            cells: list of strings one per cell
        """
        
    def reset():
        """ Resets the search query stored in the session
        """
    
    def email(object):
        """ Returns the email of a specific object
        """

class ISearch(Interface):
    """ Provides search functionality over a specific schema and/or
        by values
    """
    
    def search(query={}, sort='sortable_title'):
        """ Search for items matching the query
        """
        
class ICustomizableView(Interface):
    """ Marks a view as customizable
    """
    
    def customize_url():
        """ Returns the URL to customize a view
        """

class ICustomizableColumns(Interface):
    """ Provides customizable columns used by ITable
    """
    
    def set_columns(columns):
        """ Sets the columns
        
            columns: list of columns to be shown
        """
    
    def get_columns():
        """ Gets the list of columns to be shown
        """
    
    def get_raw_columns():
        """ Gets the list of tuples holding the name of the column
            and a boolean defining whether the columns is shown or not
        """
        
    def translate_column(column):
        """ Translates a column
        """
        
class IExport(Interface):
    """ Provides format specific export functionality
    """
    title = Attribute("title", "The title of the export format")
    
    def export(request=None, objects=None):
        """ Exports all/provided objects and sets the response header
            if a request is provided otherwise returns the export data
        """
    
class IImport(Interface):
    """ Provides format specific import functionality
    """
    title = Attribute("title", "The title of the import format")
    
    def importFile(file):
        """ Imports objects contained in the provided file and returns
            the number of persons imported
        """
    
    def successMsg(imported):
        """ The internationalized message to be display to the user after
            successful import
        """
        
    def errors():
        """ Returns a list of error messages raised by the last import
        """
    