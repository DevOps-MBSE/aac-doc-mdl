from typing import ForwardRef
from pydantic import BaseModel

import os
import json
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown
from weasyprint import HTML

from aac.context.language_context import LanguageContext

from aac_doc_mdl.ai_util import generate

# The doc dict keys will be:
#  - title (str):  The title of the section taken from the model name.
#  - description (str):  The description of the section taken from the model description.
#  - abstract (str):  An AI generated abstract.
#  - sections (doc[]):  A list of this same dict section created from the model components.
#  - content (content[]): A list of dicts describing the content of this section created from the model behaviors.
#  - reqs (req[]): A list of simple dicts containing require ID and shall statement assigned to this content.

# For completeness, the content keys will be:
#  - heading (str): The name of the content taken from the behavior name.
#  - description (str): The description taken from the behavior description.
#  - tests (test[]): The list of acceptance tests associated with the content.

# And finally, the test keys will be:
#  - name (str): The test name taken from the scenario name.
#  - reqs (req[]): A list of simple dicts containing requirement ID and shall statement assigned to the scenario.
#  - criteria (str[]):  A list of content test expectations taken from the then portion of the scenario.

# The test portion does ignore the background, given, and when for now because I've not found a way to make these
# useful in the tests I've been able to create.  I'm a bit concerned that the potentially non-useful content here
# may negatively impact the GenAI output. If it turns out to be useful, or perhaps just harmless, it can be added.

# I am a bit concerned that doing all this with keys and dicts will get messy in the code.  I'm going to use
# pydantic to create the data model and then export it to a dict to use as input to Jinja2.  This is my first time
# using pydantic, so I'll be learning as I go with this one.


class Req(BaseModel):
    id: str
    shall: str


class Test(BaseModel):
    name: str
    reqs: list[Req]
    criteria: list[str]


class Content(BaseModel):
    heading: str
    description: str
    tests: list[Test]


Doc = ForwardRef('Doc')


class Doc(BaseModel):
    title: str
    description: str
    generated: str
    output: str
    sections: list[Doc] = []
    content: list[Content]
    reqs: list[Req]


Doc.model_rebuild()


def _req_from_id(id, parent_reqs) -> list[Req]:
    """Look up a requirement based on the req ID and create the Req."""
    context = LanguageContext()

    all_reqs = context.get_definitions_by_root('req')
    print(f"All reqs = {[req.instance.id for req in all_reqs]}")
    for req_def in all_reqs:
        req = req_def.instance
        if req.id == id:
            if not parent_reqs:
                return [Req(id=id, shall=req.shall)]
            else:
                print(f"DEBUG:  id {id} looking for parent reqs {req.parents}")
                if len(req.parents) == 0:
                    return [Req(id=id, shall=req.shall)]
                else:
                    ret_val = [Req(id=id, shall=req.shall)]
                    for parent_id in req.parents:
                        ret_val.extend(_req_from_id(parent_id, parent_reqs))
                    return ret_val

    # just return empty list if I don't find anything
    print(f"DEBUG: couldn't fine req for id {id}")
    return []


def _test_from_scenario(scenario, parent_reqs) -> Test:
    """Buld a test object from a feature in the AaC model."""
    reqs = []
    for id in scenario.requirements:
        reqs.extend(_req_from_id(id, parent_reqs))

    criteria = []
    for line in scenario.then:
        criteria.append(line)
    test = Test(name=scenario.name, reqs=reqs, criteria=criteria)
    return test


def _content_from_behavior(behavior, parent_reqs) -> Content:
    """Create a Content from an AaC behavior."""
    heading = behavior.name
    description = behavior.description
    tests = []

    for feature in behavior.acceptance:
        for scenario in feature.scenarios:
            tests.append(_test_from_scenario(scenario, parent_reqs))
    return Content(heading=heading, description=description, tests=tests)


def _add_markdown_indent(md: str, indent: int) -> str:
    if indent > 0:
        lines = md.split("\n")
        update = ""
        for line in lines:
            if line.strip().startswith("#"):
                update = update + "#" * indent + line + "\n"
            else:
                update = update + line + "\n"
        # print(f"DEBUG: _add_markdown_indent\ninput: {md}\noutput: {update}")
        return update
    return md


