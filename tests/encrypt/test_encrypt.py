import pytest
from challenges.challenge_encrypt_message import encrypt_message


def test_encrypt_message():
    assert encrypt_message("Hello World!", 4) == "!dlroW o_lleH"
    assert encrypt_message("Hello World!", 20) == "!dlroW olleH"
    with pytest.raises(TypeError, match="tipo inválido para key"):
        encrypt_message("Hello World!", 4.5)
    with pytest.raises(TypeError, match="tipo inválido para message"):
        encrypt_message(123, 4)
