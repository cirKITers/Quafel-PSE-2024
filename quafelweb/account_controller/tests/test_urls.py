#from django.test import SimpleTestCase
#from django.urls import reverse, resolve
#from account_controller import AccountView

#class AccountTestUrls(SimpleTestCase):
    #def test_add_url_is_resolved(self):
     #   url = reverse('add')
      #  print(resolve(url))
        #self.assertEquals(resolve(url).func, AccountView.manage_accounts)

    #def test_delete_url_is_resolved(self):
     #   url = reverse('delete')
      #  print(resolve(url))
        #self.assertEquals(resolve(url).func, AccountView.remove_admin)

    #def test_login_url_is_resolved(self):
     #   url = reverse('login')
      #  print(resolve(url))
        #self.assertEquals(resolve(url).func, AccountView.authenticate)

    #def test_logout_url_is_resolved(self):
     #   url = reverse('logout')
      #  print(resolve(url))
        #self.assertEquals(resolve(url).func, AccountView.logout)

  #  def test_auth_url_is_resolved(self):
   #     url = reverse('auth')
    #    print(resolve(url))
        #self.assertEquals(resolve(url).func, AccountView.authenticate_callback)

    #def test_denied_url_is_resolved(self):
     #   url = reverse('denied')
      #  print(resolve(url))
        #self.assertEquals(resolve(url).func, AccountView.denied)