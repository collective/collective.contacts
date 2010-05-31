from zope.interface import Interface

class ITable(Interface):
    """ List items in a table with custom columns
    """
    
    def set_sort(sort):
        """ Defines the sorting (to be called before getting the rows)
        """
    
    def columns():
        """ Returns a list of column headers
        """
        
    def rows():
        """ Returns a list of rows containing a dictionary holding
        
            object: the object itself
            cells: list of strings one per cell
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
    