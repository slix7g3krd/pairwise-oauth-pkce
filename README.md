# pairwise-oauth-pkce

OAuth 授权服务一接移动端，PKCE 就被绕：code_challenge 只存不验，plain 和 S256 混用没有区分；redirect_uri 用前缀匹配，多一个斜杠就跳到外站；state 没有和会话绑定，nonce 只写进 ID Token 不校验；授权码可重复兑换，并发请求拿到两个 token；client_secret 在公共客户端里硬编码。security/oauth_pkce.py 是核心，tests/test_oauth_pkce.py 15个红。要修的是：S256 强制；redirect_uri 精确匹配；state/nonce 绑定；授权码一次性；公共客户端不存 secret。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：其他；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
