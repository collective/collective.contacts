from zope.interface import implements

from collective.contacts import contactsMessageFactory as _
from collective.contacts.content.person import Person
from collective.contacts.content.organization import Organization
from collective.contacts.interfaces import ICustomizableColumns

class BaseColumns(object):
    
    def __init__(self, context):
        self.context = context
    
    def convert_to_raw(self, columns):
        new = []
        for name, shown in self.default:
            new.append((name, name in columns))
        return tuple(new)
    
    def get_columns(self):
        return [name for name, shown in self.get_raw_columns() if shown]

class PersonColumns(BaseColumns):
    """ Provides functionality to customize the columns of a listing of persons
    """
    implements(ICustomizableColumns)
    default = [('title', True),
               ('shortName', False),
               ('firstName', False),
               ('lastName', False),
               ('birthdate', False),
               ('organization', True),
               ('position', False),
               ('department', False),
               ('workPhone', False),
               ('workPhoneInternal', False),
               ('workMobilePhone', False),
               ('workFax', False),
               ('workEmail', False),
               ('phone', True),
               ('mobilePhone', True),
               ('email', True),
               ('web', True),
               ('address', True),
               ('city', True),
               ('zip', True),
               ('country', True),
               ('state', False),
               ('workEmail2', False),
               ('workEmail3', False),
               ('photo', False),
               ('text', False)]
    
    def set_columns(self, columns):
        """ Sets the columns
        
            columns: list of columns to be shown
        """
        self.context.show_on_persons_view = self.convert_to_raw(columns)
    
    def get_raw_columns(self):
        """ Gets the list of tuples holding the name of the column
            and a boolean defining whether the columns is shown or not
        """
        return self.convert_to_raw([column for column, shown in getattr(self.context, 'show_on_persons_view', self.default) if shown])
        
    def translate_column(self, column):
        """ Translates a column
        """
        try:
            return Person.schema.get(column).widget.label
        except:
            return column
        

class OrganizationColumns(BaseColumns):
    """ Provides functionality to customize the columns of a listing of organizations
    """
    implements(ICustomizableColumns)
    default = [('title', True),
               ('sector', True),
               ('sub_sector', True),
               ('phone', True),
               ('phoneInternal', False),
               ('fax', True),
               ('email', True),
               ('web', True),
               ('address', True),
               ('city', True),
               ('country', True),
               ('state', False),
               ('zip', False),
               ('extraAddress', False),
               ('email2', False),
               ('email3', False),
               ('text', False)]
    
    def set_columns(self, columns):
        """ Sets the columns
        
            columns: list of columns to be shown
        """
        self.context.show_on_organizations_view = self.convert_to_raw(columns)
    
    def get_raw_columns(self):
        """ Gets the list of tuples holding the name of the column
            and a boolean defining whether the columns is shown or not
        """
        return self.convert_to_raw([column for column, shown in getattr(self.context, 'show_on_organizations_view', self.default) if shown])
        
    def translate_column(self, column):
        """ Translates a column
        """
        try:
            return Organization.schema.get(column).widget.label
        except:
            return column
    
class GroupColumns(object):
    """ Provides the columns of a listing of groups
    """
    translations = {'title': _("listingheader_groups_name", default=u"Name"),
                    'members': _("listingheader_groups_members", default=u"Members")}
    
    def __init__(self, context):
        self.context = context
    
    def set_columns(self, columns):
        pass
    
    def get_columns(self):
        return ('title',
                'members',)
    
    def get_raw_columns(self):
        return (('title', True),
                ('members', True),)
        
    def translate_column(self, column):
        """ Translates a column
        """
        return self.translations.get(column, column)
    