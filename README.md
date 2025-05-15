1. 安装依赖：

```bash
pip install requests
```



2. 获取 GitHub 个人访问令牌：

- 访问 GitHub Settings > Developer settings > Personal access tokens
- 生成一个新的令牌，至少需要 `public_repo` 权限（如果需要 Star 私有仓库，则需要 `repo` 权限）

3. 使用脚本：

```bash
# 从文件读取URL列表
python github_batch_star.py -f urls.txt -token your_github_token

# 直接提供URL文本
python github_batch_star.py -t "https://github.com/user/repo1\nhttps://github.com/user/repo2" -token your_github_token
```

4. 如果不提供 `-token` 参数，脚本会提示你输入 GitHub 用户名和密码 / 令牌

脚本特点：

- 支持从文件或命令行直接输入 URL
- 自动解析多种格式的 GitHub URL
- 提供详细的操作进度和结果统计
- 包含错误处理和认证检查
- 遵循 GitHub API 的最佳实践
