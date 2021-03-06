from flake8_debugger import check_code_for_debugger_statements, format_debugger_message
from nose.tools import assert_equal


# Python 3 detects the col as the column with the execution brackets rather than the function name. So we will attempt both when necessary.


class Flake8DebuggerTestCases(object):
    def generate_error_statement(self, line, col, item_type, item_found, name_used):
        return {
            'message': format_debugger_message(item_type, item_found, name_used),
            'line': line,
            'col': col
        }


class TestImportCases(Flake8DebuggerTestCases):
    def test_import_multiple(self):
        result = check_code_for_debugger_statements('import math, ipdb, collections')
        assert_equal(result, [self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb')])

    def test_import(self):
        result = check_code_for_debugger_statements('import pdb')
        assert_equal(result, [self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb')])

    def test_import_interactive_shell_embed(self):
        result = check_code_for_debugger_statements('from IPython.terminal.embed import InteractiveShellEmbed')
        assert_equal(result, [self.generate_error_statement(1, 0, 'import', 'IPython.terminal.embed', 'IPython.terminal.embed')])

    def test_import_both_same_line(self):
        result = check_code_for_debugger_statements('import pdb, ipdb')
        result = sorted(result, key=lambda debugger: debugger['message'])
        assert_equal(
            result,
            [
                self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
            ]
        )

    def test_import_math(self):
        result = check_code_for_debugger_statements('import math')
        assert_equal(result, [])

    def test_import_noqa(self):
        result = check_code_for_debugger_statements('import ipdb # noqa')
        assert_equal(result, [])


class TestModuleSetTraceCases(Flake8DebuggerTestCases):
    def test_import_ipython_terminal_embed_use_InteractiveShellEmbed(self):
        result = check_code_for_debugger_statements('from IPython.terminal.embed import InteractiveShellEmbed; InteractiveShellEmbed()()')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'IPython.terminal.embed', 'IPython.terminal.embed'),
                    self.generate_error_statement(1, 58, 'trace method', 'IPython.terminal.embed', 'InteractiveShellEmbed')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'IPython.terminal.embed', 'IPython.terminal.embed'),
                    self.generate_error_statement(1, 79, 'trace method', 'IPython.terminal.embed', 'InteractiveShellEmbed')
                ]
            )

    def test_import_ipdb_use_set_trace(self):
        result = check_code_for_debugger_statements('import ipdb;ipdb.set_trace();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 12, 'trace method', 'ipdb', 'set_trace')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 26, 'trace method', 'ipdb', 'set_trace')
                ]
            )

    def test_import_pdb_use_set_trace(self):
        result = check_code_for_debugger_statements('import pdb;pdb.set_trace();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
                    self.generate_error_statement(1, 11, 'trace method', 'pdb', 'set_trace')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
                    self.generate_error_statement(1, 24, 'trace method', 'pdb', 'set_trace')
                ]
            )

    def test_import_pdb_use_set_trace_twice(self):
        result = check_code_for_debugger_statements('import pdb;pdb.set_trace() and pdb.set_trace();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
                    self.generate_error_statement(1, 11, 'trace method', 'pdb', 'set_trace'),
                    self.generate_error_statement(1, 31, 'trace method', 'pdb', 'set_trace')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
                    self.generate_error_statement(1, 24, 'trace method', 'pdb', 'set_trace'),
                    self.generate_error_statement(1, 44, 'trace method', 'pdb', 'set_trace')
                ]
            )

    def test_import_other_module_as_set_trace_and_use_it(self):
        result = check_code_for_debugger_statements('from math import Max as set_trace\nset_trace()')
        assert_equal(
            result,
            []
        )


class TestImportAsCases(Flake8DebuggerTestCases):
    def test_import_ipdb_as(self):
        result = check_code_for_debugger_statements('import math, ipdb as sif, collections')
        assert_equal(result, [self.generate_error_statement(1, 0, 'import', 'ipdb', 'sif')])


class TestModuleASSetTraceCases(Flake8DebuggerTestCases):
    def test_import_ipdb_as_use_set_trace(self):
        result = check_code_for_debugger_statements('import ipdb as sif;sif.set_trace();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'sif'),
                    self.generate_error_statement(1, 19, 'trace method', 'sif', 'set_trace')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'sif'),
                    self.generate_error_statement(1, 32, 'trace method', 'sif', 'set_trace')
                ]
            )


class TestImportSetTraceCases(Flake8DebuggerTestCases):
    def test_import_set_trace_ipdb(self):
        result = check_code_for_debugger_statements('from ipdb import run, set_trace;set_trace();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 32, 'trace method', 'ipdb', 'set_trace')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 41, 'trace method', 'ipdb', 'set_trace')
                ]
            )

    def test_import_set_trace_pdb(self):
        result = check_code_for_debugger_statements('from pdb import set_trace; set_trace();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
                    self.generate_error_statement(1, 27, 'trace method', 'pdb', 'set_trace')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'pdb', 'pdb'),
                    self.generate_error_statement(1, 36, 'trace method', 'pdb', 'set_trace')
                ]
            )

    def test_import_set_trace_ipdb_as_and_use(self):
        result = check_code_for_debugger_statements('from ipdb import run, set_trace as sif; sif();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 40, 'trace method', 'ipdb', 'sif')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 43, 'trace method', 'ipdb', 'sif')
                ]
            )

    def test_import_set_trace_ipdb_as_and_use_with_conjunction_and(self):
        result = check_code_for_debugger_statements('from ipdb import run, set_trace as sif; True and sif();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 49, 'trace method', 'ipdb', 'sif')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 52, 'trace method', 'ipdb', 'sif')
                ]
            )

    def test_import_set_trace_ipdb_as_and_use_with_conjunction_or(self):
        result = check_code_for_debugger_statements('from ipdb import run, set_trace as sif; True or sif();')
        try:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 48, 'trace method', 'ipdb', 'sif')
                ]
            )
        except AssertionError:
            assert_equal(
                result,
                [
                    self.generate_error_statement(1, 0, 'import', 'ipdb', 'ipdb'),
                    self.generate_error_statement(1, 51, 'trace method', 'ipdb', 'sif')
                ]
            )

    def test_import_set_trace_ipdb_as_and_use_with_conjunction_or_noqa(self):
        result = check_code_for_debugger_statements('from ipdb import run, set_trace as sif; True or sif(); # noqa')
        try:
            assert_equal(
                result,
                []
            )
        except AssertionError:
            pass

    def test_import_set_trace_ipdb_as_and_use_with_conjunction_or_noqa_import_only(self):
        result = check_code_for_debugger_statements('from ipdb import run, set_trace as sif # noqa\nTrue or sif()')
        try:
            assert_equal(
                result,
                [self.generate_error_statement(2, 8, 'trace method', 'ipdb', 'sif')]
            )
        except AssertionError:
            assert_equal(
                result,
                [self.generate_error_statement(2, 11, 'trace method', 'ipdb', 'sif')]
            )
