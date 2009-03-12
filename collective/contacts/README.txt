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
    >>> browser.getControl(name='organization').value = 'Department'
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
