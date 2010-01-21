==============================
Contacts package documentation
==============================

Introduction
============

This is a full-blown functional test. The emphasis here is on testing what the
user may input and see, and the system is largely tested as a black box. We use
PloneTestCase to set up this test as well, so we have a full Plone site to play
with. We *can* inspect the state of the portal, e.g. using  self.portal and
self.folder, but it is often frowned upon since you are not treating the system
as a black box. Also, if you, for example, log in or set roles using calls like
self.setRoles(), these are not reflected in the test browser, which runs as a
separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.handleErrors = False
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The Address Book content type
=============================

In this section we are tesing the Address Book content type by performing
basic operations like adding, updadating and deleting Address Book content
items.

Adding a new Address Book content item
--------------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Address Book' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Address Book').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Address Book' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Address Book Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Address Book' content item to the portal.

Updating an existing Address Book content item
----------------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Address Book Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Address Book Sample' in browser.contents
    True

Removing a/an Address Book content item
---------------------------------------

If we go to the home page, we can see a tab with the 'New Address Book
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Address Book Sample' in browser.contents
    True

Now we are going to delete the 'New Address Book Sample' object. First we
go to the contents tab and select the 'New Address Book Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Address Book Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Address Book
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Address Book Sample' in browser.contents
    False

Adding a new Address Book content item as contributor
-----------------------------------------------------

Not only site managers are allowed to add Address Book content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Address Book' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Address Book').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Address Book' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Address Book Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Address Book content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Person content type
========================

In this section we are tesing the Person content type by performing
basic operations like adding, updadating and deleting Person content
items.

Adding a new Person content item
--------------------------------

First let's get inside an Address Book.

    >>> browser.getLink('Address Book Sample').click()

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Person' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Person').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Person' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='firstName').value = 'Juan'
    >>> browser.getControl(name='lastName').value = 'Perez'
    >>> browser.getControl(name='position').value = 'Position'
    >>> browser.getControl(name='department').value = 'Department'
    >>> browser.getControl(name='workEmail').value = 'test@test.com'
    >>> browser.getControl(name='email').value = 'test@test.com'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Person' content item to the portal.

Updating an existing Person content item
----------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='firstName').value = 'Pepe'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'Pepe' in browser.contents
    True

Removing a/an Person content item
---------------------------------

If we go to the address book, we can see the 'Pepe' first name in the content.

    >>> browser.open(portal_url)
    >>> browser.getLink('Address Book Sample').click()
    >>> 'Pepe' in browser.contents
    True

Now we are going to delete the 'Pepe Perez' object. First we go to the contents
tab and select the 'Perez, Pepe' for deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('Perez, Pepe').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the address book, there is no longer a 'Perez, Pepe' item.

    >>> browser.open(portal_url)
    >>> browser.getLink('Address Book Sample').click()
    >>> 'Perez, Pepe' in browser.contents
    False

Adding a new Person content item as contributor
-----------------------------------------------

Not only site managers are allowed to add Person content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Address Book Sample').click()
    >>> browser.getLink('Add new').click()

We select 'Person' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Person').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Person' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='firstName').value = 'Juan'
    >>> browser.getControl(name='lastName').value = 'Perez'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Person content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Organization content type
=============================

In this section we are tesing the Organization content type by performing
basic operations like adding, updadating and deleting Organization content
items.

Adding a new Organization content item
--------------------------------------

First let's get inside an Address Book.

    >>> browser.getLink('Address Book Sample').click()

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Organization' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Organization').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Organization' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Organization Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Organization' content item to the portal.

Updating an existing Organization content item
----------------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Organization Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Organization Sample' in browser.contents
    True

Removing a/an Organization content item
---------------------------------------

If we go to the address book, we can see an item with the 'New Organization
Sample' title.

    >>> browser.open(portal_url)
    >>> browser.getLink('Address Book Sample').click()
    >>> 'New Organization Sample' in browser.contents
    True

Now we are going to delete the 'New Organization Sample' object. First we
go to the contents tab and select the 'New Organization Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Organization Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Organization
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Organization Sample' in browser.contents
    False

Adding a new Organization content item as contributor
-----------------------------------------------------

Not only site managers are allowed to add Organization content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Address Book Sample').click()
    >>> browser.getLink('Add new').click()

We select 'Organization' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Organization').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Organization' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Organization Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Organization content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Group content type
======================

In this section we are tesing the Group content type by performing
basic operations like adding, updadating and deleting Organization content
items.

Adding a new Group content item
--------------------------------

First let's get inside an Address Book.

    >>> browser.getLink('Address Book Sample').click()

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Organization' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Group').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Organization' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Group Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Group' content item to the portal.

Updating an existing Group content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Group Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Group Sample' in browser.contents
    True

Removing a Group content item
-----------------------------

If we go to the address book, we can see an item with the 'New Group Sample'
title.

    >>> browser.open(portal_url)
    >>> browser.getLink('Address Book Sample').click()
    >>> 'New Group Sample' in browser.contents
    True

