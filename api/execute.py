import subprocess
import os
import time
import datetime
from . tasks import *
from my_App.models import *

def ErrorExtractor(error):
    lines = error.split('\n')
    new_lines = []
    keywords = ['error:']
    for line in lines:
        if 'error:' in line:
            new_lines.append(line.split('error:')[-1].lstrip().rstrip())
    return new_lines
    
def CleanInput(text):
    text = text.lstrip().rstrip()
    special_characters = ['\r',]
    new_text = ""
    for ch in text:
        if ch not in special_characters:
            new_text = new_text + ch
    return new_text

def execute(user, question, file, compiler, cases):
    '''
        Function config
        ---------------------------------------------------------
        INPUT:
        ---------------------------------------------------------
        file : name of input file        (type : str)
        input_cases : input samples      (type : str)
        output_cases : output samples    (type : str)
        ---------------------------------------------------------
        ---------------------------------------------------------
        OUTPUT:
        ---------------------------------------------------------
        (A list)
        if compilation error:
            returns a list containining single element: the error details
        else if size not equal:
            list of single element returning the result
        else:
            a list for the length of output_cases : True/False
        ---------------------------------------------------------
        DANGERS
        ---------------------------------------------------------
            SYSTEM goes down when someone types : rm -rf /
            Does not deal infinite allocation of memory
            does not deal with infinite allocation of time
        ---------------------------------------------------------
    '''
    
    output_file_name = GetTimeStamp() + '.out'.format(datetime.datetime.now())
    command = compiler + " " + file + " -o " + output_file_name + "; ./" + output_file_name
    
    
    answers = []
    elapsed_list = []
    
    for input_case, output_case, description in cases:
        pipein, pipeout = os.pipe()
    
        input_case = CleanInput(input_case)
        output_case = CleanInput(output_case)
        output_case = output_case.split('\n')
        
        os.write(pipeout, bytes(input_case, 'utf-8'))
        os.close(pipeout)
        
        start = time.time()
        s = subprocess.Popen(command , shell=True , stdin=pipein, stdout=subprocess.PIPE, stderr=subprocess.PIPE , close_fds=True)
        elapsed = time.time() - start
        output, error = s.communicate()
        output = output.decode().lstrip().rstrip().split('\n')
        error = error.decode()
        # subprocess.Popen('rm -f ' + file, shell=True)
        subprocess.Popen('rm -f ' + output_file_name, shell=True)
        
        if (error != ''):
            return 400, ErrorExtractor(error)
        elif (len(output) != len(output_case)):
            return 400, 'Output not equal to number of test cases!'
            
        ans = ([output[i]==output_case[i] for i in range(len(output_case))] == [True for i in range(len(output_case))])
        answers.append(ans)
        elapsed_list.append(elapsed)
    
    if (answers == [True for i in range(len(cases))]):
        student = User.objects.get(username=user['username']).profile
        try:
            sub = Submission.objects.get(student=student, question=question)
            sub.time_of_submission = datetime.datetime.now()
            sub.save()
        except:
            sub = Submission(student=student, question=question)
            sub.save()
    
    response = []
    for i in range(len(answers)):
        response.append({
            'result': answers[i],
            'description' : cases[i][2],
            'input_case': cases[i][0],
            'output_case': cases[i][1],
            'elapsed': elapsed_list[i],
        })
    
    return 200, response
   
# FOR DEBUGGING PURPOSES
# def main():
#     input_cases = ""
#     # '''
#     # 4
#     # 1 2
#     # 3 4
#     # 2 5
#     # 3434 56
#     # '''
    
#     output_cases = "Hello World"
#     # '''
#     # 3
#     # 7
#     # 7
#     # 3490
#     # '''
#     print(execute("/home/ubuntu/environment/cmJudge/data/hello-2019-12-28_08:59:08.c", "gcc", input_cases, output_cases))

# if __name__=="__main__":
#     main()