def _add_block_quote(md: str) -> str:
    lines = md.split("\n")
    return "\n".join(["> " + line for line in lines])


def _create_markdown_content(include_eng: bool, indent: int, doc: Doc) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_dir))
    jinja_main_template = env.get_template("./output_template_main.jinja2")
    main_markdown_text = jinja_main_template.render(doc.model_dump())
    # print(f"DEBUG: main_markdown_text\n{main_markdown_text}")
    eng_markdown_text = ""
    if indent > 0:
        main_markdown_text = _add_markdown_indent(main_markdown_text, indent)
    if include_eng:
        jinja_eng_template = env.get_template("./output_template_eng.jinja2")
        eng_markdown_text = jinja_eng_template.render(doc.model_dump())
        if indent > 0:
            eng_markdown_text = _add_markdown_indent(eng_markdown_text, indent)
        eng_markdown_text = _add_block_quote(eng_markdown_text)

    return f"{main_markdown_text}\n{eng_markdown_text}"


def doc_from_model(aac_model, ai_prompt_func, ai_client, ai_model, include_eng, parent_reqs, temperature, indent) -> Doc:
    """Create a Doc from an AaC model."""
    title = aac_model.name
    description = aac_model.description
    sections = []
    content = []
    reqs = []

    context = LanguageContext()

    print(f"DEBUG: building document - {title}")

    # populate sections
    for comp in aac_model.components:
        model_defs = context.get_definitions_by_name(comp.model)
        if len(model_defs) != 1:
            print(f"ERROR - must be 1 model with name {comp.name}")
        else:
            sections.append(doc_from_model(model_defs[0].instance, ai_prompt_func, ai_client, ai_model, include_eng, parent_reqs, temperature, indent + 1))

    # populate requirements
    for model_req in aac_model.requirements:
        req = _req_from_id(model_req, parent_reqs)
        if len(req):
            reqs.extend(req)

    # populate content
    for entry in aac_model.behavior:
        content.append(_content_from_behavior(entry, parent_reqs))

    doc = Doc(title=title, description=description, generated="", output="", sections=sections, content=content, reqs=reqs)

    prompt = ai_prompt_func(doc)
    # print(f"DEBUG:  prompt\n{prompt}\n\n")
    ai_output = generate(ai_client, ai_model, temperature, prompt).strip()
    if ai_output.startswith("```markdown"):
        text_to_replace = "```markdown\n"
        ai_output = ai_output.replace(text_to_replace, "", 1)
        index = ai_output.rfind("```")
        ai_output = ai_output[:index]

    doc.generated = ai_output

    doc.output = _create_markdown_content(include_eng, indent, doc)

    print(f"DEBUG: created document object\n{json.dumps(doc.model_dump(), indent=4)}")

    return doc


def _get_markdown_text(doc: Doc) -> str:

    # recursively walk the document sections
    markdown_text = doc.output + "\n"
    if doc.sections:
        for section in doc.sections:
            markdown_text = markdown_text + _get_markdown_text(section) + "\n"

    return markdown_text


def _write_files(path: str, file_name: str, write_pdf: bool, doc: Doc):
    """Create an ai prompt using the jinja template."""
    markdown_text = _get_markdown_text(doc)

    print(f"DEBUG: markdown_text - \n {markdown_text}")

    md_file_path = os.path.join(path, file_name + ".md")
    with open(md_file_path, "w") as file:
        file.write(markdown_text)
        print(f"DEBUG: markdown generated: {md_file_path}")

    if write_pdf:
        # Convert Markdown to HTML
        html_content = markdown(markdown_text, extras=["fenced-code-blocks"])

        # Define the PDF file path
        pdf_file_path = os.path.join(path, file_name + ".pdf")

        # Convert HTML to PDF
        HTML(string=html_content, base_url=path).write_pdf(pdf_file_path)

        print(f"DEBUG: PDF generated: {pdf_file_path}")


def write_doc(path: str, file_name: str, doc: Doc, write_pdf: bool):
    _write_files(path, file_name, write_pdf, doc)