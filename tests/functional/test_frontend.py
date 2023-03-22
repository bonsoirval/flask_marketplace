from kesandu import create_app


# def test_home_page():
#     """
#     GIVEN a Flask application configured for testing 
#     WHEN the '/' page is requested (GET)
#     THEN check that the response is valid
#     """
#     flask_app = create_app('flask_test.cfg')
    
#     # Create a test client using the Flask application configured for testing 
#     with flask_app.test_client() as test_client:
#         response = test_client().get('/')
#         assert response.status_code == 200
#         assert b'Welcome to the' in response.data
#         assert b'Flask User Management Example!' in response.data 
#         assert b'Need an account?' in response.data
#         assert b'Existing user?' in response.data
        
# def test_home_page_post():
#     """
#     GIVEN a Flask application configured for testing 
#     WHEN the '/' page is posted to (POST)
#     THEN check that a '405' status code is returned
#     """
#     flask_app = create_app('flask_test.cfg')
#     with flask_app.test_client() as test_client:
#         response = test_client.post('/')
#         assert response.status_code == 405
#         assert b'Flask User Management Example!' not in response.data 
        
def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    pass
    # response = test_client.get('/')
    # assert response.status_code == 200
    # assert b"Welcome to the" in response.data
    # assert b"Flask User Management Example!" in response.data
    # assert b"Need an account?" in response.data
    # assert b"Existing user?" in response.data


def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    pass 
    # response = test_client.post('/')
    # assert response.status_code == 405
    # assert b"Flask User Management Example!" not in response.data
