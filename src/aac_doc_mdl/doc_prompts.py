"""The AaC Documentation Model plugin AI document generation AI prompt implementation."""

from aac_doc_mdl.doc import Doc

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

DOCUMENT_PROMPT_TEMPLATE = """
# IDENTITY and PURPOSE

You are an expert technical writer of clear, concise, accurate formal engineering technical documents laid out in high-quality and authoritative looking markdown that meets all customer expectations expressed in terms of descriptions, requirements, and criteria.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS

- Fully digest the content description and requirements provided, recognize any embedded stakeholder instructions, and write high quality document content on a virtual whiteboard in your mind.

- If subsection descriptions are provided, adjust the draft document content in your mind to acknowledge this content but do not include any details in your document as that should be in the section content.  Your goal is to recognize the subsection to support high quality document text flow and framing without duplicating the content that will follow for that specific section.

- Review the stakeholder requirements and criteria for the content and adapt your draft document to ensure all expectations are fully covered.  It is crucial that the document explicitly addresses all criteria so that reviewers can easily approve for publication.

- Use the draft in your mind to write a high quality, concise document for the requested context in markdown formatting commonly seen in technical writing for formal documentation.  Use clear heading titles. Feel free to organize content using markdown structures like lists and blockquotes as needed to ensure clear, concise content in your document text.

# OUTPUT INSTRUCTIONS

- Output only markdown code.

- Ensure the document meets all stakeholder expectations as defined in the description, requirements, and criteria provided.

- Ensure the markdown code is high quality and authoritative looking, using headings, lists, or blockquotes to ensure clarity and readability.

- Do not be too wordy or abstract in your narrative.  Remember that this is technical writing and not creative writing.  A complete but concise document is optimal and meets your goals.

- You are not constrained on length unless there are specific requirements or criteria on content length from the stakeholder. Find the right balance between concise and complete language, favoring completeness to ensure all requirements and criteria are met.

# INPUT:

"""


def _create_prompt(prompt_starter: str, doc: Doc) -> str:
    """Create a GenAI prompt to produce a tailored document from a model."""
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
            input += f"  - {content.heading}: {content.description}\n"
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
                            input += f"          - {criteria}\n\n"

    return f"{prompt_starter}\n{input}"


def create_abstract_prompt(doc: Doc) -> str:
    """Create an AI prompt to generate an abstract from a document model."""
    return _create_prompt(ABSTRACT_PROMPT_TEMPLATE, doc)


def create_document_prompt(doc: Doc) -> str:
    """Create an AI prompt to generate an abstract from a document model."""
    return _create_prompt(DOCUMENT_PROMPT_TEMPLATE, doc)
