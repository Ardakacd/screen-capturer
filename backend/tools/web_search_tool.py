from crewai.tools import tool
from openai import OpenAI
import json


def create_web_search_tool():
    """
    Factory function to create web_search_url_tool.
    
    This tool doesn't need page, id_number, or loop dependencies since it only
    makes API calls to OpenAI's web search feature.
    """
    
    client = OpenAI()
    
    @tool("web_search_url_tool")
    def web_search_url_tool(goal: str) -> str:
        """
        Find the correct URL to start a web automation task using web search.
        
        This tool uses OpenAI's GPT-4 with web search capabilities to determine
        the best URL to navigate to for accomplishing a given goal. It assumes
        the user is already logged in to the target application.
        
        Args:
            goal (str): The user's goal or task description.
                       Example: "How to invite a teammate in Notion?"
        
        Returns:
            str: The URL(s) to navigate to, or an error message if the search fails.
        
        Usage: Use this at the beginning of a workflow to determine where to navigate
               based on the user's goal. This is especially useful when the starting
               URL depends on the task context (like a specific repository or project).
        """
        

        system_prompt = """You are a web URL finder assistant. 
Your job is to identify the **base URL (domain only)** of the web application where the user's workflow should begin,
assuming the user is already logged in to the target app.

Instructions:
- Return ONLY the base URL without any path (e.g., "https://example.com" NOT "https://example.com/path")
- You must prioritize **the actual web application** URL, not documentation, help articles, or blog posts.
- Return the main domain where users access the application after login.
- If the application has multiple domains or starting points, return all base URLs as a list.
- If no clear application URL is found, return an empty list.

Output Format:
You MUST return ONLY a valid JSON object with this exact structure (no extra text):
{
  "urls": ["<base_url1>", "<base_url2>", ...]
}"""

        user_prompt = f"The user's goal is: {goal}"

        try:
            response = client.chat.completions.create(
                model="gpt-4o-search-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )
            
            result = response.choices[0].message.content.strip()
            
            try:
                parsed = json.loads(result)
                if "urls" in parsed:
                    return result
                else:
                    return f'{{"urls": [], "error": "Invalid response format from web search"}}'
            except json.JSONDecodeError:
                return f'{{"urls": [], "error": "Failed to parse JSON from web search response"}}'

        except Exception as e:
            error_msg = f"Web search failed: {type(e).__name__} - {e}"
            return f'{{"urls": [], "error": "{error_msg}"}}'
    
    return web_search_url_tool

