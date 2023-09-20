import statistics as sts
import re

# Task 1: Tạo 1 hàm để đọc file 
def read_file():
    while True:
        try:
            file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
            file_data = open(file_name, 'r')
            print(f"Successfully opened {file_name}\n")
            break
        except:
            print("File cannot be found!\n")
    return file_name,file_data

# Task 2: Tạo 1 hàm để phân tích dữ liệu trong tệp, với arg là 1 list
def AnalyFile(list_data):
    print("**** ANALYZING ****\n")
    # tạo 2 list để lưu các giá trị valid và invalid
    invalid_list = []
    valid_list = []
    for data in list_data:
        answer = data.strip().split(',')
        if len(answer) != 26:
            invalid_list.append(data)
            print(f"Invalid line of data: does not contain exactly 26 values:\n{data}")
        elif not re.match('N[0-9]{8}',answer[0]):
            invalid_list.append(data)
            print(f"Invalid line of data: N# is invalid:\n{data}")
        else:
            valid_list.append(data)

    if len(invalid_list) == 0:
        print('No errors found!\n')

    print("**** REPORT ****\n")
    print(f"Total valid lines of data: {len(valid_list)}\n")
    print(f"Total invalid lines of data: {len(invalid_list)}\n")
    return valid_list

# Task 3: Tạo 1 hàm để chấm điểm bài thi valid
def Score(valid_list):
    # Tạo ra answer_key như là 1 list
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(',')

    #Tính điểm cho từng sinh viên và đưa vào 1 dict với key=stu_name, value=score_list
    # score_list chứa các giá trị 4,0,-1 tương ứng với câu trả lời đúng, bỏ trống, sai
    Score_dict = dict()
    for i in range(len(valid_list)):
        answer_list = valid_list[i].strip().split(',')
        stu_name,stu_answer = answer_list[0], answer_list[1:27]
        
        Score_list = [4 if a == b else -1 if b else 0
                        for a,b in zip(answer_key,stu_answer)]
        
        Score_dict[stu_name] = Score_list
    return Score_dict

# Task 3: Tạo 1 hàm để phân tích điểm thi
def ScoreAna(Score_dict):
    Gen_score = list(Score_dict.values())
    
    # dùng map để tính tổng các score_list.
    Sum_score = list(map(sum,Gen_score))
    
    # dùng filter để lọc các điểm > 80 và đưa vào 1 list, rồi tính len của list đó.
    Number_HighScore = len(list(filter(lambda x: x > 80,Sum_score)))
    print(f"Total student of high scores: {Number_HighScore}\n")
    
    # Tính mean bằng module statistics và in ra kết quả
    print("Mean (average) score: {:.2f}\n".format(round(sts.mean(Sum_score),2)))

    # In ra điểm cao nhất
    print(f"Highest score: {max(Sum_score)}\n")

    # In ra điểm thấp nhất
    print(f"Lowest score: {min(Sum_score)}\n")

    #In ra miền giá trị của điểm
    print(f"Range of scores: {max(Sum_score) - min(Sum_score)}\n")

    # In ra giá trị median bằng statistics
    print(f"Median score: {sts.median(Sum_score)}\n")

#Task 3: Tính số lượng câu hỏi bị bỏ qua nhiều nhất, bị trả lời sai nhiều nhất và vị trí.
def AnswerCount(Score_dict, d):
    Gen_score = list(Score_dict.values())

    #Tạo 1 list chứa giá trị là tuple(số thứ tự câu hỏi, điểm[-1,0])
    ASlist = []
    for i in range(len(Gen_score)):
        #Tạo ra một list chưa tuple(số thứ tự câu hỏi, điểm[-1,0]) bằng enumerate
        Slist = list(filter(lambda x: x[1] == d, list(enumerate(Gen_score[i], start=1))))
        ASlist.extend(Slist)
    
    #Sắp xếp lại ASlist theo thứ tự câu hỏi
    ASlist.sort(key=lambda x: x[0])

    #Tìm xem tuple nào xuất hiện nhiều nhất bằng cách tạo 1 dictionary với
    # key = tuple và value = số lần xuất hiện
    ASdict = dict()
    for sc in ASlist:
        ASdict[sc] = ASdict.get(sc,0) + 1

    # Tạo 1 chuỗi để return ra kết quả
    ASstr = ''
    for k,v in ASdict.items():
        if v == max(list(ASdict.values())):
            ASstr += "{} - {} - {:.2f}, ".format(k[0],v,v/len(Gen_score))
    return ASstr


# Task 4: Viết hàm ghi kết quả vào file
def write_file(Score_dict, file_name):
    filename = file_name.strip('.txt')
    
    with open(f'{filename}_grades.txt', 'w') as writeFile:
        for k,v in Score_dict.items():
            stscore = "{},{}\n".format(k,sum(v))
            writeFile.write(stscore)

if __name__ == "__main__":
    while True:
        # Thực hiện task 1
        file_name, file_data = read_file()
        list_data = file_data.readlines()

        # Thực hiện task 2
        valid_list = AnalyFile(list_data)
       
        # Thực hiện task 3
        Score_dict = Score(valid_list)
        ScoreAna(Score_dict)
        
        ASstr0 = AnswerCount(Score_dict, 0).strip(', ')
        print(f"Question that most people skip: {ASstr0}\n")
        
        ASstr1 = AnswerCount(Score_dict, -1).strip(', ')
        print(f"Question that most people answer incorrectly: {ASstr1}\n")

        # Thực hiện task 4
        write_file(Score_dict, file_name)

        # Hỏi người dùng có muốn thực hiện tiếp file khác không
        # Y là có và tiếp tục, N là không và dừng chương trình
        Useranswer = input("Do you want to analysis other file(Y/N): ")
        if Useranswer == 'Y':
            print(">>> {:=<10} RESTART {:=>10}\n".format('',''))
            pass
        else:
            break