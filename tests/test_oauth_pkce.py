import pytest

from security.oauth_pkce import (
    verify_challenge,
    redirect_uri_ok,
    bind_state,
    nonce_ok,
    redeem_code
)


def test_s256():
    import hashlib, base64
    challenge = base64.urlsafe_b64encode(hashlib.sha256(b'abc').digest()).rstrip(b'=').decode()
    assert verify_challenge('abc', challenge, 'S256') is True

def test_plain():
    assert verify_challenge('abc', 'abc', 'plain') is True

def test_wrong_verifier():
    assert verify_challenge('abd', 'abc', 'plain') is False

def test_unknown_method():
    assert verify_challenge('abc', 'abc', 'none') is False

def test_redirect_exact():
    assert redirect_uri_ok('https://app.example/cb', 'https://app.example/cb') is True

def test_redirect_slash():
    assert redirect_uri_ok('https://app.example/cb', 'https://app.example/cb/') is False

def test_redirect_prefix():
    assert redirect_uri_ok('https://app.example/cb', 'https://app.example/cb.evil') is False

def test_state_match():
    assert bind_state('s1', 's1') is True

def test_state_mismatch():
    assert bind_state('s1', 's2') is False

def test_nonce_match():
    assert nonce_ok('n1', 'n1') is True

def test_nonce_missing():
    assert nonce_ok('n1', None) is False

def test_redeem_once():
    store = {'c1': {'client': 'web', 'used': False}}
    assert redeem_code(store, 'c1', 'web') is True

def test_redeem_replay():
    store = {'c1': {'client': 'web', 'used': False}}
    assert redeem_code(store, 'c1', 'web') is True
    assert redeem_code(store, 'c1', 'web') is False

def test_wrong_client():
    store = {'c1': {'client': 'web', 'used': False}}
    assert redeem_code(store, 'c1', 'mobile') is False

def test_empty_code():
    assert redeem_code({}, '', 'web') is False