Now we are going to delete the 'New Group Sample' object. First we go to the
contents tab and select the 'New Group Sample' for deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Group Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Group Sample'
tab.

    >>> browser.open(portal_url)
    >>> 'New Group Sample' in browser.contents
    False

Adding a new Group content item as contributor
----------------------------------------------

Not only site managers are allowed to add Group content items, but also site
contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Address Book Sample').click()
    >>> browser.getLink('Add new').click()

We select 'Group' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Group').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Organization' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Group Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Group content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)
		
Test the names of the view are correct
--------------------------------------
Let's add more persons

	>>> browser.open(portal_url)
	>>> browser.getLink('Address Book Sample').click()
	>>> browser.getLink('Add new').click()
	>>> browser.getControl('Person').click()
	>>> browser.getControl(name='form.button.Add').click()
	>>> 'Person' in browser.contents
	True
	>>> browser.getControl(name='firstName').value = 'name1'
	>>> browser.getControl(name='lastName').value = 'last1'
	>>> browser.getControl(name='email').value = 'name1@mail.com'
	>>> browser.getControl('Save').click()
	>>> 'Changes saved' in browser.contents
	True

this one do not have no e-mail

    >>> browser.open(portal_url)
	>>> browser.getLink('Address Book Sample').click()
    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Person').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Person' in browser.contents
    True
    >>> browser.getControl(name='firstName').value = 'name2'
    >>> browser.getControl(name='lastName').value = 'last2'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
	True

Let's add more organizations

	>>> browser.getLink('Address Book Sample').click()
	>>> browser.getLink('Add new').click()
	>>> browser.getControl('Organization').click()
	>>> browser.getControl(name='form.button.Add').click()
	>>> 'Organization' in browser.contents
	True
	>>> browser.getControl(name='title').value = 'Organization1'
	>>> browser.getControl(name='email').value = 'Org@mail.com'
	>>> browser.getControl('Save').click()
	>>> 'Changes saved' in browser.contents
	True

this one with out an email

	>>> browser.getLink('Address Book Sample').click()
	>>> browser.getLink('Add new').click()
	>>> browser.getControl('Organization').click()
	>>> browser.getControl(name='form.button.Add').click()
	>>> 'Organization' in browser.contents
	True
	>>> browser.getControl(name='title').value = 'Organization2'
	>>> browser.getControl('Save').click()
	>>> 'Changes saved' in browser.contents
	True

Checking the organization view is called organizations

    >>> browser.open(portal_url)
	>>> browser.getLink('Address Book Sample').click()
	>>> view_org_url = browser.url +"/organizations"
	>>> browser.open(view_org_url)
	>>> "Organization Sample" in browser.contents
	True
	>>> "Organization1" in browser.contents
	True
	>>> "Organization2" in browser.contents
	True



Checking the persons view is called persons

    >>> browser.open(portal_url)
	>>> browser.getLink('Address Book Sample').click()
	>>> view_pers_url = browser.url +"/persons"
	>>> browser.open(view_pers_url)
	>>> "juan" in browser.contents
	True
	>>> "name1" in browser.contents
	True
	>>> "name2" in browser.contents
	True


Checking the groups view is called groups

    >>> browser.open(portal_url)
	>>> browser.getLink('Address Book Sample').click()
	>>> view_group_url = browser.url +"/groups"
	>>> browser.open(view_group_url)
	>>> "Group Sample" in browser.contents
	True


Send mail to persons
--------------------

Send mail to persons with email


	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'Send emails' in browser.contents
	True
	>>> 'name1@mail.com' in browser.contents
	True
	>>> 'test@test.com' in browser.contents
	False
	
Sending mail with out choosing a person

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'You need to select at least one person or organization' in browser.contents
	True
	
Sending mail to a person without an email

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='no_mail').value = ['last2-name2 ']
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'You need to select at least one person or organization that has an email' in browser.contents
	True
	
Sending mails to a person with an email and one without an email

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='no_mail').value = ['last2-name2 ']
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'Send emails' in browser.contents
	True
	>>> 'name1@mail.com' in browser.contents
	True


Send mail to organizations
--------------------------

Send mail to organizations with email

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'Send emails' in browser.contents
	True
	>>> 'Org@mail.com' in browser.contents
	True

Sending mail with out choosing an organization

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'You need to select at least one person or organization' in browser.contents
	True

Sending mail to an organization without an email

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='no_mail').value = ['organization2 ']
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'You need to select at least one person or organization that has an email' in browser.contents
	True
	
Sending mails to an organization with an email and one without an email

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='no_mail').value = ['organization2 ']
	>>> browser.getControl(name='form.button.mailto').click()
	>>> 'Send emails' in browser.contents
	True
	>>> 'Org@mail.com' in browser.contents
	True


Test export file persons
------------------------

persons with email
------------------

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='form.button.export_persons',index=0).click()
	
check the headers

	>>> "id,short_name,first_name,last_name,organization,position" in browser.contents 
	True
	>>> "department,work_phone,work_mobile_phone,work_email,work_email2," in browser.contents
	True
	>>> "work_email3,address,country,state,city,phone,mobile_phone,email,web,text" in browser.contents
	True
	
