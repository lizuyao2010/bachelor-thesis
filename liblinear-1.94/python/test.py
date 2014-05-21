from liblinearutil import *
model=load_model('table2.txt.model')
y,x=svm_read_problem('test_table.txt')
p_labs,p_acc,p_vals=predict(y,x,model,'-b 1')
print p_labs