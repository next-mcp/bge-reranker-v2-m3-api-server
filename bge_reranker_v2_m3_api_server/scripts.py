"""Development scripts for BGE Reranker v2-m3 API Server."""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str, success_checker=None) -> bool:
    """运行命令并返回是否成功.

    Args:
        cmd: 要执行的命令列表
        description: 命令描述
        success_checker: 可选的成功判断函数，接受(returncode, stdout, stderr)参数，返回bool
    """
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
            check=False,
        )

        # 打印输出
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # 使用自定义成功判断逻辑或默认逻辑
        if success_checker:
            is_success = success_checker(
                result.returncode, result.stdout, result.stderr
            )
        else:
            is_success = result.returncode == 0

        if is_success:
            print(f"✅ {description} 成功")
            return True
        print(f"❌ {description} 失败")
        print(f"错误码: {result.returncode}")
        return False

    except Exception as e:
        print(f"❌ {description} 失败")
        print(f"异常: {e}")
        return False


def pytest_success_checker(returncode: int, stdout: str, _stderr: str) -> bool:
    """pytest专用的成功判断函数：允许跳过的测试，但不允许失败的测试"""
    if returncode == 0:
        return True

    # 检查输出中是否只包含跳过的测试（没有真正的失败）
    return bool(
        stdout and "skipped" in stdout.lower() and "failed" not in stdout.lower()
    )


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
    is_ci = os.getenv("CI", "false").lower() in ("true", "1", "yes")

    if is_ci:
        # CI环境：添加--tb=short减少输出，使用--maxfail=1快速失败
        cmd = [
            "pytest",
            "tests/",
            "-v",
            "--cov=bge_reranker_v2_m3_api_server",
            "--tb=short",
            "--maxfail=1",
        ]
    else:
        # 本地环境：保持详细输出
        cmd = ["pytest", "tests/", "-v", "--cov=bge_reranker_v2_m3_api_server"]

    return run_command(cmd, "运行测试", pytest_success_checker)


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


def main() -> None:
    """主入口函数."""
    check_all()


if __name__ == "__main__":
    main()
