from click.testing import CliRunner
from typing import Tuple
from unittest import TestCase

from aac.execute.aac_execution_result import ExecutionStatus
from aac.execute.command_line import cli, initialize_cli

from aac_doc_mdl.document_model_impl import (
    plugin_name,
    gen_doc_outline,
    gen_doc_draft,
    gen_doc_vcrm,
)


class TestDocumentModel(TestCase):

    def test_gen_doc_outline(self):

        # TODO: Write success and failure unit tests for gen_doc_outline
        self.fail("Test not yet implemented.")

    def run_gen_doc_outline_cli_command_with_args(
        self, args: list[str]
    ) -> Tuple[int, str]:
        """Utility function to invoke the CLI command with the given arguments."""
        initialize_cli()
        runner = CliRunner()
        result = runner.invoke(cli, ["gen-doc-outline"] + args)
        exit_code = result.exit_code
        std_out = str(result.stdout)
        output_message = std_out.strip().replace("\x1b[0m", "")
        return exit_code, output_message

    def test_cli_gen_doc_outline(self):
        args = []

        # TODO: populate args list, or pass empty list for no args
        exit_code, output_message = self.run_gen_doc_outline_cli_command_with_args(args)

        # TODO:  perform assertions against the output message
        self.assertEqual(0, exit_code)  # asserts the command ran successfully
        self.assertTrue(len(output_message) > 0)  # asserts the command produced output
        # TODO:  assert the output message is correct

    def test_cli_gen_doc_outline_failure(self):
        args = []

        # TODO: populate args list, or pass empty list for no args
        exit_code, output_message = self.run_gen_doc_outline_cli_command_with_args(args)

        # TODO:  perform assertions against the output message
        self.assertNotEqual(
            0, exit_code
        )  # asserts the command did not run successfully
        self.assertTrue(len(output_message) > 0)  # asserts the command produced output
        # TODO:  assert the output message contains correct failure message

    def test_gen_doc_draft(self):

        # TODO: Write success and failure unit tests for gen_doc_draft
        self.fail("Test not yet implemented.")

    def run_gen_doc_draft_cli_command_with_args(
        self, args: list[str]
    ) -> Tuple[int, str]:
        """Utility function to invoke the CLI command with the given arguments."""
        initialize_cli()
        runner = CliRunner()
        result = runner.invoke(cli, ["gen-doc-draft"] + args)
        exit_code = result.exit_code
        std_out = str(result.stdout)
        output_message = std_out.strip().replace("\x1b[0m", "")
        return exit_code, output_message

    def test_cli_gen_doc_draft(self):
        args = []

        # TODO: populate args list, or pass empty list for no args
        exit_code, output_message = self.run_gen_doc_draft_cli_command_with_args(args)

        # TODO:  perform assertions against the output message
        self.assertEqual(0, exit_code)  # asserts the command ran successfully
        self.assertTrue(len(output_message) > 0)  # asserts the command produced output
        # TODO:  assert the output message is correct

    def test_cli_gen_doc_draft_failure(self):
        args = []

        # TODO: populate args list, or pass empty list for no args
        exit_code, output_message = self.run_gen_doc_draft_cli_command_with_args(args)

        # TODO:  perform assertions against the output message
        self.assertNotEqual(
            0, exit_code
        )  # asserts the command did not run successfully
        self.assertTrue(len(output_message) > 0)  # asserts the command produced output
        # TODO:  assert the output message contains correct failure message

    def test_gen_doc_vcrm(self):

        # TODO: Write success and failure unit tests for gen_doc_vcrm
        self.fail("Test not yet implemented.")

    def run_gen_doc_vcrm_cli_command_with_args(
        self, args: list[str]
    ) -> Tuple[int, str]:
        """Utility function to invoke the CLI command with the given arguments."""
        initialize_cli()
        runner = CliRunner()
        result = runner.invoke(cli, ["gen-doc-vcrm"] + args)
        exit_code = result.exit_code
        std_out = str(result.stdout)
        output_message = std_out.strip().replace("\x1b[0m", "")
        return exit_code, output_message

    def test_cli_gen_doc_vcrm(self):
        args = []

        # TODO: populate args list, or pass empty list for no args
        exit_code, output_message = self.run_gen_doc_vcrm_cli_command_with_args(args)

        # TODO:  perform assertions against the output message
        self.assertEqual(0, exit_code)  # asserts the command ran successfully
        self.assertTrue(len(output_message) > 0)  # asserts the command produced output
        # TODO:  assert the output message is correct

    def test_cli_gen_doc_vcrm_failure(self):
        args = []

        # TODO: populate args list, or pass empty list for no args
        exit_code, output_message = self.run_gen_doc_vcrm_cli_command_with_args(args)

        # TODO:  perform assertions against the output message
        self.assertNotEqual(
            0, exit_code
        )  # asserts the command did not run successfully
        self.assertTrue(len(output_message) > 0)  # asserts the command produced output
        # TODO:  assert the output message contains correct failure message
