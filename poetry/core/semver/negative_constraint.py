from .version import Version
from .version_constraint import VersionConstraint
from .version_range import VersionRange


class NegativeVersionRange(VersionConstraint):
    def __init__(
        self, version_range, pretty_constraint
    ):  # type: (VersionRange, str) -> None
        self._version_range = version_range
        self._pretty_constraint = pretty_constraint

        # Checking range
        if not isinstance(version_range, Version):
            min_ = version_range.min
            max_ = version_range.max

            if min_ is None or max_ is None:
                raise ValueError("Invalid negative range")

            if min_.precision != max_.precision:
                raise ValueError("Invalid negative range")

            if not version_range.include_min or version_range.include_max:
                raise ValueError("Invalid negative range")

    @property
    def version_range(self):  # type: () -> VersionRange
        return self._version_range

    def is_empty(self):  # type: () -> bool
        return not self._version_range.is_any()

    def is_any(self):  # type: () -> bool
        return not self._version_range.is_empty()

    def allows(self, version):  # type: (Version) -> bool
        return not self._version_range.allows(version)

    def allows_any(self, other):  # type: (VersionConstraint) -> bool
        if other.is_empty():
            return False

        if other.is_any():
            return True

        return not self._version_range.allows_all(other)

    def allows_all(self, other):  # type: (VersionConstraint) -> bool
        if other.is_empty():
            return True

        if other.is_any():
            return False

        return not self._version_range.allows_any(other)

    def intersect(self, other):  # type: (VersionConstraint) -> VersionConstraint
        return VersionRange().difference(self._version_range).intersect(other)

    def __eq__(self, other):  # type: () -> bool
        if not isinstance(other, NegativeVersionRange):
            return False

        return self._version_range == other.version_range

    def __str__(self):  # type: () -> str
        return self._pretty_constraint

    def __repr__(self):  # type () -> str
        return "<NegativeVersionRange ({}, {})>".format(
            str(self._version_range), str(self)
        )