check some of the data

	>>> 'last1-name1' in browser.contents
	True
	>>> 'name1@mail.com' in browser.contents
	True

persons without an email
------------------------

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='no_mail').value = ['last2-name2 ']
	>>> browser.getControl(name='form.button.export_persons',index=0).click()

check the headers

	>>> "id,short_name,first_name,last_name,organization,position" in browser.contents 
	True
	>>> "department,work_phone,work_mobile_phone,work_email,work_email2," in browser.contents
	True
	>>> "work_email3,address,country,state,city,phone,mobile_phone,email,web,text" in browser.contents
	True

check some of the data

	>>> 'last2-name2' in browser.contents
	True


persons with and without an email
---------------------------------

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='no_mail').value = ['last2-name2 ']
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='form.button.export_persons',index=0).click()

check the headers

	>>> "id,short_name,first_name,last_name,organization,position" in browser.contents 
	True
	>>> "department,work_phone,work_mobile_phone,work_email,work_email2," in browser.contents
	True
	>>> "work_email3,address,country,state,city,phone,mobile_phone,email,web,text" in browser.contents
	True

check some of the data

	>>> 'last1-name1' in browser.contents
	True
	>>> 'name1@mail.com' in browser.contents
	True
	>>> 'last2-name2' in browser.contents
	True

without choosing a person
-------------------------

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='form.button.export_persons',index=0).click()
	>>> 'You need to select at least one person or organization' in browser.contents
	True


export all persons
------------------

	>>> browser.open(view_pers_url)
	>>> browser.getControl(name='form.button.export_persons',index=1).click()

check the headers

	>>> "id,short_name,first_name,last_name,organization,position" in browser.contents 
	True
	>>> "department,work_phone,work_mobile_phone,work_email,work_email2," in browser.contents
	True
	>>> "work_email3,address,country,state,city,phone,mobile_phone,email,web,text" in browser.contents
	True

check some of the data

	>>> 'perez-juan' in browser.contents
	True
	>>> 'last1-name1' in browser.contents
	True
	>>> 'name1@mail.com' in browser.contents
	True
	>>> 'last2-name2' in browser.contents
	True


Test export file organizations
------------------------------

organizations with email
------------------------

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='form.button.export_org',index=0).click()

check the headers

	>>> "id,title,address,city,zip,country,state,extra_address,phone,fax,email" in browser.contents
	True
	>>> "email2,email3,web,sector,sub_sector,text" in browser.contents
	True

check some of the data

	>>> 'organization1' in browser.contents
	True
	>>> 'Org@mail.com' in browser.contents
	True

organizations without an email
------------------------

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='no_mail').value = ['organization2 ']
	>>> browser.getControl(name='form.button.export_org',index=0).click()

check the headers

	>>> "id,title,address,city,zip,country,state,extra_address,phone,fax,email" in browser.contents
	True
	>>> "email2,email3,web,sector,sub_sector,text" in browser.contents
	True

check some of the data

	>>> 'organization2' in browser.contents
	True


organizations with and without an email
---------------------------------

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='no_mail').value = ['organization2 ']
	>>> browser.getControl(name='user_selection:list').value = [1]
	>>> browser.getControl(name='form.button.export_org',index=0).click()

check the headers

	>>> "id,title,address,city,zip,country,state,extra_address,phone,fax,email" in browser.contents
	True
	>>> "email2,email3,web,sector,sub_sector,text" in browser.contents
	True

check some of the data

	>>> 'organization1' in browser.contents
	True
	>>> 'Org@mail.com' in browser.contents
	True
	>>> 'organization2' in browser.contents
	True

without choosing an organization
--------------------------------

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='form.button.export_org',index=0).click()
	>>> 'You need to select at least one person or organization' in browser.contents
	True


export all organizations
------------------------

	>>> browser.open(view_org_url)
	>>> browser.getControl(name='form.button.export_org',index=1).click()

check the headers


	>>> "id,title,address,city,zip,country,state,extra_address,phone,fax,email" in browser.contents
	True
	>>> "email2,email3,web,sector,sub_sector,text" in browser.contents
	True

check some of the data

	>>> 'organization1' in browser.contents
	True
	>>> 'Org@mail.com' in browser.contents
	True
	>>> 'organization2' in browser.contents
	True
	
Import persons
---------------

    >>> #import_view = portal_url + "/import_view"
    >>> #browser.open(import_view)
    >>> #browser.getControl(name='import_selection').value = ['persons']
    >>> #import os
    >>> #input = open('user.csv', 'rb')
    >>> #control = browser.getControl(name='import_file')
    >>> #file_control = control.mech_control
    >>> #file_control.add_file(input,'text/plain', 'test.csv')
    >>> #browser.getControl(name='submit').click()
    >>> #'1 successfuly imported persons' in browser.contents

for a reason is not reading the file correctly, but if it's done throw the web works
