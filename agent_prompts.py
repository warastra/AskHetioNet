from langchain.prompts import PromptTemplate
import re

# Langchain self-ask with search default prompt
self_ask_w_search_template = """Question: Who lived longer, Muhammad Ali or Alan Turing?
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali

Question: When was the founder of craigslist born?
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952

Question: Who was the maternal grandfather of George Washington?
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball

Question: Are both the directors of Jaws and Casino Royale from the same country?
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate answer: New Zealand.
So the final answer is: No

Question: {input}
Are followup questions needed here:{agent_scratchpad}"""

self_ask_w_search_prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad"], 
    template=self_ask_w_search_template
)

ReAct_EXAMPLES = [
    """Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?
Thought: I need to search Colorado orogeny, find the area that the eastern sector of the Colorado orogeny extends into, then find the elevation range of the area.
Action: Search[Colorado orogeny]
Observation: The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas.
Thought: It does not mention the eastern sector. So I need to look up eastern sector.
Action: Lookup[eastern sector]
Observation: (Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny.
Thought: The eastern sector of Colorado orogeny extends into the High Plains. So I need to search High Plains and find its elevation range.
Action: Search[High Plains]
Observation: High Plains refers to one of two distinct land regions
Thought: I need to instead search High Plains (United States).
Action: Search[High Plains (United States)]
Observation: The High Plains are a subregion of the Great Plains. From east to west, the High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130 m).[3]
Thought: High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft.
Action: Finish[1,800 to 7,000 ft]""",
    """Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
Thought: The question simplifies to "The Simpsons" character Milhouse is named after who. I only need to search Milhouse and find who it is named after.
Action: Search[Milhouse]
Observation: Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening.
Thought: The paragraph does not tell who Milhouse is named after, maybe I can look up "named after".
Action: Lookup[named after]
Observation: (Result 1 / 1) Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous.
Thought: Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.
Action: Finish[Richard Nixon]""",
    """Question: Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?
Thought: I need to search Adam Clayton Powell and The Saimaa Gesture, and find which documentary is about Finnish rock groups.
Action: Search[Adam Clayton Powell]
Observation: Could not find [Adam Clayton Powell]. Similar: [’Adam Clayton Powell III’, ’Seventh Avenue (Manhattan)’, ’Adam Clayton Powell Jr. State Office Building’, ’Isabel Washington Powell’, ’Adam Powell’, ’Adam Clayton Powell (film)’, ’Giancarlo Esposito’].
Thought: To find the documentary, I can search Adam Clayton Powell (film).
Action: Search[Adam Clayton Powell (film)]
Observation: Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg. The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience.
Thought: Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture.
Action: Finish[The Saimaa Gesture]""",
    """Question: What profession does Nicholas Ray and Elia Kazan have in common?
Thought: I need to search Nicholas Ray and Elia Kazan, find their professions, then find the profession they have in common.
Action: Search[Nicholas Ray]
Observation: Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 - June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause.
Thought: Professions of Nicholas Ray are director, screenwriter, and actor. I need to search Elia Kazan next and find his professions.
Action: Search[Elia Kazan]
Observation: Elia Kazan was an American film and theatre director, producer, screenwriter and actor.
Thought: Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor.
Action: Finish[director, screenwriter, actor]""",
    """Question: Which magazine was started first Arthur’s Magazine or First for Women?
Thought: I need to search Arthur’s Magazine and First for Women, and find which was started first.
Action: Search[Arthur’s Magazine]
Observation: Arthur’s Magazine (1844-1846) was an American literary periodical published in Philadelphia in the 19th century.
Thought: Arthur’s Magazine was started in 1844. I need to search First for Women next.
Action: Search[First for Women]
Observation: First for Women is a woman’s magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989.
Thought: First for Women was started in 1989. 1844 (Arthur’s Magazine) < 1989 (First for Women), so Arthur’s Magazine was started first.
Action: Finish[Arthur’s Magazine]""",
    """Question: Were Pavel Urysohn and Leonid Levin known for the same type of work?
Thought: I need to search Pavel Urysohn and Leonid Levin, find their types of work, then find if they are the same.
Action: Search[Pavel Urysohn]
Observation: Pavel Samuilovich Urysohn (February 3, 1898 - August 17, 1924) was a Soviet mathematician who is best known for his contributions in dimension theory.
Thought: Pavel Urysohn is a mathematician. I need to search Leonid Levin next and find its type of work.
Action: Search[Leonid Levin]
Observation: Leonid Anatolievich Levin is a Soviet-American mathematician and computer scientist.
Thought: Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn and Leonid Levin have the same type of work.
Action: Finish[yes]""",
]
ReAct_SUFFIX = """\nQuestion: {input}
{agent_scratchpad}"""

ReAct_WIKI_PROMPT = PromptTemplate.from_examples(
    ReAct_EXAMPLES, ReAct_SUFFIX, ["input", "agent_scratchpad"]
)

ReAct_agent_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

ReAct_agent_PROMPT = PromptTemplate(
    input_variables=["tools","tool_names","input", "agent_scratchpad"],
    template=ReAct_agent_template
)


# my own custom prompt 
ReAct_self_ask_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Are follow up questions needed here: either a Yes or No
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Examples:

Question: How much older was Muhammad Ali when he died compared to Alan Turing?
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Action: Search
Action Input: How old was Muhammad Ali when he died?
Observation: Muhammad Ali was 74 years old when he died.
Thought: I need to find out about Alan Turing
Follow up: How old was Alan Turing when he died?
Action: Search
Action Input: How old was Alan Turing when he died?
Observation: Alan Turing was 41 years old when he died.
Final Answer: Muhammad Ali

Begin!

Question: {input}
Are followup questions needed here:{agent_scratchpad}"""

ReAct_self_ask_prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad"], 
    template=ReAct_self_ask_template
)

summarize_template = """The following original question has been answered by different assistants ordered by their expertise level with Assistant 1 being the best.
refine the assistants' answer into a single coherent answer in bahasa indonesia. Ignore assistant that say 'answer not found' or 'tidak ditemukan'.
Original Question:{query_str}
{assistants}
Answer Summary:
"""

def get_summarize_refine_prompt(query, answer_list):
    assistants = ''
    for idx, answer in enumerate(answer_list):
        str_idx = str(idx+1)
        assistants += f'Assistant {str_idx}: {answer}\n'
    return summarize_template.format(query_str=query, assistants=assistants)

entity_extract_prompt = """From the following questions extract the JARGONS mentioned in the question.
ONLY extract technical JARGONS that are related to information technology, artificial intelligence, healthcare, social welfare, culture, education,  employment, inclusion, or disability.
format the answer by separating each JARGONS with comma. Answer with "NO_JARGONS_FOUND" if there is no JARGONS related to the specified topics.

Example 1
Question: Apa yg dapat dilakukan pemerintah untuk menjamin inklusi masyarakat adat?
JARGONS: inklusi masyarakat adat

Example 2
Question: bagaimana contoh pemanfaatan image analysis dalam menyelesaikan konflik pekerja asing di tambang nikel
JARGONS: image analysis

Example 3
Question: Sejak kapan Phil Foden bermain untuk Manchester City
JARGONS: NO_JARGONS_FOUND

Question: {query}
KEY TERMS: 
"""

def keyterm_extraction_parser(model_output:str):
    try:
        keyterm = model_output.split(',')
        keyterm = [x.strip() for x in keyterm]
    except:
        keyterm = []
    return keyterm