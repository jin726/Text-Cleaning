import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 下载NLTK中的停用词数据包（如果尚未下载）
nltk.download('stopwords')
nltk.download('punkt')

# 获取英语停用词列表
stop_words = set(stopwords.words('english'))

def remove_stop_words(input_file, output_file):
    # 打开并读取原始文件
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # 使用NLTK的word_tokenize进行分词
    words = word_tokenize(text)

    # 过滤停用词
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # 重新组合成文本
    cleaned_text = ' '.join(filtered_words)

    # 保存清洗后的文本
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"清洗后的文本已保存到 {output_file}")

# 使用
input_file = 'ross_cleaned.txt'  # 输入文件路径
output_file = 'output_Ross.txt'  # 输出文件路径
remove_stop_words(input_file, output_file)
print("处理完成！")