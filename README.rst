====================
django-generic-feeds
====================

A simple way for objects to subscribe to other objects for a "feed-like"
functionality in a Django project.

You can use django-generic-feeds to create "feeds" for that can subscribe to
other objects and then list activity that happen on those objects. For example
you may wish for your users to have a feed with subscriptions to other users
to create an activity stream for users for a primitive Twitter clone.


.. image:: https://travis-ci.org/rvause/django-generic-feeds.png?branch=master


Installation
============

``pip install django-generic-feeds``

or

Run ``setup.py install`` or add to your Python path.


You will need to include ``'feeds'`` in your ``INSTALLED_APPS`` setting.


Usage
=====

Make a new feed::

    from feeds.models import Feed

    feed = Feed.objects.create()


Add a subscription to a feed::

    from myapp.models import Event

    event = Event.objects.get(pk=36)
    feed.add_subscription(event)


Then you can add an activity::

    from feeds.models import add_activity

    add_activity(actor=request.user, verb='attended', obj=event)


Then the feed's activity will be populated with this activity::

    print feed.activity.all()


See the source code for more.


Running Tests
=============

To run the tests::

    python setup.py test


Need Help?
==========

Email: rvause@gmail.com

Github: https://github.com/rvause/django-generic-feeds
