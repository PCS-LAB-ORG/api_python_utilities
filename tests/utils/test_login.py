import json

from apu.utils import logger, login

logger = logger.setup_logger()

def test_with_expired_access_key():
    ''' rotate on failure may be a login flag I want to use '''
    try:
        # using a known expired access_key/secret_key
        # with pytest.raises(HTTPError):
        login.login(credential_name="expired_credentials")
        assert login.headers['Authorization'] == "-1" # remove this line once it is expired
    except Exception as e:
        logger.info(e)

def test_with_deleted_access_key():
    ''' rotate on failure may be a login flag I want to use '''
    try:
        # using a known deleted access_key/secret_key
        login.login(credential_name="deleted_credentials")
    except BaseException as e:
        if e.response.status_code == 401:
            js_res = json.loads(e.response.text)
            assert js_res.get("message") == "invalid_credentials"
            assert e.response.reason == "Unauthorized"

def test_with_inactive():
    ''' rotate on failure may be a login flag I want to use '''
    try:
        # using a known deleted access_key/secret_key
        login.login(credential_name="inactive_credentials")
    except SystemExit as e:
        assert "401" in e.code
        assert "inactive_access_key" in e.code
        
def test_access_key_blank_secret():
    ''' rotate on failure may be a login flag I want to use '''
    try:
        # using a known deleted access_key/secret_key
        login.login(url="https://api2.prismacloud.io/", access_key="", secret_key="")
        # This successfully logs in
    except Exception as e:
        logger.info(e)
        
def test_access_key_no_secret():
    ''' rotate on failure may be a login flag I want to use '''
    # using a known deleted access_key/secret_key
    login.login(url="https://api2.prismacloud.io/", access_key="")
    # This successfully logs in
    assert len(login.headers['identity']) == 13
    
def test_invalid_user_pass():
    ''' rotate on failure may be a login flag I want to use '''
    try:
        # using a known deleted access_key/secret_key
        login.login(url="https://api2.prismacloud.io/", access_key="as", secret_key="asd")
    except BaseException as e:
        if e.response.status_code == 401:
            js_res = json.loads(e.response.text)
            assert js_res.get("message") == "invalid_credentials"
            assert e.response.reason == "Unauthorized"
        # logger.info(e)
