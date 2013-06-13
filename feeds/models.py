from operator import or_

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timesince import timesince


# Make shortcut to this manager method for convenience
ct_get_for_model = ContentType.objects.get_for_model


class Subscription(models.Model):
    """
    To store a subscription to an object for inclusion in a feed

    Basically this model just stores a relation to an object which makes
    the feed start watching this object
    """
    ct = models.ForeignKey(ContentType)
    obj_id = models.PositiveIntegerField()
    c_obj = generic.GenericForeignKey('ct', 'obj_id')

    class Meta:
        app_label = 'feeds'

    def __unicode__(self):
        return '%s: %s' % (self.ct, self.c_obj.name)


class ActivityManager(models.Manager):
    """
    Manager for Activity
    """
    def create(self, actor, verb, obj=None, target=None, *ar, **kw):
        kw.update({
            'actor_c_obj': actor,
            'verb': verb,
            'object_c_obj': obj,
            'target_c_obj': target
        })
        for k, v in kw.items():
            if not v:
                kw.pop(k)
        return super(ActivityManager, self).create(*ar, **kw)


class Activity(models.Model):
    """
    To store a single activity
    """
    published = models.DateTimeField(default=timezone.now)

    actor_ct = models.ForeignKey(ContentType, related_name='as_actor')
    actor_obj_id = models.PositiveIntegerField()
    actor_c_obj = generic.GenericForeignKey('actor_ct', 'actor_obj_id')

    verb = models.CharField(max_length=100)

    object_ct = models.ForeignKey(
        ContentType,
        related_name='as_object',
        blank=True,
        null=True
    )
    object_obj_id = models.PositiveIntegerField(blank=True, null=True)
    object_c_obj = generic.GenericForeignKey('object_ct', 'object_obj_id')

    target_ct = models.ForeignKey(
        ContentType,
        related_name='as_target',
        blank=True,
        null=True
    )
    target_obj_id = models.PositiveIntegerField(blank=True, null=True)
    target_c_obj = generic.GenericForeignKey('target_ct', 'target_obj_id')

    objects = ActivityManager()

    class Meta:
        app_label = 'feeds'
        ordering = ['-published']

    def save(self, *ar, **kw):
        super(Activity, self).save(*ar, **kw)
        if self.pk:
            self.propagate_activity()

    def __unicode__(self):
        if self.object_c_obj and self.target_c_obj:
            return '%s %s %s on %s %s ago' % (
                self.actor_c_obj,
                self.verb,
                self.object_c_obj,
                self.target_c_obj,
                timesince(self.published)
            )
        elif self.object_c_obj:
            return '%s %s %s %s ago' % (
                self.actor_c_obj,
                self.verb,
                self.object_c_obj,
                timesince(self.published)
            )
        elif self.target_c_obj:
            return '%s %s on %s %s ago' % (
                self.actor_c_obj,
                self.verb,
                self.target_c_obj,
                timesince(self.published)
            )
        else:
            return '%s %s %s ago' % (
                self.actor_c_obj,
                self.verb,
                timesince(self.published)
            )

    def propagate_activity(self):
        """
        should be run when the Activity is saved then will get
        a set of Feeds that are subscribed to either the actor instance, the
        object instance or the target instance and add the Activity to them
        """
        qs = []
        # we're expecting the actor to always be there so always query on this
        qs.append(
            Q(
                subscriptions__ct=ct_get_for_model(self.actor_c_obj),
                subscriptions__obj_id=self.actor_c_obj.id
            )
        )

        # additional optional instances to filter by
        if self.object_c_obj:
            qs.append(
                Q(
                    subscriptions__ct=ct_get_for_model(self.object_c_obj),
                    subscriptions__obj_id=self.object_c_obj.id
                )
            )
        if self.target_c_obj:
            qs.append(
                Q(
                    subscriptions__ct=ct_get_for_model(self.target_c_obj),
                    subscriptions__obj_id=self.target_c_obj.id
                )
            )
        # create Q() | Q() ...
        q = reduce(or_, qs)
        feeds = Feed.objects.filter(q)
        for feed in feeds:
            feed.activity.add(self)


# to import and be convenient/helpful elsewhere
add_activity = Activity.objects.create


class Feed(models.Model):
    """
    Just a collection of activities and subscription
    See the propagate_activity method below to learn how activities end up
    here
    """
    subscriptions = models.ManyToManyField(Subscription, blank=True, null=True)
    activity = models.ManyToManyField(Activity, blank=True, null=True)

    class Meta:
        app_label = 'feeds'

    def add_subscription(self, obj):
        try:
            sub = Subscription.objects.get(
                ct=ct_get_for_model(obj),
                obj_id=obj.id
            )
        except Subscription.DoesNotExist:
            sub = Subscription.objects.create(c_obj=obj)
        self.subscriptions.add(sub)

    def add_subscriptions(self, *ar):
        for obj in ar:
            self.add_subscription(obj)
