from uploadapi.models import AccountTier, Account
from django.contrib.auth.models import User


def setup_test_env():
    test_tier_basic = AccountTier.objects.create(name='Basic', has_image_link=False, has_expiring_links=False, thumbnail_sizes=[200])
    test_tier_premium = AccountTier.objects.create(name='Premium', has_image_link=True, has_expiring_links=False, thumbnail_sizes=[200, 400])
    test_tier_enterprise = AccountTier.objects.create(name='Enterprise', has_image_link=True, has_expiring_links=True, thumbnail_sizes=[200, 400])


    test_admin = User.objects.create_superuser(username='test_admin', password='asdf4444')
    test_admin_acc = Account.objects.create(user=test_admin, account_tier=test_tier_basic)

    test_user_basic = User.objects.create_user(username='test_user_basic', password='asdf4444')
    test_user_basic_acc = Account.objects.create(user=test_user_basic, account_tier=test_tier_basic)


    test_user_premium = User.objects.create_user(username='test_user_premium', password='asdf4444')
    test_user_premium_acc = Account.objects.create(user=test_user_premium, account_tier=test_tier_premium)


    test_user_enterprise = User.objects.create_user(username='test_user_enterprise', password='asdf4444')
    test_user_enterprise_acc = Account.objects.create(user=test_user_enterprise, account_tier=test_tier_enterprise)



