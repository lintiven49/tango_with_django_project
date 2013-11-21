from django.test import TestCase
from django.core.urlresolvers import reverse
# Create your tests here.


class ViewTest(TestCase):

    def test_search(self):
        response = self.client.get(reverse('rango:search', args=('test',)))
        print response.content

