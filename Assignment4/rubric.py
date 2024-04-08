import os
import argparse
import glob
import re

from subprocess import Popen, PIPE

import traceback

def get_python_stdout(py_file):
    try:
        process = Popen(["python", py_file], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
    except Exception:
        traceback.print_exc()

    output = output.decode('ascii').strip().split('\n')
    return output

def q1(q1_file):
    
    marks = 5
    W, B, B_std = 23, 43 + 5, 5
    
    output = get_python_stdout(q1_file) 
    assert len(output) == 1, "%s, %d lines" % (q1_file, len(output))
    output = output[0]

    if not ("w=" in output or "w =" in output): 
        print ("%s: w missing: -2 marks" % q1_file)
        marks -= 2
    if not ("b=" in output or "b =" in output): 
        print ("%s: w missing: -2 marks" % q1_file)
        marks -= 2
    
    eq = output.split("=")
    try:
        assert "w" in eq[0] and "b" in eq[1], "%s: %s" % (q1_file, output)
    except AssertionError:
        marks = 0
        return marks

    w = float(re.split(' |, |,', eq[1].split(',')[0].strip())[0])
    b = float(eq[-1].strip())
    
    with open(q1_file, 'r') as f:
        lines = list(f.readlines())

    print ("%s: %d lines of code" % (q1_file, len(lines)))
    
    if (W-w)**2 > 0.07 and (W-w)**2 < 0.1:
        print ("W_answer=%f, w=%f: -1.5 marks" % (W, w))
        marks -= 1.5
    elif (W-w)**2 > 0.1:
        print ("W_answer=%f, w=%f: 0 marks" % (W, w))
        marks = 0
        return marks

    if (B-b)**2 >= 4:
        print ("B_answer=%f, b=%f: -1.5 marks" % (B, b))
        marks -= 1.5
    
    return marks

def q2(q2_file, regression_type):

    assert regression_type in ["linear", "logistic"]
    
    marks = 15
    
    """ #HARDCODED
    if regression_type == "linear":
        r2_baseline, mean, std = 0.56, 0.55, 0.02
    else:
        r2_baseline, mean, std = 0.55, 0.50, 0.006
    
    with occupation + missing values
    Full dataset accuracy: full: 0.824782, train: 0.824944, test: 0.826384
    70-15-15 Cross validation boxplot: mean=0.760915, std=0.004763
    without occupation
    Full dataset accuracy: full: 0.824864, train: 0.825763, test: 0.822835
    70-15-15 Cross validation boxplot: mean=0.761388, std=0.004407
    """

    output = get_python_stdout(q2_file)

    if regression_type == "linear":
        full_r2 = float(output[0].split(' ')[-1])
        # 0.52 -> 0.58, avg 0.56
        if full_r2 > 0.56:
            marks = 10
            if full_r2 > 0.57:
                print ("%s: r2 score %f" % (q2_file, full_r2))
        else:
            marks = 10 * (full_r2 - 0.52) / 0.04
            print ("full dataset r2 not in (0.52, 0.56+ - max=0.59): -%d" % (10-marks))
    else:
        col = output[0].split(':')
        # 0.52 -> 0.59, avg 0.55
        full_r2 = float(col[2].split(',')[0].strip())
        train_r2 = float(col[3].split(',')[0].strip())
        test_r2 = float(col[-1].strip())
        
        if full_r2 > 0.82:
            marks = 10
            if full_r2 > 0.8247:
                print ("%s: r2 score %f" % (q2_file, full_r2))
        else:
            print ("full dataset r2", full_r2, "!=0.8247: -3 marks")
            marks = 7
        
        if train_r2 > 0.82486:
            if train_r2 > 0.82487:
                print ("%s: r2 score %f" % (q2_file, full_r2))
        else:
            print ("train dataset r2", train_r2, "!=0.82486: -3 marks")
            marks -= 3 
        
        if test_r2 > 0.8262:
            if test_r2 > 0.82487:
                print ("%s: r2 score %f" % (q2_file, full_r2))
        else:
            print ("test dataset r2", test_r2, "!=0.8262: -3 marks")
            marks -= 3
        
    regression_marks = marks

    # cross validation
    eq = output[1].split('=')
    mean = float(eq[1].split(',')[0].split(' ')[0].strip())
    std = float(eq[-1].strip())
    
    if regression_type == "linear":
        # 0.559254, std=0.015131
        marks = 5
        if (mean - 0.559)**2 > 1e-3 or (std-0.015)**2 > 1e-4:
            print ("mean and std marks", mean, "!=0.559", std, "!=0.015: -3 marks")
            marks -= 3
    else:
        # 0.761 0.0044
        marks = 5
        if ((mean - 0.761)**2 > 1e-4 and mean < 0.761) or ((std-0.0044)**2 > 1e-5 and std > 0.0044):
            print ("mean and std marks", mean, "!=0.761", std, "!=0.0044: -3 marks")
            marks -= 3
    
    cross_val_marks = marks

    return regression_marks + cross_val_marks

if __name__ == "__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("assignment_dir", help="Directory with #folders=#students")
    args = ap.parse_args()

    students = glob.glob(os.path.join(args.assignment_dir, '*'))

    for student in students:
        q1_file = glob.glob(os.path.join(student, '*_gradient.py'))[0]
        print ("q1: %d marks" % q1(q1_file))
        
        try:
            q2_file = glob.glob(os.path.join(student, '*_linear_regression.py'))[0]
            print ("q2: %d marks" % q2(q2_file, regression_type="linear"))
        except Exception:
            try:
                q2_file = glob.glob(os.path.join(student, '*_logistic_regression.py'))[0]
                print ("q2: %d marks" % q2(q2_file, regression_type="logistic"))
            except Exception:
                print (q1_file, "SYNTAX ERROR")

        print ('.'*50, '\n', '.'*50, '\n\n')
