from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Message

# Author: Student 3 - Tawfiq

User = get_user_model()

class MessagingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@sky.com',
            password='TestPass123!'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@sky.com',
            password='TestPass123!'
        )

    def test_send_message(self):
        self.client.login(username='testuser1', password='TestPass123!')
        response = self.client.post(reverse('compose'), {
            'recipients': [self.user2.pk],
            'subject': 'Test Subject',
            'body': 'Test Body',
            'send': True
        })
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().subject, 'Test Subject')

    def test_message_appears_in_inbox(self):
        message = Message.objects.create(
            sender=self.user1,
            subject='Inbox Test',
            body='Test body',
            is_draft=False
        )
        message.recipients.add(self.user2)
        self.client.login(username='testuser2', password='TestPass123!')
        response = self.client.get(reverse('inbox'))
        self.assertContains(response, 'Inbox Test')

    def test_draft_not_in_inbox(self):
        message = Message.objects.create(
            sender=self.user1,
            subject='Draft Test',
            body='Test body',
            is_draft=True
        )
        message.recipients.add(self.user2)
        self.client.login(username='testuser2', password='TestPass123!')
        response = self.client.get(reverse('inbox'))
        self.assertNotContains(response, 'Draft Test')

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse('inbox'))
        self.assertRedirects(response, '/accounts/login/?next=/messaging/')

    def test_empty_subject_fails(self):
        self.client.login(username='testuser1', password='TestPass123!')
        response = self.client.post(reverse('compose'), {
            'recipients': [self.user2.pk],
            'subject': '',
            'body': 'Test Body',
            'send': True
        })
        self.assertEqual(Message.objects.count(), 0)

    def test_message_marked_read_when_opened(self):
        message = Message.objects.create(
            sender=self.user1,
            subject='Read Test',
            body='Test body',
            is_draft=False,
            is_read=False
        )
        message.recipients.add(self.user2)
        self.client.login(username='testuser2', password='TestPass123!')
        self.client.get(reverse('view_message', args=[message.pk]))
        message.refresh_from_db()
        self.assertTrue(message.is_read)

    def test_save_draft(self):
        self.client.login(username='testuser1', password='TestPass123!')
        response = self.client.post(reverse('compose'), {
            'recipients': [self.user2.pk],
            'subject': 'My Draft',
            'body': 'Draft body',
            'save_draft': True
        })
        self.assertEqual(Message.objects.filter(is_draft=True).count(), 1)

    def test_sent_messages_appear_in_sent(self):
        message = Message.objects.create(
            sender=self.user1,
            subject='Sent Test',
            body='Test body',
            is_draft=False
        )
        message.recipients.add(self.user2)
        self.client.login(username='testuser1', password='TestPass123!')
        response = self.client.get(reverse('sent'))
        self.assertContains(response, 'Sent Test')