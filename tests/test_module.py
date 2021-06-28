""" Test module module """
import pytest

from aries_staticagent.module import Module, InvalidModule, route


def test_module_def():
    """Test module creationg and special attributes of module"""

    class TestModule(Module):
        """Simple module for testing"""

        DOC_URI = "test_doc_uri/"
        PROTOCOL = "test_protocol"
        VERSION = "1.0"


def test_module_missing_attrs():
    """Test that defining a module without required attributes raises
    an error.
    """
    # pylint: disable=unused-variable

    with pytest.raises(InvalidModule):

        class TestModule1(Module):
            """Simple module for testing"""

            DOC_URI = "test_doc_uri/"
            PROTOCOL = "test_protocol"

    with pytest.raises(InvalidModule):

        class TestModule2(Module):
            """Simple module for testing"""

            DOC_URI = "test_doc_uri/"
            VERSION = "1.0"

    with pytest.raises(InvalidModule):

        class TestModule3(Module):
            """Simple module for testing"""

            PROTOCOL = "test_protocol"
            VERSION = "1.0"


def test_routes_construction():
    """Test that module routes are properly constructed."""

    class TestModule(Module):
        """Simple module for testing"""

        DOC_URI = "test_doc_uri/"
        PROTOCOL = "test_protocol"
        VERSION = "1.0"

        @route
        async def test(self, msg):
            """This should create a route"""

        @route
        async def test1(self, msg):
            """This should create another route"""

    mod = TestModule()
    assert mod.routes
    assert "test_doc_uri/test_protocol/1.0.0/test" in mod.routes
    assert "test_doc_uri/test_protocol/1.0.0/test1" in mod.routes


def test_module_type_helper():
    """Test that module routes are properly constructed."""

    class TestModule(Module):
        """Simple module for testing"""

        DOC_URI = "test_doc_uri/"
        PROTOCOL = "test_protocol"
        VERSION = "1.0"

    mod = TestModule()
    assert mod.type("test") == "test_doc_uri/test_protocol/1.0.0/test"
    assert mod.type("test", doc_uri="") == "test_protocol/1.0.0/test"
    assert mod.type("test", protocol="protocol") == "test_doc_uri/protocol/1.0.0/test"
    assert mod.type("test", version="2.0") == "test_doc_uri/test_protocol/2.0.0/test"


def test_route_bad_input():
    """Test that calling route directly with bad inputs raises error."""
    with pytest.raises(ValueError):
        route([1, 2, "garbage"])
