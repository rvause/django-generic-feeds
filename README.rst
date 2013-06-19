====================
django-generic-feeds
====================

A simple way for objects to subscribe to other objects for a "feed-like"
functionality in a Django project.

.. image:: https://travis-ci.org/rvause/django-generic-feeds.png?branch=master


Installation
============

``pip install django-generic-feeds``

or

Run ``setup.py install`` or add to your Python path and include ``'feeds'``
in your ``INSTALLED_APPS`` setting.


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


Need Help?
==========

Email: rvause@gmail.com

Github: https://github.com/rvause/django-generic-feeds
