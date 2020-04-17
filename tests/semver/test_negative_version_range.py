import pytest

from poetry.core.semver import EmptyConstraint
from poetry.core.semver import NegativeVersionRange
from poetry.core.semver import Version
from poetry.core.semver import VersionRange
from poetry.core.semver import VersionUnion


@pytest.fixture()
def v003():
    return Version.parse("0.0.3")


@pytest.fixture()
def v010():
    return Version.parse("0.1.0")


@pytest.fixture()
def v080():
    return Version.parse("0.8.0")


@pytest.fixture()
def v072():
    return Version.parse("0.7.2")


@pytest.fixture()
def v114():
    return Version.parse("1.1.4")


@pytest.fixture()
def v123():
    return Version.parse("1.2.3")


@pytest.fixture()
def v124():
    return Version.parse("1.2.4")


@pytest.fixture()
def v130():
    return Version.parse("1.3.0")


@pytest.fixture()
def v140():
    return Version.parse("1.4.0")


@pytest.fixture()
def v200():
    return Version.parse("2.0.0")


@pytest.fixture()
def v234():
    return Version.parse("2.3.4")


@pytest.fixture()
def v250():
    return Version.parse("2.5.0")


@pytest.fixture()
def v300():
    return Version.parse("3.0.0")


def test_allows_all(v003, v010, v080, v114, v123, v124, v140, v200, v234, v250, v300):
    range = NegativeVersionRange(v114, "!=" + str(v114))
    assert range.allows_all(EmptyConstraint())

    range = NegativeVersionRange(v114, "!=" + str(v114))
    assert not range.allows_all(v114)
    assert range.allows_all(v124)
    assert range.allows_all(v250)
    assert range.allows_all(v300)

    range = NegativeVersionRange(VersionRange(v200, v300, include_min=True), "!=2.*")
    assert not range.allows_all(v200)
    assert not range.allows_all(v234)
    assert not range.allows_all(v250)
    assert range.allows_all(v300)
    assert range.allows_all(VersionRange(v123, v140))
    assert range.allows_all(VersionRange(v123, v200, include_max=False))
    assert not range.allows_all(VersionRange(v123, v200, include_max=True))


def test_allows_any(v003, v010, v080, v114, v123, v124, v140, v200, v234, v250, v300):
    range = NegativeVersionRange(v114, "!=" + str(v114))
    assert not range.allows_any(EmptyConstraint())

    range = NegativeVersionRange(v114, "!=" + str(v114))
    assert not range.allows_any(v114)
    assert range.allows_any(v124)
    assert range.allows_any(v250)
    assert range.allows_any(v300)

    range = NegativeVersionRange(VersionRange(v200, v300, include_min=True), "!=2.*")
    assert not range.allows_any(v200)
    assert not range.allows_any(v234)
    assert not range.allows_any(v250)
    assert range.allows_any(v300)
    assert range.allows_any(VersionRange(v123, v140))
    assert range.allows_any(VersionRange(v123, v200, include_max=False))
    assert range.allows_any(VersionRange(v123, v200, include_max=True))
    assert not range.allows_any(VersionRange(v200, v300, include_min=True))
    assert range.allows_any(VersionRange())


def test_intersect(v003, v010, v080, v114, v123, v124, v140, v200, v234, v250, v300):
    range = NegativeVersionRange(v114, "!=" + str(v114))
    assert range.intersect(EmptyConstraint()).is_empty()

    range = NegativeVersionRange(v114, "!=" + str(v114))
    assert range.intersect(v114).is_empty()
    assert v124 == range.intersect(v124)

    range = NegativeVersionRange(VersionRange(v200, v300, include_min=True), "!=2.*")
    assert range.intersect(VersionRange(v200, v300, include_min=True)).is_empty()
    assert v300 == range.intersect(
        VersionRange(v200, v300, include_min=True, include_max=True)
    )
    assert VersionRange(v123, v200, include_min=True) == range.intersect(
        VersionRange(v123, v300, include_min=True)
    )
    assert VersionUnion(
        VersionRange(v123, v200, include_min=True), v300
    ) == range.intersect(VersionRange(v123, v300, include_min=True, include_max=True))
