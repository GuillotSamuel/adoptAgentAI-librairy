import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from adoptagentai.utils.api_keys import get_api_credentials
from adoptagentai.core.agent import Agent


@pytest.fixture
def mock_api_credentials():
    """Fixture to mock get_api_credentials function"""
    with patch('adoptagentai.core.agent.get_api_credentials') as mock_get:
        mock_get.return_value = {"api_key": "test-api-key"}
        yield mock_get


@pytest.fixture
def mock_logger():
    """Fixture to mock logger"""
    with patch('adoptagentai.core.agent.logging.getLogger') as mock_logger:
        mock_log = MagicMock()
        mock_logger.return_value = mock_log
        yield mock_log


def test_agent_initialization(mock_api_credentials, mock_logger):
    """Test that Agent initializes correctly with default and provided values"""
    # Test with minimal parameters
    agent = Agent(name="TestAgent")
    assert agent.name == "TestAgent"
    assert agent.model_name is None
    assert agent.model_credentials is None
    assert agent.tool_list == []
    assert agent.tool_credentials == {}
    assert agent.memory == []
    mock_logger.info.assert_called_once()
    
    # Test with all parameters
    tools = ["search", "calculator"]
    tool_creds = {"search": {"api_key": "search-key"}}
    memory = [{"data": "test memory", "category": "test", "timestamp": datetime.now()}]
    
    agent = Agent(
        name="FullAgent", 
        model_name="openai", 
        model_account_name="default",
        tool_list=tools,
        tool_credentials=tool_creds,
        memory=memory
    )
    
    assert agent.name == "FullAgent"
    assert agent.model_name == "openai"
    assert agent.model_account_name == "default"
    assert agent.tool_list == tools
    assert agent.tool_credentials == tool_creds
    assert agent.memory == memory
    mock_api_credentials.assert_called_with("openai", "default")


def test_add_tool(mock_logger):
    """Test that add_tool correctly adds a new tool or updates existing ones"""
    agent = Agent(name="TestAgent")
    
    # Add new tool
    agent.add_tool("search", {"api_key": "search-key"})
    assert "search" in agent.tool_list
    assert agent.tool_credentials["search"] == {"api_key": "search-key"}
    mock_logger.info.assert_called_with("Tool 'search' added to the agent.")
    
    # Update existing tool
    mock_logger.warning.assert_not_called()
    agent.add_tool("search", {"api_key": "new-search-key"})
    assert agent.tool_credentials["search"] == {"api_key": "new-search-key"}
    mock_logger.warning.assert_called_with("Tool 'search' already exists. Updating credentials.")


def test_add_memory(mock_logger):
    """Test that add_memory correctly adds memory entries with metadata"""
    agent = Agent(name="TestAgent")
    
    # Add memory without category
    entry = agent.add_memory("Test memory data")
    assert len(agent.memory) == 1
    assert agent.memory[0]["data"] == "Test memory data"
    assert agent.memory[0]["category"] is None
    assert isinstance(agent.memory[0]["timestamp"], datetime)
    mock_logger.info.assert_called()
    
    # Add memory with category
    entry = agent.add_memory("Category test", "test-category")
    assert len(agent.memory) == 2
    assert agent.memory[1]["data"] == "Category test"
    assert agent.memory[1]["category"] == "test-category"
    
    # Test return value
    assert entry["data"] == "Category test"
    assert entry["category"] == "test-category"
    assert isinstance(entry["timestamp"], datetime)


def test_list_tools():
    """Test that list_tools returns the correct tool list"""
    agent = Agent(name="TestAgent", tool_list=["search", "calculator"])
    
    tools = agent.list_tools()
    assert tools == ["search", "calculator"]


def test_retrieve_memory():
    """Test that retrieve_memory returns all or filtered memory entries"""
    now = datetime.now()
    memory = [
        {"data": "test1", "category": "cat1", "timestamp": now},
        {"data": "test2", "category": "cat2", "timestamp": now},
        {"data": "test3", "category": "cat1", "timestamp": now}
    ]
    agent = Agent(name="TestAgent", memory=memory)
    
    # Get all memory
    result = agent.retrieve_memory()
    assert result == memory
    
    # Get filtered memory
    result = agent.retrieve_memory(category="cat1")
    assert len(result) == 2
    assert all(entry["category"] == "cat1" for entry in result)


def test_remove_tool(mock_logger):
    """Test that remove_tool correctly removes tools"""
    agent = Agent(
        name="TestAgent", 
        tool_list=["search", "calculator"],
        tool_credentials={"search": {"api_key": "key1"}, "calculator": {"api_key": "key2"}}
    )
    
    # Remove existing tool
    agent.remove_tool("search")
    assert "search" not in agent.tool_list
    assert "search" not in agent.tool_credentials
    mock_logger.info.assert_called_with("Tool 'search' removed from the agent.")
    
    # Try to remove non-existent tool
    agent.remove_tool("nonexistent")
    mock_logger.warning.assert_called_with("Tool 'nonexistent' not found in the agent.")


def test_clear_memory(mock_logger):
    """Test that clear_memory correctly clears all or filtered memory entries"""
    memory = [
        {"data": "test1", "category": "cat1", "timestamp": datetime.now()},
        {"data": "test2", "category": "cat2", "timestamp": datetime.now()},
        {"data": "test3", "category": "cat1", "timestamp": datetime.now()}
    ]
    agent = Agent(name="TestAgent", memory=memory)
    
    # Clear specific category
    agent.clear_memory(category="cat1")
    assert len(agent.memory) == 1
    assert agent.memory[0]["category"] == "cat2"
    mock_logger.info.assert_called_with("Memory entries with category 'cat1' cleared.")
    
    # Clear all memory
    agent.clear_memory()
    assert len(agent.memory) == 0
    mock_logger.info.assert_called_with("All memory entries cleared.")


@patch('adoptagentai.core.agent.get_api_credentials')
def test_update_model(mock_get_credentials, mock_logger):
    """Test that update_model correctly updates the model configuration"""
    mock_get_credentials.return_value = {"api_key": "new-model-key"}
    
    agent = Agent(name="TestAgent")
    agent.update_model("openai", "prod")
    
    assert agent.model_name == "openai"
    assert agent.model_account_name == "prod"
    assert agent.model_credentials == {"api_key": "new-model-key"}
    mock_get_credentials.assert_called_with("openai", "prod")
    mock_logger.info.assert_called_with("Agent model updated to: openai")
    
    # Test model name gets lowercased
    agent.update_model("OpenAI")
    assert agent.model_name == "openai"