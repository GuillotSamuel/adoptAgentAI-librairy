import os
import pytest
from unittest.mock import patch, MagicMock
from adoptagentai.utils.api_keys import (
    list_api_requirements,
    define_api_credentials,
    get_api_credentials,
    remove_api_credentials,
    list_api_accounts,
    list_configured_apis,
    API_REQUIREMENTS
)


@pytest.fixture
def mock_environ():
    """Fixture to provide a clean environment for each test"""
    with patch.dict(os.environ, {
        "OPENAI_DEFAULT_API_KEY": "test-key",
        "OPENAI_TEST_API_KEY": "test-key-2",
        "OPENAI_PROD_API_KEY": "prod-key",
    }, clear=True):
        yield


@pytest.fixture
def mock_dotenv():
    """Fixture to mock dotenv functions"""
    with patch('adoptagentai.utils.api_keys.find_dotenv') as mock_find:
        with patch('adoptagentai.utils.api_keys.set_key') as mock_set:
            with patch('adoptagentai.utils.api_keys.unset_key') as mock_unset:
                with patch('builtins.open', MagicMock()):
                    mock_find.return_value = ".env"
                    yield mock_find, mock_set, mock_unset


def test_list_api_requirements():
    """Test that list_api_requirements returns the correct dictionary"""
    requirements = list_api_requirements()
    assert requirements == API_REQUIREMENTS
    assert "gpt-4o" in requirements
    assert "api_key" in requirements["gpt-4o"]


def test_define_api_credentials(mock_dotenv):
    """Test that define_api_credentials correctly sets credentials"""
    mock_find, mock_set, _ = mock_dotenv
    
    # Test with valid API and credentials
    result = define_api_credentials("gpt-4o", "test", api_key="test-key")
    assert result is True
    mock_set.assert_called_once_with('.env', 'GPT-4O_TEST_API_KEY', 'test-key')
    
    # Test with unsupported API
    with pytest.raises(ValueError) as excinfo:
        define_api_credentials("unsupported", "test", api_key="test-key")
    assert "API unsupported not supported" in str(excinfo.value)
    
    # Test with missing credentials
    with pytest.raises(ValueError) as excinfo:
        define_api_credentials("gpt-4o", "test")
    assert "Missing required credentials" in str(excinfo.value)


def test_define_api_credentials_no_dotenv(mock_dotenv):
    """Test define_api_credentials when no .env file exists"""
    mock_find, mock_set, _ = mock_dotenv
    mock_find.return_value = ""
    
    result = define_api_credentials("gpt-4o", "test", api_key="test-key")
    assert result is True
    mock_set.assert_called_once_with('.env', 'GPT-4O_TEST_API_KEY', 'test-key')


def test_get_api_credentials(mock_environ):
    """Test that get_api_credentials returns the correct credentials"""
    # Test with valid API and account
    credentials = get_api_credentials("gpt-4o", "default")
    assert credentials == {"api_key": "test-key"}
    
    # Test with valid API and different account
    credentials = get_api_credentials("gpt-4o", "test")
    assert credentials == {"api_key": "test-key-2"}
    
    # Test with unsupported API
    with pytest.raises(ValueError) as excinfo:
        get_api_credentials("unsupported", "default")
    assert "API unsupported not supported" in str(excinfo.value)
    
    # Test with non-existent account
    credentials = get_api_credentials("gpt-4o", "nonexistent")
    assert credentials == {}


def test_remove_api_credentials(mock_environ, mock_dotenv):
    """Test that remove_api_credentials correctly removes credentials"""
    _, _, mock_unset = mock_dotenv
    
    # Test with valid API and account
    result = remove_api_credentials("gpt-4o", "default")
    assert result is True
    mock_unset.assert_called_once_with(".env", "GPT-4O_DEFAULT_API_KEY")
    
    # Test with unsupported API
    with pytest.raises(ValueError) as excinfo:
        remove_api_credentials("unsupported", "default")
    assert "API unsupported not supported" in str(excinfo.value)
    
    # Test with non-existent account
    with patch.dict(os.environ, {}, clear=True):
        result = remove_api_credentials("gpt-4o", "nonexistent")
        assert result is False


def test_remove_api_credentials_no_dotenv(mock_environ, mock_dotenv):
    """Test remove_api_credentials when no .env file exists"""
    mock_find, _, _ = mock_dotenv
    mock_find.return_value = ""
    
    result = remove_api_credentials("gpt-4o", "default")
    assert result is False


def test_list_api_accounts(mock_environ):
    """Test that list_api_accounts returns the correct list of accounts"""
    # Test with valid API
    accounts = list_api_accounts("gpt-4o")
    assert set(accounts) == {"DEFAULT", "TEST", "PROD"}
    
    # Test with unsupported API
    with pytest.raises(ValueError) as excinfo:
        list_api_accounts("unsupported")
    assert "API unsupported not supported" in str(excinfo.value)
    
    # Test with no accounts
    with patch.dict(os.environ, {}, clear=True):
        accounts = list_api_accounts("gpt-4o")
        assert accounts == []


def test_list_configured_apis(mock_environ):
    """Test that list_configured_apis returns the correct list of APIs"""
    # Test with configured APIs
    apis = list_configured_apis()
    assert apis == ["gpt-4o"]
    
    # Test with no configured APIs
    with patch.dict(os.environ, {}, clear=True):
        apis = list_configured_apis()
        assert apis == []


def test_case_insensitivity():
    """Test that API names and credential keys are case-insensitive"""
    with patch.dict(os.environ, {
        "GPT-4O_DEFAULT_API_KEY": "test-key",
    }, clear=True):
        # Test with uppercase API name
        credentials = get_api_credentials("GPT-4O", "default")
        assert credentials == {"api_key": "test-key"}
        
        # Test with mixed-case API name
        credentials = get_api_credentials("gpt-4o", "default")
        assert credentials == {"api_key": "test-key"}
    
    with patch('adoptagentai.utils.api_keys.set_key') as mock_set:
        with patch('adoptagentai.utils.api_keys.find_dotenv', return_value=".env"):
            # Test with uppercase credential key
            result = define_api_credentials("gpt-4o", "test", API_KEY="test-key")
            assert result is True
            mock_set.assert_called_once_with('.env', 'GPT-4O_TEST_API_KEY', 'test-key')
