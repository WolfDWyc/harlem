import importlib.metadata
from pathlib import Path
from typing import List

from harlem.models.har import Har
from harlem.models.har import Page, Log, Entry, Creator

_harlem_version = "0.0.0+unknown"

# Taken from https://github.com/python-poetry/poetry/issues/273#issuecomment-1877789967
try:
    # Try to get the version of the current package if
    # it is running from a distribution.
    _harlem_version = importlib.metadata.version("harlem")
except importlib.metadata.PackageNotFoundError:
    # Fall back on getting it from a local pyproject.toml.
    # This works in a development environment where the
    # package has not been installed from a distribution.
    import toml

    pyproject_toml_file = Path(__file__).parent.parent.parent / "pyproject.toml"
    if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
        _harlem_version = toml.load(pyproject_toml_file)["tool"]["poetry"]["version"]
        # Indicate it might be locally modified or unreleased.
        _harlem_version = _harlem_version + "+"


def to_har_model(pages: List[Page], entries: List[Entry]) -> Har:
    return Har(
        log=Log(
            version="1.2",
            creator=Creator(name="Harlem", version=_harlem_version),
            entries=entries,
            pages=pages,
        )
    )
