import time
from apotheosession.opencode_schema import (
    make_text_part,
    make_reasoning_part,
    make_tool_part,
    make_step_finish_part,
    make_user_message,
    make_assistant_message,
    build_info,
    parse_iso_timestamp,
)


def test_parse_iso_timestamp():
    ts = parse_iso_timestamp("2026-05-23T10:32:34.584Z")
    assert isinstance(ts, int)
    assert ts > 1700000000000


def test_make_text_part():
    part = make_text_part("hello", "msg_1", "ses_1")
    assert part["type"] == "text"
    assert part["text"] == "hello"
    assert part["messageID"] == "msg_1"
    assert part["sessionID"] == "ses_1"


def test_make_reasoning_part():
    part = make_reasoning_part("msg_1", "ses_1")
    assert part["type"] == "reasoning"
    assert "encrypted" in part["text"]


def test_make_tool_part_pending():
    part = make_tool_part("call_abc", "msg_1", "ses_1", raw='{"command":"ls"}')
    assert part["type"] == "tool"
    assert part["callID"] == "call_abc"
    assert part["state"]["status"] == "pending"


def test_make_tool_part_completed():
    part = make_tool_part("call_abc", "msg_1", "ses_1", output="file1.txt\n")
    assert part["type"] == "tool"
    assert part["state"]["status"] == "completed"
    assert part["state"]["output"] == "file1.txt\n"


def test_make_step_finish_part():
    part = make_step_finish_part(input_t=100, output_t=50, reason="stop")
    assert part["type"] == "step-finish"
    assert part["tokens"]["input"] == 100
    assert part["tokens"]["output"] == 50


def test_make_user_message():
    msg = make_user_message("hello", "ses_1")
    assert msg.info["role"] == "user"
    assert len(msg.parts) == 1
    assert msg.parts[0]["text"] == "hello"


def test_make_assistant_message():
    msg = make_assistant_message("parent_1", "ses_1")
    assert msg.info["role"] == "assistant"
    assert msg.info["parentID"] == "parent_1"


def test_build_info_minimal():
    info = build_info(title="Test", directory="/tmp")
    assert info.title == "Test"
    assert info.directory == "/tmp"
    assert info.projectID == "global"
