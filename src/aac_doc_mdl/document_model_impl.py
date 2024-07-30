"""The AaC Document Model plugin implementation module."""

# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

# There may be some unused imports depending on the definition of the plugin, be sure to remove unused imports.

import os

from aac.context.language_context import LanguageContext
from aac.execute.aac_execution_result import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionMessage,
    MessageLevel,
)

from aac_doc_mdl.ai_util import get_client
from aac_doc_mdl.doc import Doc, doc_from_model, write_doc, vcrm_from_model, vcrm_to_csv, vcrm_to_markdown, has_full_coverage
from aac_doc_mdl.doc_prompts import create_outline_prompt, create_document_prompt

plugin_name = "Document Model"


def _get_model_definition_with_name(title: str, architecture_file: str):

    context = LanguageContext()

    definitions = context.parse_and_load(architecture_file)

    for definition in definitions:
        if definition.get_root_key() == "model" and definition.instance.name == title:
            # This is the document model
            return definition

    # print(f"DEBUG: Cannot find model with name {title} in {[definition.instance.name for definition in definitions if definition.get_root_key() == 'model']}")
    return None


def _get_filename_from_path(path: str) -> str:
    file_name = ""

    # get last part of the path
    parts = path.split(os.sep)
    file_name = parts[-1]

    # remove file extension
    parts = file_name.split(".")
    file_name = parts[0]

    return file_name


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
            parent_reqs (bool): Tells AaC to include parent requirements from your spec in the metadata output.  Default does not include parent requirements.
            output (str): The location to output generated document.  Default is current working directory.
            temperature (float): The temperature passed into the AI text generator.  Default value is 0.1

       Returns:
            The results of the execution of the gen-doc-outline command.
    """

    definition = _get_model_definition_with_name(title, architecture_file)
    if definition is None:
        status = ExecutionStatus.GENERAL_FAILURE
        messages: list[ExecutionMessage] = []
        error_msg = ExecutionMessage(
            f"Unable to locate a document model with name/title {title} in {architecture_file}.",
            MessageLevel.ERROR,
            None,
            None,
        )
        messages.append(error_msg)
        return ExecutionResult(plugin_name, "gen-doc-outline", status, messages)

    client, model, client_error, error_result = get_client(plugin_name)
    if client_error:
        return error_result

    doc: Doc = doc_from_model(definition.instance, create_outline_prompt, client, model, True, parent_reqs, temperature, 0)

    write_doc(output, f"{_get_filename_from_path(architecture_file)}-outline", doc, not no_pdf)

    return ExecutionResult(
        plugin_name,
        "gen-doc-outline",
        ExecutionStatus.SUCCESS,
        [
            ExecutionMessage(
                "Generated: an outline with abstracts",
                MessageLevel.INFO,
                definition.source,
                None,
            )
        ],
    )


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

    definition = _get_model_definition_with_name(title, architecture_file)
    if definition is None:
        status = ExecutionStatus.GENERAL_FAILURE
        messages: list[ExecutionMessage] = []
        error_msg = ExecutionMessage(
            f"Unable to locate a document model with name/title {title} in {architecture_file}.",
            MessageLevel.ERROR,
            None,
            None,
        )
        messages.append(error_msg)
        return ExecutionResult(plugin_name, "gen-doc-draft", status, messages)

    client, model, client_error, error_result = get_client(plugin_name)
    if client_error:
        return error_result

    doc: Doc = doc_from_model(definition.instance, create_document_prompt, client, model, True, parent_reqs, temperature, 0)

    write_doc(output, f"{_get_filename_from_path(architecture_file)}-draft", doc, not no_pdf)

    return ExecutionResult(
        plugin_name,
        "gen-doc-draft",
        ExecutionStatus.SUCCESS,
        [
            ExecutionMessage(
                "Generated: a draft document from a model",
                MessageLevel.INFO,
                definition.source,
                None,
            )
        ],
    )


def gen_doc_vcrm(
    title: str, doc_architecture_file: str, output: str, parent_reqs: bool
) -> ExecutionResult:
    """
        Business logic for allowing gen-doc-vcrm command to perform Generate a verification cross-reference matrix for you document.  The creates a table with all the requirements as rows, document sections as columns, and an indicator showing the trace from requirement to section.

        Args:
            title (str): The name of the root document model.
            doc_architecture_file (str): A path to a YAML file containing an AaC-defined document model to evaluate.
            output (str): The location to output generated document.  Default is current working directory.
            parent_reqs (bool): Tells AaC to include parent requirements from your spec in the VCRM output.  Default does not include parent requirements.

       Returns:
            The results of the execution of the gen-doc-vcrm command.
    """

    definition = _get_model_definition_with_name(title, doc_architecture_file)
    if definition is None:
        status = ExecutionStatus.GENERAL_FAILURE
        messages: list[ExecutionMessage] = []
        error_msg = ExecutionMessage(
            f"Unable to locate a document model with name/title {title} in {doc_architecture_file}.",
            MessageLevel.ERROR,
            None,
            None,
        )
        messages.append(error_msg)
        return ExecutionResult(plugin_name, "gen-doc-vcrm", status, messages)

    vcrm = vcrm_from_model(definition.instance, parent_reqs)

    arch_file_name = _get_filename_from_path(doc_architecture_file)
    vcrm_to_csv(vcrm, f"{os.path.join(output, arch_file_name)}-vcrm.csv")
    vcrm_to_markdown(vcrm, f"{os.path.join(output, arch_file_name)}-vcrm.md")

    if has_full_coverage(vcrm):
        return ExecutionResult(
            plugin_name,
            "gen-doc-vcrm",
            ExecutionStatus.SUCCESS,
            [
                ExecutionMessage(
                    f"Generated: a vcrm outputs from the document model {doc_architecture_file}",
                    MessageLevel.INFO,
                    definition.source,
                    None,
                )
            ],
        )
    else:
        status = ExecutionStatus.GENERAL_FAILURE
        messages: list[ExecutionMessage] = []
        error_msg = ExecutionMessage(
            f"VCRM for {title} resulted in an incomplete trace.",
            MessageLevel.ERROR,
            definition.source,
            None,
        )
        messages.append(error_msg)
        return ExecutionResult(plugin_name, "gen-doc-vcrm", status, messages)
