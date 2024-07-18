"""The AaC Document Model plugin implementation module."""

# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

# There may be some unused imports depending on the definition of the plugin, be sure to remove unused imports.
from typing import Any

from aac.context.definition import Definition
from aac.context.language_context import LanguageContext
from aac.context.source_location import SourceLocation
from aac.execute.aac_execution_result import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionMessage,
    MessageLevel,
)
from aac.in_out.files.aac_file import AaCFile

plugin_name = "Document Model"


def gen_doc_outline(
    title: str,
    architecture_file: str,
    no_pdf: bool,
    gen_eval: bool,
    parent_reqs: bool,
    output: str,
    temperature: float,
) -> ExecutionResult:
    """
        Business logic for allowing gen-doc-outline command to perform An AI powered command that uses your model definition to generate an annotated outline of the document with abstracts for each section.  The output is a markdown file and a PDF generated from the markdown.

    The structure of the annotated outline is based on your model-component decomposition.  The content for each section abstract is generated using any linked requirements, acceptance test specification, the descriptions provided by the model and if present the description of components.

    Because this utilizes Generative AI, the output should be carefully reviewed by a human for quality and correctness.  It may also take quite some time to run depending on the number of AI calls required based on your document model.

        Args:
            title (str): The name of the root document model.
    architecture_file (str): A path to a YAML file containing an AaC-defined document model to evaluate.
    no_pdf (bool): Instructs the plugin to not generate a PDF file, resulting only in a markdown file.
    gen_eval (bool): Instructs the plugin to generate an evaluation model where descriptions are replaced with AI generated abstracts.  Disabled by default.
    parent_reqs (bool): Tells AaC to include parent requirements from your spec in the metadata output.  Default does not include parent requirements.output (str): The location to output generated document.  Default is current working directory.temperature (float): The temperature passed into the AI text generator.  Default value is 0.1

       Returns:
            The results of the execution of the gen-doc-outline command.
    """

    # Create the outline based on the structure of the model's composition. The model with the title name is the base doc.
    # Each component is a section in the doc.  Further components are sub-sections, and so on.
    # It seems that the abstract for a portion of the model should be aware of it's sub-portions so first build the structure
    # as a hierarchy and then traverse the document structure from the lowest level up to the top.

    # First capture the document structure as a dict with appropriate content captured at each level.  Then generate whatever
    # content is needed by adding entries to the layers of the dict.  The pass the dict into Jinja to produce the desired output.

    


    # TODO: implement plugin logic here
    status = ExecutionStatus.GENERAL_FAILURE
    messages: list[ExecutionMessage] = []
    error_msg = ExecutionMessage(
        "The gen-doc-outline command for the Document Model plugin has not been implemented yet.",
        MessageLevel.ERROR,
        None,
        None,
    )
    messages.append(error_msg)

    return ExecutionResult(plugin_name, "gen-doc-outline", status, messages)


def gen_doc_draft(
    title: str,
    architecture_file: str,
    no_pdf: bool,
    output: str,
    content_only: bool,
    parent_reqs: bool,
    temperature: float,
) -> ExecutionResult:
    """
        Business logic for allowing gen-doc-draft command to perform An AI powered command that uses your model definition to generate an a draft of the document with content for each section.  The output is a markdown file and a PDF generated from the markdown.

    The structure of the document is based on your model-component decomposition.  The content for each section is generated using any linked requirements, acceptance test specification, the descriptions provided by the model and if present the description of components.

    Because this utilizes Generative AI, the output should be carefully reviewed by a human for quality and correctness.  It may also take quite some time to run depending on the number of AI calls required based on your document model.

        Args:
            title (str): The name of the root document model.
    architecture_file (str): A path to a YAML file containing an AaC-defined document model to evaluate.
    no_pdf (bool): Instructs the plugin to not generate a PDF file, resulting only in a markdown file
    output (str): The location to output generated document.  Default is current working directory.content_only (bool): Instructs the plugin to only produce document content, eliminating additional data such as requirements and test information.
    parent_reqs (bool): Tells AaC to include parent requirements from your spec in the metadata output.  Default does not include parent requirements.temperature (float): The temperature passed into the AI text generator.  Default value is 0.2

       Returns:
            The results of the execution of the gen-doc-draft command.
    """

    # TODO: implement plugin logic here
    status = ExecutionStatus.GENERAL_FAILURE
    messages: list[ExecutionMessage] = []
    error_msg = ExecutionMessage(
        "The gen-doc-draft command for the Document Model plugin has not been implemented yet.",
        MessageLevel.ERROR,
        None,
        None,
    )
    messages.append(error_msg)

    return ExecutionResult(plugin_name, "gen-doc-draft", status, messages)


def gen_doc_vcrm(
    title: str, doc_architecture_file: str, output: str, parent_reqs: bool
) -> ExecutionResult:
    """
        Business logic for allowing gen-doc-vcrm command to perform Generate a verification cross-reference matrix for you document.  The creates a table with all the requirements as rows, document sections as columns, and an indicator showing the trace from requirement to section.

        Args:
            title (str): The name of the root document model.
    doc_architecture_file (str): A path to a YAML file containing an AaC-defined document model to evaluate.
    output (str): The location to output generated document.  Default is current working directory.parent_reqs (bool): Tells AaC to include parent requirements from your spec in the VCRM output.  Default does not include parent requirements.

       Returns:
            The results of the execution of the gen-doc-vcrm command.
    """

    # TODO: implement plugin logic here
    status = ExecutionStatus.GENERAL_FAILURE
    messages: list[ExecutionMessage] = []
    error_msg = ExecutionMessage(
        "The gen-doc-vcrm command for the Document Model plugin has not been implemented yet.",
        MessageLevel.ERROR,
        None,
        None,
    )
    messages.append(error_msg)

    return ExecutionResult(plugin_name, "gen-doc-vcrm", status, messages)
