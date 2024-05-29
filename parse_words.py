import json
import re

def parse_vocabulary_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = {}
    current_classification = None
    current_category = None
    parsing_words = False
    parsing_category = False
    
    word_pattern = re.compile(r"(\w+)［([^］]+)］(\w+)\.\s(.+?)(?:（([^）]+)）)?$")

    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("按") and line.endswith("分类"):
            current_classification = line
            data[current_classification] = {}
            print(f'分类方式: {current_classification}')
            parsing_words = False
            i += 1
            continue
        
        if line == "":
            if i + 4 < len(lines) and all(lines[i + j].strip() == "" for j in range(1, 4)):
                parsing_category = True
                i += 1
            else:
                i += 1
            continue
        
        if parsing_category:
            current_category = line.strip()
            if current_category in ["事物属性", "人类生活", "品德品行", "万事万物", "心理", "行为", "状态", "语言"]:
                print(f'---- 细分类别: {current_category}')
                i += 1
                continue
            print(f'------ 类别: {current_category}')
            data[current_classification][current_category] = []
            parsing_category = False
            parsing_words = True
            i += 1
            continue
        
        if parsing_words:
            # 处理单词
            # print(f'------ 单词: {line}')
            word_match = word_pattern.match(line)
            if word_match:
                word = word_match.group(1)
                pronunciation = word_match.group(2)
                part_of_speech = word_match.group(3)
                meaning = word_match.group(4)
                synonyms = word_match.group(5) # 注意group(5)可能为None
                synonymses = synonyms.split(", ") if synonyms else ""
                details = {"word": word, "pronunciation": pronunciation, "part_of_speech": part_of_speech, "meaning": meaning, "synonyms": synonymses,  "memory_tips": "", "example_sentence": ""}
                i += 1
                while i < len(lines):
                    if lines[i].strip() == "" and i + 4 < len(lines) and all(lines[i + j].strip() == "" for j in range(1, 4)):
                        break
                    new_match = word_pattern.match(lines[i]) #发现新单词了
                    if new_match:
                        i -= 1
                        break
                    if lines[i].strip() == "":
                        i += 1
                        continue
                    if lines[i].strip().startswith("【记 】"):
                        details["memory_tips"] = lines[i].strip()[4:]
                        i += 1
                        continue
                    elif lines[i].strip().startswith("【例 】"):
                        details["example_sentence"] = lines[i].strip()[4:]
                        i += 1
                        continue
                    else:
                        break
                    
                # print(details)
                data[current_classification][current_category].append(details)
                i += 1
                continue
            else:
                i += 1
                continue
                # print(f'未解析的词组，请手动添加: {line}, category: {current_category}, current_classification:{current_classification} ', )
       

    return data

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
def main():
    vocabulary_data = parse_vocabulary_file('./words_list.txt')
    output_file = 'vocabulary.json'
    save_to_json(vocabulary_data, output_file)
    
    
if __name__ == '__main__':
    main()