import os
from dotenv import set_key, find_dotenv, unset_key, load_dotenv


API_REQUIREMENTS = {
    "openai": ["api_key"]
}


def list_api_requirements() -> dict:
    """
    Returns the required credentials for each supported API.
    
    Returns:
        dict: A dictionary mapping API names to required credential keys.
    """
    return API_REQUIREMENTS


def define_api_credentials(api_name: str, account_name: str = "default", **credentials) -> bool:
    """
    Stores API credentials in the .env file.
    
    Args:
        api_name (str): The name of the API.
        account_name (str, optional): The account identifier. Defaults to "default".
        **credentials: Key-value pairs of credentials.
        
    Returns:
        bool: True if credentials were stored successfully.
        
    Raises:
        ValueError: If the API is not supported or required credentials are missing.
    """
    api_name = api_name.lower()
    
    if api_name not in API_REQUIREMENTS:
        raise ValueError(f"API {api_name} not supported.")
    
    required_credentials = [cred.lower() for cred in API_REQUIREMENTS[api_name]]
    provided_credentials = {k.lower(): v for k, v in credentials.items()}

    missing_credentials = set(required_credentials) - set(provided_credentials.keys())
    
    if missing_credentials:
        raise ValueError(f"Missing required credentials for {api_name}: {', '.join(missing_credentials)}")

    dotenv_path = find_dotenv()
    if not dotenv_path:
        dotenv_path = '.env'
        with open(dotenv_path, 'a'):
            pass

    for key, value in provided_credentials.items():
        env_key = f"{api_name.upper()}_{account_name.upper()}_{key.upper()}"
        set_key('.env', env_key, value)

    return True


def get_api_credentials(api_name: str, account_name: str = "default") -> dict:
    """
    Retrieves API credentials from environment variables.
    
    Args:
        api_name (str): The name of the API.
        account_name (str, optional): The account identifier. Defaults to "default".
        
    Returns:
        dict: The retrieved credentials.
        
    Raises:
        ValueError: If the API is not supported.
    """
    api_name = api_name.lower()
    
    load_dotenv()
    
    if api_name not in API_REQUIREMENTS:
        raise ValueError(f"API {api_name} not supported.")
    
    prefix = f"{api_name.upper()}_{account_name.upper()}"
    
    credentials = {}
    for key in os.environ:
        if key.startswith(prefix):
            cred_type = key[len(prefix) + 1:].lower()
            credentials[cred_type] = os.getenv(key)


    return credentials


def remove_api_credentials(api_name: str, account_name: str = "default") -> bool:
    """
    Removes API credentials from the .env file.
    
    Args:
        api_name (str): The name of the API.
        account_name (str, optional): The account identifier. Defaults to "default".
        
    Returns:
        bool: True if any credentials were removed, False otherwise.
        
    Raises:
        ValueError: If the API is not supported.
    """
    api_name = api_name.lower()
    
    load_dotenv()
    
    if api_name not in API_REQUIREMENTS:
        raise ValueError(f"API {api_name} not supported.")
    
    prefix = f"{api_name.upper()}_{account_name.upper()}"

    dotenv_path = find_dotenv()
    if not dotenv_path:
        return False
    
    removed = False
    for key in list(os.environ.keys()):
        if key.startswith(prefix):
            unset_key(dotenv_path, key)
            del os.environ[key]
            removed = True
    
    load_dotenv()
    
    return removed


def list_api_accounts(api_name: str) -> list:
    """
    Lists all accounts defined for a given API.
    
    Args:
        api_name (str): The name of the API.
        
    Returns:
        list: A list of account names.
        
    Raises:
        ValueError: If the API is not supported.
    """
    api_name = api_name.lower()
    
    load_dotenv()
    
    if api_name not in API_REQUIREMENTS:
        raise ValueError(f"API {api_name} not supported.")
    
    prefix = f"{api_name.upper()}_"
    
    accounts = set()
    for key in os.environ:
        if key.startswith(prefix):
            parts = key.split('_')
            if len(parts) > 1:
                accounts.add(parts[1])
                
    return list(accounts)


def list_configured_apis() -> list:
    """
    Returns a list of all APIs that have at least one set of credentials configured.
    
    Returns:
        list: Names of APIs with configured credentials.
    """
    configured_apis = set()
    
    load_dotenv()
    
    for key in os.environ:
        parts = key.split('_')
        if len(parts) >= 3 and parts[0] in [api.upper() for api in API_REQUIREMENTS]:
            configured_apis.add(parts[0].lower())
    
    return list(configured_apis)
