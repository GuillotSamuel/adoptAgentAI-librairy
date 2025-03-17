import logging
from datetime import datetime
from adoptagentai.utils.api_keys import get_api_credentials

class Agent:
    def __init__(self, name: str = None, model_name: str = None, model_account_name: str = None):
        """Initialize an AI agent with optional model and tool configuration."""
        # Agent general
        self.name = name
        
        # Retrieval Model
        self.model_name = model_name.lower() if model_name else None
        self.model_account_name = model_account_name
        self.model_credentials = get_api_credentials(self.model_name, self.model_account_name) if model_name else None
        
        # Tools
        self.tool_list = []
        self.tool_credentials = {}
        
        # Memory
        self.memory = []
        
        # Logging configuration
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        self.logger.info(f"Agent '{name}' initialized with model: {model_name}")
        
    
    def add_tool(self, tool_name: str, tool_credentials: dict) -> None:
        """Add a tool to the agent with its credentials."""
        self.tool_list.append(tool_name)
        self.tool_credentials[tool_name] = tool_credentials
        self.logger.info(f"Tool '{tool_name}' added to the agent.")
        
    
    def add_memory(self, data: str, category: str = None) -> dict:
        """Add data with metadata to the agent's memory."""
        memory_entry = {
            'data': data,
            'category': category,
            'timestamp': datetime.now()
        }
        self.memory.append(memory_entry)
        self.logger.info(f"Memory updated with: {data[:50]}{'...' if len(data) > 50 else ''}, Category: {category}")
        return memory_entry

    
    def list_tools(self) -> list:
        """List the tools the agent has."""
        return self.tool_list
    
    
    def retrieve_memory(self, category: str = None):
        """Retrieve the agent's memory, optionally filtered by category."""
        if category:
            return [entry for entry in self.memory if entry['category'] == category]
        return self.memory
    
    
    def remove_tool(self, tool_name: str) -> None:
        """Remove a tool from the agent."""
        if tool_name in self.tool_list:
            self.tool_list.remove(tool_name)
            del self.tool_credentials[tool_name]
            self.logger.info(f"Tool '{tool_name}' removed from the agent.")
        else:
            self.logger.warning(f"Tool '{tool_name}' not found in the agent.")
            
            
    def clear_memory(self, category: str = None):
        """Clear agent's memory, optionally filtered by category."""
        if category:
            self.memory = [entry for entry in self.memory if entry['category'] != category]
            self.logger.info(f"Memory entries with category '{category}' cleared.")
        else:
            self.memory = []
            self.logger.info("All memory entries cleared.")


    def update_model(self, model_name: str, model_account_name: str = None):
        """Update the agent's model configuration."""
        self.model_name = model_name.lower() if model_name else None
        self.model_account_name = model_account_name
        self.model_credentials = get_api_credentials(self.model_name, self.model_account_name)
        self.logger.info(f"Agent model updated to: {model_name}")