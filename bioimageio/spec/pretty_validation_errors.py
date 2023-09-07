from pprint import pformat
from types import TracebackType
from typing import Any, List, Type, Union

from pydantic import ValidationError

from bioimageio.spec.summary import format_loc

try:
    from IPython.core.getipython import get_ipython
    from IPython.core.interactiveshell import InteractiveShell

    class PrettyValidationError(ValueError):
        """Wrap a pydantic.ValidationError to custumize formatting."""

        def __init__(self, validation_error: ValidationError):
            super().__init__()
            self.error = validation_error

        def __str__(self):
            errors: List[str] = []
            for e in self.error.errors(include_url=False):
                ipt_lines = pformat(e["input"], sort_dicts=False, depth=1, compact=True, width=30).split("\n")
                if len(ipt_lines) > 2:
                    ipt_lines[1:-1] = ["..."]

                ipt = " ".join([il.strip() for il in ipt_lines])

                errors.append(f"\n{format_loc(e['loc'])}\n  {e['msg']} [type={e['type']}, input={ipt}]")

            return f"{self.error.error_count()} validation errors for {self.error.title}:{''.join(errors)}"

    def _custom_exception_handler(
        self: InteractiveShell,
        etype: Type[ValidationError],
        evalue: ValidationError,
        tb: TracebackType,
        tb_offset: Any = None,
    ):
        assert issubclass(etype, ValidationError)
        assert isinstance(evalue, ValidationError)

        stb: Union[List[Union[str, Any]], Any] = self.InteractiveTB.structured_traceback(etype, PrettyValidationError(evalue), tb, tb_offset=tb_offset)  # type: ignore
        if isinstance(stb, list):
            orig_stb = list(stb)
            stb: List[Any] = []
            for line in orig_stb:
                if isinstance(line, str) and "pydantic" in line and "__tracebackhide__" in line:
                    # ignore pydantic internal frame in traceback
                    continue
                stb.append(line)

        self._showtraceback(etype, PrettyValidationError(evalue), stb)  # type: ignore

    def enable_pretty_validation_errors_in_ipynb():
        """A modestly hacky way to display prettified validaiton error messages and traceback
        in interactive Python notebooks"""
        ipy = get_ipython()
        if ipy is not None:
            ipy.set_custom_exc((ValidationError,), _custom_exception_handler)

except ImportError:

    def enable_pretty_validation_errors_in_ipynb():
        return
