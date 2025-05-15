import requests
import argparse
import re
from typing import List, Tuple, Optional
from getpass import getpass

# 配置GitHub API
BASE_URL = "https://api.github.com"
AUTH_HEADERS = {}

def setup_auth(token: Optional[str] = None) -> None:
    """设置GitHub API认证信息"""
    if token:
        AUTH_HEADERS["Authorization"] = f"token {token}"
    else:
        print("请输入GitHub认证信息：")
        username = input("用户名: ")
        password = getpass("密码 (或个人访问令牌): ")
        AUTH_HEADERS["Authorization"] = f"token {password}"

def parse_repo_url(url: str) -> Optional[Tuple[str, str]]:
    """解析GitHub仓库URL，返回(owner, repo)元组"""
    # 匹配常见的GitHub URL格式
    patterns = [
        r"github.com/([^/]+)/([^/]+?)(?:\.git)?$",
        r"github.com/([^/]+)/([^/]+?)/?$"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url.strip())
        if match:
            return match.group(1), match.group(2)
    return None

def star_repo(owner: str, repo: str) -> bool:
    """Star一个GitHub仓库"""
    url = f"{BASE_URL}/user/starred/{owner}/{repo}"
    response = requests.put(url, headers=AUTH_HEADERS)
    
    if response.status_code == 204:
        print(f"已成功Star仓库: {owner}/{repo}")
        return True
    elif response.status_code == 404:
        print(f"错误: 仓库 {owner}/{repo} 不存在或您没有访问权限")
        return False
    elif response.status_code == 401:
        print("认证失败，请检查您的凭证")
        return False
    else:
        print(f"未知错误: {response.status_code} - {response.text}")
        return False

def process_file(file_path: str) -> None:
    """从文件中读取URL并批量Star"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = file.readlines()
        process_urls(urls)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def process_text(text: str) -> None:
    """处理文本中的URL并批量Star"""
    urls = text.strip().split('\n')
    process_urls(urls)

def process_urls(urls: List[str]) -> None:
    """处理URL列表并批量Star"""
    if not urls:
        print("没有提供任何URL")
        return
    
    total = len(urls)
    success = 0
    
    for i, url in enumerate(urls, 1):
        url = url.strip()
        if not url:
            continue
            
        print(f"[{i}/{total}] 处理: {url}")
        repo_info = parse_repo_url(url)
        
        if repo_info:
            owner, repo = repo_info
            if star_repo(owner, repo):
                success += 1
        else:
            print(f"错误: 无法解析URL: {url}")
    
    print(f"\n处理完成! 总共: {total}, 成功: {success}, 失败: {total - success}")

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="批量Star GitHub仓库")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="包含GitHub URL的文件路径")
    group.add_argument("-t", "--text", help="直接提供GitHub URL文本")
    parser.add_argument("-token", "--token", help="GitHub个人访问令牌")
    
    args = parser.parse_args()
    
    # 设置认证
    setup_auth(args.token)
    
    # 检查API访问权限
    test_response = requests.get(f"{BASE_URL}/user", headers=AUTH_HEADERS)
    if test_response.status_code != 200:
        print("认证失败，请检查您的凭证")
        return
    
    # 处理输入
    if args.file:
        process_file(args.file)
    elif args.text:
        process_text(args.text)

if __name__ == "__main__":
    main()    