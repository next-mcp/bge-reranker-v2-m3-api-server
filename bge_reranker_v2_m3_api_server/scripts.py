"""Development scripts for BGE Reranker v2-m3 API Server."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """运行命令并返回是否成功."""
    print(f"🔍 {description}...")
    print(f"执行命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        print(f"✅ {description} 成功")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败")
        print(f"错误码: {e.returncode}")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False


def format_code() -> bool:
    """格式化代码."""
    return run_command(["ruff", "format", "."], "代码格式化")


def lint_code() -> bool:
    """检查代码质量."""
    return run_command(["ruff", "check", ".", "--fix"], "代码质量检查")


def type_check() -> bool:
    """类型检查."""
    return run_command(["pyright"], "类型检查")


def run_tests() -> bool:
    """运行测试."""
    return run_command(
        ["pytest", "tests/", "-v", "--cov=bge_reranker_v2_m3_api_server"],
        "运行测试",
    )


def install_pre_commit() -> None:
    """安装 pre-commit 钩子."""
    print("🪝 安装 pre-commit 钩子...")
    success = run_command(["pre-commit", "install"], "安装 pre-commit 钩子")
    if success:
        print("🎉 pre-commit 钩子安装成功!")
    else:
        print("❌ pre-commit 钩子安装失败!")
        sys.exit(1)


def update_pre_commit() -> None:
    """更新 pre-commit 仓库."""
    print("🔄 更新 pre-commit 仓库...")
    success = run_command(["pre-commit", "autoupdate"], "更新 pre-commit 仓库")
    if success:
        print("🎉 pre-commit 仓库更新成功!")
    else:
        print("❌ pre-commit 仓库更新失败!")
        sys.exit(1)


def check_all() -> None:
    """执行所有检查."""
    print("🚀 开始执行所有代码质量检查...")
    print("=" * 50)

    checks = [
        ("代码格式化", format_code),
        ("代码质量检查", lint_code),
        ("类型检查", type_check),
        ("运行测试", run_tests),
    ]

    failed_checks = []

    for name, check_func in checks:
        print(f"\n📋 执行: {name}")
        print("-" * 30)

        if not check_func():
            failed_checks.append(name)

        print("-" * 30)

    print("\n" + "=" * 50)
    print("📊 检查结果总结:")

    if failed_checks:
        print(f"❌ 失败的检查 ({len(failed_checks)}):")
        for check in failed_checks:
            print(f"  - {check}")
        print(f"\n✅ 成功的检查 ({len(checks) - len(failed_checks)}):")
        for name, _ in checks:
            if name not in failed_checks:
                print(f"  - {name}")
        sys.exit(1)
    else:
        print(f"✅ 所有检查都通过了! ({len(checks)}/{len(checks)})")
        print("🎉 代码质量良好, 可以提交!")


def run_format() -> None:
    """格式化代码的入口函数."""
    success = format_code()
    if not success:
        sys.exit(1)


def run_lint() -> None:
    """代码检查的入口函数."""
    success = lint_code()
    if not success:
        sys.exit(1)


def test_entry() -> None:
    """测试的入口函数，用于命令行调用."""
    success = run_tests()
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)


def main() -> None:
    """主入口函数."""
    check_all()


if __name__ == "__main__":
    main()
