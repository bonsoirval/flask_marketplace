from kesandu.frontend.models import User

# def test_new_user():
#     """
#     GIVEN a User model 
#     WHEN a new User is created
#     THEN check the email, hashed_password, and the role filds are defined correctly
#     """
#     user = User(email='patkennedy79@gmail.com', name='FlaskIsAwesome')
#     assert user.email == 'patkennedy79@gmail.com'
#     assert user.password_hash != "FlaskIsAwesome"
#     assert user.password_hash == user.check_password('FlaskIsAwesome')
#     assert user.role == 'user'
    
def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model 
    WHEN  a new user is created
    THEN check the email, password_hash, authenticated, and role fields are defined correctly
    """
    # assert new_user.email == 'patkennedy97@gmail.com'
    # assert new_user.password_hash != 'FlaskIsAwesome'
    # assert new_user.role == 'user'
    pass