import re
import sys


def clean_irwin_text(text):
    """清洗Terence Irwin译本"""
    lines = text.split('\n')
    cleaned_lines = []

    # 跳过标题和引言，找到正文开始
    start_index = 0
    for i, line in enumerate(lines):
        if 'BOOK' in line and 'I' in line:
            start_index = i
            break

    for line in lines[start_index:]:
        line = line.strip()

        # 跳过空行
        if not line:
            continue

        # 删除页码（如 1094a, 1095b等）
        line = re.sub(r'\b\d{4}[ab]\b', '', line)

        # 删除章节标记（如 ¡ì1, ¡ì2等）
        line = re.sub(r'¡ì\d+', '', line)

        # 删除纯数字行（页码）
        if re.match(r'^\d+$', line):
            continue

        # 删除章节标题行（如 [Happiness], [Ends and Goods]等）
        if re.match(r'^\[.*\]$', line):
            continue

        # 删除纯标题行（全大写或短标题）
        if line.isupper() and len(line) < 50:
            continue

        # 删除BOOK标记
        if line.startswith('BOOK') or line.startswith('Book'):
            continue

        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines


def clean_ross_text(text):
    """清洗W.D. Ross译本"""
    lines = text.split('\n')
    cleaned_lines = []

    # 跳过开头的元数据
    start_index = 0
    for i, line in enumerate(lines):
        if 'BOOK I' in line:
            start_index = i + 1
            break

    for line in lines[start_index:]:
        line = line.strip()

        # 跳过空行
        if not line:
            continue

        # 删除纯数字行（章节号）
        if re.match(r'^\d+$', line):
            continue

        # 删除BOOK标记
        if line.startswith('BOOK'):
            continue

        # 删除纯标题行（全大写短行）
        if line.isupper() and len(line) < 50:
            continue

        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines


def split_into_sentences(lines):
    """将文本分句，确保每个句子独立成行"""
    sentences = []

    for line in lines:
        # 按句号、问号、感叹号分割
        # 但要注意缩写词（如 e.g., i.e.等）
        parts = re.split(r'(?<!\be\.g)(?<!\bi\.e)(?<!\bviz)(?<!\bMr)(?<!\bDr)(?<!\bMrs)(?<!\bMs)(?<=[.!?])\s+', line)

        for part in parts:
            part = part.strip()
            if part and len(part) > 10:  # 过滤太短的片段
                sentences.append(part)

    return sentences


def clean_text_file(input_text, translator='irwin'):
    """主清洗函数"""

    # 根据译者选择清洗方法
    if translator.lower() == 'irwin':
        cleaned_lines = clean_irwin_text(input_text)
    else:
        cleaned_lines = clean_ross_text(input_text)

    # 分句处理
    sentences = split_into_sentences(cleaned_lines)

    # 进一步清理：删除重复空格
    sentences = [re.sub(r'\s+', ' ', s).strip() for s in sentences]

    # 删除太短的句子（可能是残留标记）
    sentences = [s for s in sentences if len(s) > 20]

    return sentences


# 读取上传的文件
try:
    # 尝试多种编码读取第一个文件（Irwin译本）
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    irwin_text = None
    for encoding in encodings:
        try:
            with open('Terence Irwin_30-78.txt', 'r', encoding=encoding) as f:
                irwin_text = f.read()
            print(f"Irwin文件使用 {encoding} 编码读取成功")
            break
        except UnicodeDecodeError:
            continue

    if irwin_text is None:
        raise Exception("无法读取Irwin文件，尝试了所有编码")

    # 尝试多种编码读取第二个文件（Ross译本）
    ross_text = None
    for encoding in encodings:
        try:
            with open('W. D. Ross_1-49.txt', 'r', encoding=encoding) as f:
                ross_text = f.read()
            print(f"Ross文件使用 {encoding} 编码读取成功")
            break
        except UnicodeDecodeError:
            continue

    if ross_text is None:
        raise Exception("无法读取Ross文件，尝试了所有编码")

    # 清洗文本
    print("正在清洗Terence Irwin译本...")
    irwin_cleaned = clean_text_file(irwin_text, 'irwin')

    print("正在清洗W.D. Ross译本...")
    ross_cleaned = clean_text_file(ross_text, 'ross')

    # 保存清洗后的文本
    with open('irwin_cleaned.txt', 'w', encoding='utf-8') as f:
        for sentence in irwin_cleaned:
            f.write(sentence + '\n')

    with open('ross_cleaned.txt', 'w', encoding='utf-8') as f:
        for sentence in ross_cleaned:
            f.write(sentence + '\n')

    print(f"\n清洗完成！")
    print(f"Irwin译本：{len(irwin_cleaned)} 个句子")
    print(f"Ross译本：{len(ross_cleaned)} 个句子")
    print(f"\n清洗后的文件已保存为：")
    print(f"- irwin_cleaned.txt")
    print(f"- ross_cleaned.txt")

    # 显示前5个句子作为示例
    print("\n=== Irwin译本示例（前5句）===")
    for i, sent in enumerate(irwin_cleaned[:5], 1):
        print(f"{i}. {sent[:100]}...")

    print("\n=== Ross译本示例（前5句）===")
    for i, sent in enumerate(ross_cleaned[:5], 1):
        print(f"{i}. {sent[:100]}...")

except FileNotFoundError:
    print("错误：找不到文件。请确保文件名正确。")
except Exception as e:
    print(f"发生错误：{e}")