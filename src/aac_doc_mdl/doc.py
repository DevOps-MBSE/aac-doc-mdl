from typing import ForwardRef
from pydantic import BaseModel

from aac.context.language_context import LanguageContext

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
    abstract: str
    sections: list[Doc] = []
    content: list[Content]
    reqs: list[Req]


Doc.model_rebuild()


def _req_from_id(id) -> Req:
    """Look up a requirement based on the req ID and create the Req."""
    context = LanguageContext()

    for req_def in context.get_definitions_by_root('req'):
        req = req_def.instance
        if req.id == id:
            return Req(id=id, shall=req.shall)
    
    # just return None if I don't find anything
    print(f"DEBUG: couldn't fine req for id {id}")
    return None


def _test_from_scenario(scenario) -> Test:
    """Buld a test object from a feature in the AaC model."""
    reqs = []
    for id in scenario.requirements:
        reqs.append(_req_from_id(id))

    criteria = []
    for line in scenario.then:
        criteria.append(line)
    test = Test(name=scenario.name, reqs=reqs, criteria=criteria)
    return test


def _content_from_behavior(behavior) -> Content:
    """Create a Content from an AaC behavior."""
    heading = behavior.name
    description = behavior.description
    tests = []

    print(f"DEBUG:  working on behavior - {behavior.name} with {len(behavior.acceptance)} acceptance tests")
    print(f"DEBUG:  dump\n\n{behavior}")
    for feature in behavior.acceptance:
        for scenario in feature.scenarios:
            tests.append(_test_from_scenario(scenario))
    print(f"DEBUG:  creating content - {heading}, {description}, {tests}")
    return Content(heading=heading, description=description, tests=tests)


def doc_from_model(model) -> Doc:
    """Create a Doc from an AaC model."""
    title = model.name
    description = model.description
    abstract = ""
    sections = []
    content = []
    reqs = []

    context = LanguageContext()

    # populate sections
    for comp in model.components:
        model_defs = context.get_definitions_by_name(comp.name)
        if len(model_defs) != 1:
            print(f"ERROR - must be only 1 model with name {comp.name}")
        else:
            sections.append(doc_from_model(model_defs[0].instance))

    # populate requirements
    for model_req in model.requirements:
        req = _req_from_id(model_req)
        if req:
            reqs.append(req)

    # populate content
    for entry in model.behavior:
        content.append(_content_from_behavior(entry))

    return Doc(title=title, description=description, abstract=abstract, sections=sections, content=content, reqs=reqs)
