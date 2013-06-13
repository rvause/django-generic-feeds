from django.test import TestCase
from django.contrib.sites.models import Site

from models import Activity, Feed


class FeedsTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.all()[0]

    def test_activity(self):
        a = Activity.objects.create(
            self.site,
            'sited',
            self.site,
            self.site
        )
        self.assertEqual(
            'example.com sited example.com on example.com 0 minutes ago',
            str(a)
        )

        a = Activity.objects.create(
            self.site,
            'sited',
            self.site,
        )
        self.assertEqual(
            'example.com sited example.com 0 minutes ago',
            str(a)
        )

        a = Activity.objects.create(
            self.site,
            'sited',
            target=self.site
        )
        self.assertEqual(
            'example.com sited on example.com 0 minutes ago',
            str(a)
        )

        a = Activity.objects.create(
            self.site,
            'sited'
        )
        self.assertEqual(
            'example.com sited 0 minutes ago',
            str(a)
        )

    def test_feed(self):
        f = Feed.objects.create()
        site2 = Site.objects.create(domain='test', name='test')
        f.add_subscriptions(self.site, site2)
        self.assertEqual(f.subscriptions.count(), 2)
        a = Activity.objects.create(
            self.site,
            'sited',
            self.site,
            self.site
        )
        self.assertTrue(a in f.activity.all())
