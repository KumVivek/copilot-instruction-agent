"""LLM client for generating Copilot instructions."""
import os
import logging
from typing import Dict, List, Any, Optional
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
        
        logger.info(f"🤖 LLM Client initialized with model: {self.model}")
        logger.info(f"   API Key: {'✅ Set' if self.key else '❌ Not set'}")
        logger.debug(f"   Temperature: {self.temperature}, Max tokens: {self.max_tokens}")

    def generate_instructions(
        self, 
        stack: Dict[str, Any], 
        rules: List[str],
        findings: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, str]:
        """Generate categorized GitHub Copilot instructions from stack and rules.
        
        Args:
            stack: Detected tech stack information
            rules: List of rules/constraints to enforce
            findings: Optional list of findings from analysis
        
        Returns:
            Dictionary mapping category names to instruction content
        
        Raises:
            Exception: If API call fails
        """
        if not rules:
            logger.warning("No rules provided, generating generic instructions")
        
        findings = findings or []
        
        # Check if caching is present
        from core.instructions.generator import InstructionGenerator
        generator = InstructionGenerator(stack.get("language", ""))
        has_caching = generator._detect_caching(findings, rules, stack)
        
        # Generate instructions for each category
        categories = ["design", "api", "security", "data-access", "testing", "logging"]
        if has_caching:
            categories.append("caching")
        
        instructions = {}
        
        for category in categories:
            try:
                prompt = self._build_category_prompt(category, stack, rules, findings)
                
                logger.info(f"🤖 Making OpenAI API call for {category} category using {self.model}")
                logger.debug(f"API Key present: {bool(self.key)}")
                logger.debug(f"Prompt length: {len(prompt)} characters")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are an expert at writing GitHub Copilot instruction files for {category}. Generate clear, detailed, enforceable rules based on best practices."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                
                # Log API usage information
                usage = getattr(response, 'usage', None)
                if usage:
                    logger.info(f"✅ API call successful for {category}: {usage.total_tokens} tokens used")
                else:
                    logger.info(f"✅ API call successful for {category}")
                
                category_instructions = response.choices[0].message.content
                if category_instructions:
                    instructions[category] = category_instructions
                    logger.info(f"✅ Generated {category} instructions ({len(category_instructions)} chars)")
                else:
                    logger.warning(f"⚠️ Empty response for {category}")
            except Exception as e:
                error_msg = str(e)
                # Handle specific API errors
                if "insufficient_quota" in error_msg or "429" in error_msg:
                    logger.error(f"OpenAI API quota exceeded for {category}")
                    raise RuntimeError(
                        "OpenAI API quota exceeded. Please:\n"
                        "1. Check your OpenAI account billing and plan\n"
                        "2. Visit https://platform.openai.com/account/billing\n"
                        "3. Or use the --skip-llm flag to generate rules without AI instructions"
                    ) from e
                elif "invalid_api_key" in error_msg or "401" in error_msg:
                    logger.error(f"Invalid OpenAI API key for {category}")
                    raise RuntimeError(
                        "Invalid OpenAI API key. Please:\n"
                        "1. Check your OPENAI_API_KEY environment variable\n"
                        "2. Get a key from https://platform.openai.com/api-keys\n"
                        "3. Or use the --skip-llm flag to skip AI generation"
                    ) from e
                else:
                    logger.warning(f"Failed to generate {category} instructions: {e}")
                    continue
        
        logger.info(f"Successfully generated {len(instructions)} category instruction files")
        return instructions
    
    def _build_category_prompt(
        self, 
        category: str,
        stack: Dict[str, Any], 
        rules: List[str],
        findings: List[Dict[str, Any]]
    ) -> str:
        """Build the prompt for category-specific instruction generation."""
        language = stack.get('language', 'Unknown')
        
        # Category mapping
        category_map = {
            "design": ["Architecture", "Code Quality"],
            "api": ["Architecture", "Security"],
            "security": ["Security"],
            "data-access": ["Architecture", "Security"],
            "caching": ["Performance"],
            "testing": ["Code Quality"],
            "logging": ["Code Quality"],
        }
        
        # Filter findings for this category
        relevant_categories = category_map.get(category, [])
        category_findings = [
            f for f in findings 
            if f.get("category") in relevant_categories
        ]
        
        # Filter rules for this category
        category_keywords = {
            "design": ["architecture", "design", "pattern", "controller", "service"],
            "api": ["api", "endpoint", "controller", "route", "http"],
            "security": ["security", "secure", "vulnerability", "injection", "authentication"],
            "data-access": ["database", "data", "repository", "query", "entity", "dbcontext"],
            "caching": ["cache", "performance", "optimize"],
            "testing": ["test", "unit", "integration", "mock"],
            "logging": ["log", "logger", "trace", "debug"],
        }
        
        keywords = category_keywords.get(category, [])
        category_rules = [
            rule for rule in rules
            if any(keyword in rule.lower() for keyword in keywords)
        ]
        
        # Load best practices for this category
        best_practices_context = ""
        try:
            loader = BestPracticesLoader()
            practices = loader.load_practices(language)
            
            # Get category-specific practices
            practices_categories = {
                "design": ["architecture", "code_quality"],
                "api": ["architecture"],
                "security": ["security"],
                "data-access": ["architecture", "security"],
                "caching": ["performance"],
                "testing": ["code_quality"],
                "logging": ["code_quality"],
            }
            
            relevant_practice_cats = practices_categories.get(category, [])
            categories = practices.get("categories", {})
            
            for cat_name in relevant_practice_cats:
                if cat_name in categories:
                    cat_info = categories[cat_name]
                    best_practices_context += f"\n### {cat_name.title()} Practices:\n"
                    best_practices_context += f"{cat_info.get('description', '')}\n"
                    for practice in cat_info.get("practices", []):
                        best_practices_context += f"- {practice}\n"
        except Exception as e:
            logger.debug(f"Could not load best practices for {category}: {e}")
        
        category_titles = {
            "design": "Design & Architecture",
            "api": "API Development",
            "security": "Security",
            "data-access": "Data Access",
            "caching": "Caching",
            "testing": "Testing",
            "logging": "Logging",
        }
        
        category_title = category_titles.get(category, category.title())
        
        findings_text = ""
        if category_findings:
            findings_text = f"\n\nIssues found in codebase ({len(category_findings)}):\n"
            for finding in category_findings[:5]:
                findings_text += f"- {finding.get('pattern', 'Unknown')} ({finding.get('severity', 'UNKNOWN')})\n"
        
        rules_text = "\n".join(f"- {rule}" for rule in category_rules) if category_rules else "None specific to this category"
        
        return f"""Generate a detailed GitHub Copilot instruction file for {category_title} in a {language} project.

Tech stack: {language} (confidence: {stack.get('confidence', 0):.0%})
Category: {category_title}
{findings_text}

Rules and constraints for {category}:
{rules_text}
{best_practices_context}

Requirements:
- Create a comprehensive, detailed instruction file
- Include best practices specific to {category} for {language}
- Provide clear, actionable, enforceable rules
- Include examples where helpful
- Format as proper markdown
- Be specific to {language} frameworks and patterns
- Cover all aspects of {category} development
- Prioritize critical issues found in the codebase

Generate the complete instruction file content (markdown format) that will be saved as .github/copilot-instructions-{category}.md
"""
