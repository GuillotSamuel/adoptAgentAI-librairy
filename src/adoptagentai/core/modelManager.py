import logging
from typing import Dict, List, Any, Optional, Union


class ModelManager:
    def __init__(self, model_name: str = None, credentials: dict = None):
        """Initialize the model manager with a model name and credentials."""
        self.model_name = model_name
        self.credentials = credentials
        self.client = self._initialize_client()
        self.logger = logging.getLogger(__name__)


    def _initialize_client(self):
        """Initialize the appropriate client based on the model name."""
        if not self.model_name:
            return None
        try:
            from openai import OpenAI
            return OpenAI(api_key=self.credentials.get('api_key'))
        except ImportError:
            self.logger.error("OpenAI package not installed. Please run 'pip install openai'")
            raise


    def generate(self, prompt: str, system_message: str = None, 
                 max_tokens: int = 1000, temperature: float = 0.7, 
                 chat_history: List[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate a response using the configured model.
        
        Args:
            prompt: The user prompt or query
            system_message: Optional system message to set context
            max_tokens: Maximum number of tokens in the response
            temperature: Controls randomness (0 = deterministic, 1 = creative)
            chat_history: List of previous messages in the conversation
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dictionary containing the response and additional information
        """
        if not self.client:
            raise ValueError("No client initialized. Make sure model_name and credentials are provided.")
        
        if "openai" in self.model_name.lower():
            return self._generate_openai(prompt, system_message, max_tokens, temperature, chat_history, **kwargs)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
        
    
    def _generate_openai(self, prompt: str, system_message: str = None, 
                        max_tokens: int = 1000, temperature: float = 0.7, 
                        chat_history: List[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """Generate a response using OpenAI's API."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        if chat_history:
            messages.extend(chat_history)
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            model = kwargs.get("model", "gpt-4o")
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **{k: v for k, v in kwargs.items() if k not in ['model']}
            )
            
            return {
                    "content": completion.choices[0].message.content,
                    "model": model,
                    "finish_reason": completion.choices[0].finish_reason,
                    "usage": {
                        "prompt_tokens": completion.usage.prompt_tokens,
                        "completion_tokens": completion.usage.completion_tokens,
                        "total_tokens": completion.usage.total_tokens
                    }
                }
        
        except Exception as e:
            self.logger.error(f"Error generating OpenAI response: {str(e)}")
            return {"error": str(e)}


    def stream_generate(self, prompt: str, system_message: str = None,
                        max_tokens: int = 1000, temperature: float = 0.7,
                        chat_history: List[Dict[str, str]] = None, **kwargs) -> Any:
        """
        Generate a streaming response using the configured model.
        
        Returns a generator that yields response chunks as they become available.
        """
        if not self.client:
            raise ValueError("No client initialized. Make sure model_name and credentials are provided.")
        
        if "openai" in self.model_name.lower():
            return self._stream_generate_openai(prompt, system_message, max_tokens, temperature, chat_history, **kwargs)
        else:
            raise ValueError(f"Streaming not implemented for model: {self.model_name}")
        
        
    def _stream_generate_openai(self, prompt: str, system_message: str = None,
                                max_tokens: int = 1000, temperature: float = 0.7,
                                chat_history: List[Dict[str, str]] = None, **kwargs) -> Any:
        """Stream generate a response using OpenAI's API."""
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history)
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Get the specific model from kwargs or use a default
            model = kwargs.get("model", "gpt-4o")
            
            # Create the streaming completion
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
                **{k: v for k, v in kwargs.items() if k not in ['model', 'stream']}
            )
            
            return stream
        except Exception as e:
            self.logger.error(f"Error streaming OpenAI response: {str(e)}")
            raise