from django.test import TestCase, Client
from django.urls import reverse
from account_controller.models import AdminAccount


class AccountTestViews(TestCase):

    def setUp(self):

        self.client = Client()

        self.account_url = reverse('account')
        self.add_url = reverse('add')
        self.delete_url = reverse('delete')

        self.account1 = AdminAccount.objects.create(identifier='admin1')
    def test_manage_accounts_GET(self):

        response = self.client.get(reverse(self.account_url))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')

    def test_add_accounts_POST_add_new_admin(self):

        initial_count = AdminAccount.objects.count()

        response = self.client.post(self.add_url, {
            'identifier': self.account1.identifier})

        new_count = AdminAccount.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_count, initial_count + 1)

    def test_add_accounts_POST_no_data(self):

        initial_count = AdminAccount.objects.count()

        response = self.client.post(self.add_url)

        new_count = AdminAccount.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_count, initial_count)

    def test_remove_accounts_POST_remove_account(self):

        initial_count = AdminAccount.objects.count()

        response = self.client.post(self.delete_url, {
            'identifier': self.account1.identifier})

        new_count = AdminAccount.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_count, initial_count - 1)

    def test_remove_accounts_POST_no_data(self):

        initial_count = AdminAccount.objects.count()

        response = self.client.post(self.delete_url)

        new_count = AdminAccount.objects.count()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(new_count, initial_count)


