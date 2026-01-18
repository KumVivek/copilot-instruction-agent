"""LLM client for generating Copilot instructions."""
import os
import logging
from typing import Dict, List, Any
from openai import OpenAI
from core.config import Config
from core.best_practices.loader import BestPracticesLoader

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with OpenAI API to generate Copilot instructions."""
    
    def __init__(self, config: Config):
        """Initialize LLM client.
        
        Args:
            config: Configuration instance
        
        Raises:
            RuntimeError: If OPENAI_API_KEY is not set
        """
        self.config = config
        self.key = os.getenv("OPENAI_API_KEY")
        if not self.key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.key)
        self.model = config.get("llm.model", "gpt-4o-mini")
        self.temperature = config.get("llm.temperature", 0.3)
        self.max_tokens = config.get("llm.max_tokens", 2000)
        
        logger.debug(f"Initialized LLM client with model: {self.model}")

    def generate_instructions(self, stack: Dict[str, Any], rules: List[str]) -> str:
        """Generate GitHub Copilot instructions from stack and rules.
        
        Args:
            stack: Detected tech stack information
            rules: List of rules/constraints to enforce
        
        Returns:
            Generated Copilot instructions as markdown string
        
        Raises:
            Exception: If API call fails
        """
        if not rules:
            logger.warning("No rules provided, generating generic instructions")
        
        prompt = self._build_prompt(stack, rules)
        
        try:
            logger.info(f"Generating Copilot instructions using {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at writing GitHub Copilot instruction files. Generate clear, enforceable rules only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            instructions = response.choices[0].message.content
            logger.info("Successfully generated Copilot instructions")
            return instructions or ""
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific API errors with helpful messages
            if "insufficient_quota" in error_msg or "429" in error_msg:
                logger.error("OpenAI API quota exceeded. Please check your billing and plan.")
                raise RuntimeError(
                    "OpenAI API quota exceeded. Please:\n"
                    "1. Check your OpenAI account billing and plan\n"
                    "2. Visit https://platform.openai.com/account/billing\n"
                    "3. Or use the --skip-llm flag to generate rules without AI instructions"
                ) from e
            elif "invalid_api_key" in error_msg or "401" in error_msg:
                logger.error("Invalid OpenAI API key")
                raise RuntimeError(
                    "Invalid OpenAI API key. Please:\n"
                    "1. Check your OPENAI_API_KEY environment variable\n"
                    "2. Get a key from https://platform.openai.com/api-keys\n"
                    "3. Or use the --skip-llm flag to skip AI generation"
                ) from e
            else:
                logger.error(f"Failed to generate instructions: {e}")
                raise RuntimeError(f"LLM API call failed: {e}") from e
    
    def _build_prompt(self, stack: Dict[str, Any], rules: List[str]) -> str:
        """Build the prompt for instruction generation."""
        language = stack.get('language', 'Unknown')
        rules_text = "\n".join(f"- {rule}" for rule in rules) if rules else "None specified"
        
        # Load best practices for context
        best_practices_context = ""
        try:
            loader = BestPracticesLoader()
            practices = loader.load_practices(language)
            
            practices_rules = practices.get("rules", [])
            if practices_rules:
                best_practices_context = "\n\nBest Practices for " + language + ":\n"
                best_practices_context += "\n".join(f"- {rule}" for rule in practices_rules[:10])  # Limit to 10
            
            categories = practices.get("categories", {})
            if categories:
                best_practices_context += "\n\nKey Practice Categories:\n"
                for cat_name, cat_info in list(categories.items())[:5]:  # Limit to 5 categories
                    desc = cat_info.get("description", cat_name)
                    best_practices_context += f"- {cat_name}: {desc}\n"
        except Exception as e:
            logger.debug(f"Could not load best practices for prompt: {e}")
        
        return f"""Tech stack: {language} (confidence: {stack.get('confidence', 0)})

Rules and constraints to enforce (based on code analysis):
{rules_text}
{best_practices_context}

Generate a GitHub Copilot instructions file (.github/copilot-instructions.md format).
Requirements:
- No explanations or commentary
- Only enforceable rules and constraints
- Clear, actionable directives
- Format as proper markdown
- Focus on preventing the issues found in the codebase
- Incorporate the best practices for {language}
- Be specific to the {language} stack and framework patterns
- Prioritize critical security and architectural constraints
"""
