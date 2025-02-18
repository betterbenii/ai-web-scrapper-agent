import os
import groq
from dotenv import load_dotenv
from langchain_core.prompts import ChatMessagePromptTemplate


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please set it in the .env file.")

# Initialize Groq client with the API key
client = groq.Client(api_key=GROQ_API_KEY)

# Define the prompt template
template = (
    "You are an intelligent assistant tasked with extracting useful, well-structured information from the following text content: {dom_content}. "
    "Please organize your response in a structured format with proper bullet points, categories, and human-like phrasing. \n\n"
    "### Instructions:\n"
    "1. **Extract only relevant information** based on this request: {parse_description}.\n"
    "2. **Format the output properly**, using bullet points or sections when applicable.\n"
    "3. **Use natural human-like phrasing** to make the output readable.\n"
    "4. **If no useful information is found, respond with:** 'No relevant data found.'\n\n"
    
    "5. **If the user asks the assistant to summarize and provide a a table, a chart, etc, provide the type of summaryy requested.**"
    "6. **If no structured information is found, respond accordingly.**"
    "7. **If the user asks for a formal report, provide a detailed summary.**"
)

def parse_with_groq(dom_chunks, parse_description):
    """
    Parse the given DOM content with Groq using the template defined above.

    This function takes a list of strings representing the DOM content, and a description of the information to be extracted.
    It iterates over each chunk of the DOM content, creates a Groq prompt with the given text and instructions, and parses the content
    using the Groq client. The parsed text content is then returned as a single string.

    Args:
        dom_chunks (list): A list of strings, each containing a chunk of the DOM content.
        parse_description (str): A description of the information to be extracted from the DOM content.

    Returns:
        str: The parsed text content, formatted according to the instructions in the template.
    """
    parsed_results = []
    
    # Iterate over each chunk of the DOM content and parse it
    for i, chunk in enumerate(dom_chunks, start=1):
        # Create a prompt with the given text and instructions
        prompt_text = template.format(dom_content=chunk, parse_description=parse_description)
        # Create a chat completion with the given prompt and instructions
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt_text}
            ],
            # Adjust the temperature to control the level of creativity in the output
            temperature=0.3,
            # Set the maximum number of tokens to generate
            max_tokens=3000,
        )

        # Get the parsed text content
        result_text = response.choices[0].message.content.strip()
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(result_text)

    # Join the parsed results into a single string
    return "\n".join(parsed_results)
