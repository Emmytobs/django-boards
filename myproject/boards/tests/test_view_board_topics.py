from django.urls import resolve, reverse
from django.test import TestCase
from ..views import TopicListView
from ..models import Board

class BoardTopicsTests(TestCase):
    def setUp(self):
        self.python_board = Board.objects.create(name='Python', description='Python board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': self.python_board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        board_url = f"/boards/{self.python_board.pk}/"
        view = resolve(board_url)
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_navigation_links(self):
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': self.python_board.id})
        board_topics_url = reverse('board_topics', kwargs={'pk': self.python_board.pk})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))