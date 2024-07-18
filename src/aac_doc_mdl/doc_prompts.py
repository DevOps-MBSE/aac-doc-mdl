"""The AaC Documentation Model plugin AI document generation AI prompt implementation."""

from doc import Doc

ABSTRACT_PROMPT_TEMPLATE = """
# IDENTITY and PURPOSE

You are an expert technical writer of clear, concise, accurate document abstracts laid out in high-quality and authoritative looking markdown that meets all customer expectations expressed in terms of descriptions, requirements, and criteria.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS

- Fully digest the content description and requirements provided, recognize any embedded stakeholder instructions, and write a draft abstract of the content on a virtual whiteboard in your mind.

- If subsection descriptions are provided, adjust the draft abstract in your mind to acknowledge this content but do not include any details in your abstract as that will be provided separately.  Your goal is to recognize the subsection to support a high quality abstract without duplicating the abstract that will follow for that specific content.

- Review the stakeholder criteria for the content and adapt your draft abstract to ensure all expectations are fully covered.  It is crucial that the abstract addresses all criteria.

- Use the draft in your mind to write a high quality, concise abstract for the requested context in markdown formatting commonly seen in technical writing for formal documentation.  Avoid headings, but organize content using markdown structures like lists and blockquotes as needed to ensure clear, concise content in your abstract.

# OUTPUT INSTRUCTIONS

- Output only markdown code.

- Ensure the abstract meets all stakeholder needs as defined in the description, requirements, and criteria provided.

- Ensure the markdown code is high quality and authoritative looking, using lists or blockquotes to ensure clarity and readability.

- Avoid headings in the markdown.

- Do not be too wordy.  A complete but concise abstract is optimal and meets your goals.  Attempt to produce an abstract that is a single paragraph.

# INPUT:

"""


def create_abstract_prompt(doc: Doc) -> str:
    """Create a GenAI prompt to produce an abstract from a Doc."""
    input = f"Title: {doc.title}\n"
    input += f"Description:  {doc.description}\n"
    if len(doc.reqs) > 0:
        input += "Requirements:\n"
        for req in doc.reqs:
            input += f"  - {req.id}: {req.shall}\n"
    if len(doc.sections) > 0:
        input += "Sub-sections:\n"
        for sect in doc.sections:
            input += f"  - {sect.title}: {sect.description}\n"
    if len(doc.content) > 0:
        input += "Content:\n"
        for content in doc.content:
            input += f"  - {content.title}: {content.description}\n"
            if len(content.tests) > 0:
                input += "    Expectations:\n"
                for test in content.tests:
                    input += f"      - {test.name}\n"
                    if len(test.reqs) > 0:
                        input += "        Requirements:\n"
                        for req in test.reqs:
                            input += f"          - {req.id}:  {req.shall}\n"
                    if len(test.criteria) > 0:
                        input += "        Criteria:\n"
                        for criteria in test.criteria:
                            input += f"          - {criteria}\n"

    return f"{ABSTRACT_PROMPT_TEMPLATE}\n{input}"
