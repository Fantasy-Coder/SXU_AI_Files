def read_scores(filename):
    scores = []
    failing_students = []

    with open(filename, 'r', encoding='utf-8') as file:
        next(file) 
        for line in file:
            line = line.strip()
            if line:
                try:
                    parts = line.split(',')
                    name = parts[1]
                    score = float(parts[2])
                    scores.append(score)

                    if score < 60:
                        failing_students.append(name)
                except (ValueError, IndexError):
                    print(f"无效成绩数据: {line}")
    return scores, failing_students

def calculate_average(scores):
    if scores:
        average = sum(scores) / len(scores)
        return round(average, 2)
    else:
        return 0.0

def save_failing_students(filename, failing_students):
    with open(filename, 'w', encoding='utf-8') as file:
        for student in failing_students:
            file.write(student + "\n")

def main():
    scores_file = 'E:\\Python code\\project\\scores.txt'
    failing_students_file = 'E:\\Python code\\project\\不及格人员名单.txt'
    scores, failing_students = read_scores(scores_file)
    average_score = calculate_average(scores)
    print(f"平均成绩: {average_score}")
    save_failing_students(failing_students_file, failing_students)
    print("不及格人员名单已保存到 '不及格人员名单.txt'。")
if __name__ == '__main__':
    main()
