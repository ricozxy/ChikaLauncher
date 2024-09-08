# ChikaLauncher

ChikaLauncher is a program that enables all programs to bind to [NSSM](https://nssm.cc/) and locate a specific directory to open.

## Scope of Use

When a program does not support NSSM calls, ChikaLauncher can be used to help the program be supported by NSSM.

## How to Use

You can add parameters to use this program:

- `-c` : the program to be executed
- `-d` : the path to open when executing the program
- `-a` : additional parameters

### Example: ChikaLauncher

```bash
.\ChikaLauncher -c "D:\You.exe" -d "D:\Ruby" -a "-c D:\Chika\config.yml"
```

ChikaLauncher will locate `D:\Ruby` and execute:

```bash
"D:\You.exe -c D:\Chika\config.yml"
```

After that, in NSSM:

- **Path**: Fill in the absolute location of ChikaLauncher
- **Startup directory**: Can be filled freely
- **Arguments**: Fill in `-c`, `-d`, `-a`, and any other parameters

---

ChikaLauncher 是一个能使所有程序都能绑定到 NSSM 中并可在特定目录中打开的实用程序。

## 使用范围

当程序不支持 NSSM 调用时，可以使用 ChikaLauncher 帮助程序支持 NSSM。

## 使用方法

您可以添加参数来使用本程序：

- `-c`：要执行的程序
- `-d`：执行程序时打开的路径
- `-a`：附加参数

### 示例：ChikaLauncher

```bash
.\ChikaLauncher -c "D:\You.exe" -d "D:\Ruby" -a "-c D:\Chika\config.yml"
```

ChikaLauncher 会找到 `D:\Ruby` 并执行：

```bash
"D:\You.exe -c D:\Chika\config.yml"
```

之后，在 NSSM 中：

- **Path**：填入 ChikaLauncher 的绝对位置
- **Startup directory**：自由填写
- **Arguments**：填入 `-c`、`-d`、`-a` 和其他参数
