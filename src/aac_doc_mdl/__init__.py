"""__init__.py module for the Document Model plugin."""

# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED.
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from copy import deepcopy
from os.path import join, dirname
from typing import Any

from aac.context.definition import Definition
from aac.context.language_context import LanguageContext
from aac.context.source_location import SourceLocation
from aac.execute import hookimpl
from aac.execute.aac_execution_result import ExecutionResult, ExecutionStatus
from aac.execute.plugin_runner import PluginRunner
from aac.in_out.files.aac_file import AaCFile

from aac_doc_mdl.document_model_impl import plugin_name, gen_doc_outline, gen_doc_draft


document_model_aac_file_name = "document_model.aac"


def run_gen_doc_outline(
    title: str,
    architecture_file: str,
    no_pdf: bool,
    gen_eval: bool,
    output: str,
    temperature: float,
) -> ExecutionResult:
    """
        An AI powered command that uses your model definition to generate an annotated outline of the document with abstracts for each section.  The output is a markdown file and a PDF generated from the markdown.

    The structure of the annotated outline is based on your model-component decomposition.  The content for each section abstract is generated using any linked requirements, acceptance test specification, the descriptions provided by the model and if present the description of components.

    Because this utilizes Generative AI, the output should be carefully reviewed by a human for quality and correctness.  It may also take quite some time to run depending on the number of AI calls required based on your document model.

        Args:
            title (str): The name of the root document model.
    architecture_file (str): A path to a YAML file containing an AaC-defined document model to evaluate.
    no_pdf (bool): Instructs the plugin to not generate a PDF file, resulting only in a markdown file.
    gen_eval (bool): Instructs the plugin to generate an evaluation model where descriptions are replaced with AI generated abstracts.  Disabled by default.
    output (str): The location to output generated document.  Default is current working directory.temperature (float): The temperature passed into the AI text generator.  Default value is 0.1

       Returns:
            The results of the execution of the plugin gen-doc-outline command.
    """

    result = ExecutionResult(
        plugin_name, "gen-doc-outline", ExecutionStatus.SUCCESS, []
    )

    gen_doc_outline_result = gen_doc_outline(
        title, architecture_file, no_pdf, gen_eval, output, temperature
    )
    if not gen_doc_outline_result.is_success():
        return gen_doc_outline_result
    else:
        result.add_messages(gen_doc_outline_result.messages)

    return result


def run_gen_doc_draft(
    title: str,
    architecture_file: str,
    no_pdf: bool,
    output: str,
    content_only: bool,
    temperature: float,
) -> ExecutionResult:
    """
        An AI powered command that uses your model definition to generate an a draft of the document with content for each section.  The output is a markdown file and a PDF generated from the markdown.

    The structure of the document is based on your model-component decomposition.  The content for each section is generated using any linked requirements, acceptance test specification, the descriptions provided by the model and if present the description of components.

    Because this utilizes Generative AI, the output should be carefully reviewed by a human for quality and correctness.  It may also take quite some time to run depending on the number of AI calls required based on your document model.

        Args:
            title (str): The name of the root document model.
    architecture_file (str): A path to a YAML file containing an AaC-defined document model to evaluate.
    no_pdf (bool): Instructs the plugin to not generate a PDF file, resulting only in a markdown file
    output (str): The location to output generated document.  Default is current working directory.content_only (bool): Instructs the plugin to only produce document content, eliminating additional data such as requirements and test information.
    temperature (float): The temperature passed into the AI text generator.  Default value is 0.2

       Returns:
            The results of the execution of the plugin gen-doc-draft command.
    """

    result = ExecutionResult(plugin_name, "gen-doc-draft", ExecutionStatus.SUCCESS, [])

    gen_doc_draft_result = gen_doc_draft(
        title, architecture_file, no_pdf, output, content_only, temperature
    )
    if not gen_doc_draft_result.is_success():
        return gen_doc_draft_result
    else:
        result.add_messages(gen_doc_draft_result.messages)

    return result


@hookimpl
def register_plugin() -> None:
    """
    Registers information about the plugin for use in the CLI.
    """

    active_context = LanguageContext()
    document_model_aac_file = join(dirname(__file__), document_model_aac_file_name)
    definitions = active_context.parse_and_load(document_model_aac_file)

    document_model_plugin_definition = [
        definition for definition in definitions if definition.name == plugin_name
    ][0]

    plugin_instance = document_model_plugin_definition.instance
    for file_to_load in plugin_instance.definition_sources:
        active_context.parse_and_load(file_to_load)

    plugin_runner = PluginRunner(plugin_definition=document_model_plugin_definition)
    plugin_runner.add_command_callback("gen-doc-outline", run_gen_doc_outline)
    plugin_runner.add_command_callback("gen-doc-draft", run_gen_doc_draft)

    active_context.register_plugin_runner(plugin_runner)
