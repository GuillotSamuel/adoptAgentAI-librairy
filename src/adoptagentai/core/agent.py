import logging
from datetime import datetime
from adoptagentai.utils.api_keys import get_api_credentials
import adoptagentai.core.modelStrategies as modelStrategies

class Agent:
    def __init__(self, name: str = None, model_name: str = None, model_account_name: str = None, tool_list: list = None, tool_credentials: dict = None, memory: list = None):
        """Initialize an AI agent with optional model and tool configuration."""
        # Agent general
        self.name = name
        
        # Retrieval Model
        self.model_name = model_name if model_name else None
        self.model_account_name = model_account_name
        self.model_credentials = get_api_credentials(self.model_name, self.model_account_name) if model_name else None
        self.strategies = {
            "gpt-4o": modelStrategies.gpt_4o_strategy,
            "gpt-4o-mini": modelStrategies.gpt_4o_mini_strategy,
        }
        
        # Tools
        self.tool_list = tool_list if tool_list else []
        self.tool_credentials = tool_credentials if tool_credentials else {}
        
        # Memory
        self.memory = memory if memory else []
        
        # Logging configuration
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        self.logger.info(f"Agent '{name}' initialized with model: {model_name}")
        
    
    def add_tool(self, tool_name: str, tool_credentials: dict) -> None:
        """Add a tool to the agent with its credentials."""
        if tool_name in self.tool_list:
            self.logger.warning(f"Tool '{tool_name}' already exists. Updating credentials.")
            self.tool_credentials[tool_name] = tool_credentials
        else:
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
        
    
    def run_agent(self, prompt: str) -> str:
        """Execute the agent by generating a response from the configured model."""
        print(f"model name {self.model_name}, model account name {self.model_account_name}, model credentials {self.model_credentials}") # TEST
        if not self.model_name or not self.model_account_name or not self.model_credentials:
            self.logger.error("No model configured for execution.")
            return "Error: No model configured."

        try:
            for key, strategy in self.strategies.items():
                if key in self.model_name:
                    response = strategy(self.model_name, prompt, self.model_credentials)
                    self.logger.info(f"Model '{self.model_name}' executed successfully.")
                    return response

        except Exception as e:
            self.logger.error(f"Error executing model: {e}")
            return "Error executing model."
    