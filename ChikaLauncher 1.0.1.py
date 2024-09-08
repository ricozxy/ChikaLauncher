# © 2024 米柑喵 保持所有权利

import argparse
import subprocess
import os
import sys
import signal

Version = "1.0.1"
WELCOME_MESSAGE = f"""
Welcome to ChikaLauncher! The author of this program is 米柑喵.
Current version: {Version}


You can add parameters to use this program.
-c : the program to be executed
-d : the path to open when executing the program
-a : additional parameters

Example: ChikaLauncher
.\ChikaLauncher -c “D:\\You.exe” -d “D:\\Ruby” -a “-c D:\\Chika\\config.yml”

ChikaLauncher will locate “D:\\Ruby” and execute “D:\\You.exe -c D:\\Chika\\config.yml”.
"""

# 用于保存子进程对象
process = None


# 捕获终止信号并杀掉子进程
def handle_termination_signal(signum, frame):
    global process
    if process and process.poll() is None:  # 如果进程还在运行
        sys.stderr.write("\nTerminating the process...\n")
        process.terminate()  # 尝试优雅终止
        try:
            process.wait(timeout=5)  # 等待子进程结束
        except subprocess.TimeoutExpired:
            sys.stderr.write("Force killing the process...\n")
            process.kill()  # 强制杀死进程
    sys.exit(0)


# 自定义 ArgumentParser 来处理无效参数的错误
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'Error: {message}\n')
        print(WELCOME_MESSAGE)
        sys.exit(2)


# 主程序
def main():
    global process

    # 确保 sys.stdout 和 sys.stderr 正常
    if not sys.stdout:
        sys.stdout = open(os.devnull, 'w')
    if not sys.stderr:
        sys.stderr = open(os.devnull, 'w')

    # 捕获终止信号（如Ctrl+C，和NSSM停止信号）
    signal.signal(signal.SIGINT, handle_termination_signal)  # Ctrl+C
    signal.signal(signal.SIGTERM, handle_termination_signal)  # NSSM停止信号

    # 创建参数解析器
    parser = CustomArgumentParser(description="ChikaLauncher - 静默执行cmd指令", add_help=False)

    # 定义启动参数
    parser.add_argument('-c', '--command', help="需要执行的程序")
    parser.add_argument('-d', '--directory', help="执行程序时需要打开的路径")
    parser.add_argument('-a', '--args', nargs=argparse.REMAINDER, help="需要附加的参数")

    # 如果没有提供参数，显示欢迎信息
    if len(sys.argv) == 1:
        print(WELCOME_MESSAGE)
        sys.exit(0)

    # 解析命令行参数
    args = parser.parse_args()

    # 如果没有提供有效的 -c 参数，显示欢迎信息
    if not args.command:
        print(WELCOME_MESSAGE)
        sys.exit(0)

    # 如果指定了路径，则切换到该路径；否则，切换到执行程序所在的目录
    if args.directory:
        os.chdir(args.directory)
    else:
        # 获取执行程序所在目录
        command_dir = os.path.dirname(os.path.abspath(args.command))
        os.chdir(command_dir)

    # 构建最终的执行命令
    command = f'"{args.command}"'
    if args.args:
        command += ' ' + ' '.join(args.args)

    # 执行命令并显示输出
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 实时显示标准输出
        for stdout_line in iter(process.stdout.readline, ""):
            sys.stdout.write(stdout_line)

        process.stdout.close()

        # 等待进程结束
        process.wait()

        # 显示标准错误输出
        if process.returncode != 0:
            for stderr_line in iter(process.stderr.readline, ""):
                sys.stderr.write(stderr_line)
            process.stderr.close()

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()