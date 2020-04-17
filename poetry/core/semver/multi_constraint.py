from typing import Tuple

from .version_constraint import VersionConstraint


class MultiVersionConstraint(VersionConstraint):
    def __init__(self, *constraints):  # type: (Tuple[VersionConstraint]) -> None
        self._constraints = constraints

    @property
    def constraints(self):  # type: () -> Tuple[VersionConstraint]
        return self._constraints

    @classmethod
    def of(cls, *constraints):  # type: (Tuple[VersionConstraint]) -> VersionConstraint
        from .version_range import VersionRange

        if len(constraints) == 1:
            return constraints[0]

        new_constraints = []
        for current_constraint in constraints:
            i = 0
            while i < len(new_constraints):
                constraint = new_constraints[i]
                if isinstance(current_constraint, VersionRange) and isinstance(
                    constraint, VersionRange
                ):
                    if (
                        current_constraint.min
                        and not current_constraint.max
                        and not constraint.min
                        and constraint.max
                    ):
                        constraint = VersionRange(
                            current_constraint.min,
                            constraint.max,
                            include_min=current_constraint.include_min,
                            include_max=constraint.include_max,
                        )
                        new_constraints[i] = constraint
                        current_constraint = None
                    elif (
                        constraint.min
                        and not constraint.max
                        and not current_constraint.min
                        and current_constraint.max
                    ):
                        constraint = VersionRange(
                            constraint.min,
                            current_constraint.max,
                            include_min=constraint.include_min,
                            include_max=current_constraint.include_max,
                        )
                        new_constraints[i] = constraint
                        current_constraint = None

                i += 1

            if current_constraint:
                new_constraints.append(current_constraint)

        if len(new_constraints) == 1:
            return new_constraints[0]

        return MultiVersionConstraint(*constraints)

    def allows(self, version):  # type: ("Version") -> bool
        for constraint in self._constraints:
            if not constraint.allows(version):
                return False

        return True

    def allows_any(self, other):  # type: (VersionConstraint) -> bool
        for constraint in self._constraints:
            if not constraint.allows_any(other):
                return False

        return True

    def allows_all(self, other):  # type: (VersionConstraint) -> bool
        for constraint in self._constraints:
            if not constraint.allows_all(other):
                return False

        return True

    def __eq__(self, other):  # type: (VersionConstraint) -> bool
        if not isinstance(other, MultiVersionConstraint):
            return False

        if len(self._constraints) != len(other.constraints):
            return False

        for constraint in self._constraints:
            if constraint not in other.constraints:
                return False

        return True

    def __hash__(self):
        h = hash(self._constraints[0])

        for c in self._constraints[1:]:
            h ^= hash(c)

        return h

    def __str__(self):  # type: () -> str
        return ",".join(str(c) for c in self._constraints)

    def __repr__(self):
        return "<MultiVersionConstraint ({})>".format(str(self))
