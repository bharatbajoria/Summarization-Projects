# -*- coding: utf-8 -*-
"""final data prep summ.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16oUipECZElb_gU6VC5nA_GxvmBnnEGA-
"""

def lcs(X,Y,m,n,Corp_Participants,word_tokenize):
  #X,Y=removing_corp(X,Y,Corp_Participants)
  x="BERT-Presentation"
  y="KL-Presentation"
  if x in (X or Y):
    X=X.replace(x,"")
    Y=Y.replace(x,"")
  if y in (Y or X):
    Y=Y.replace(y,"")
    X=X.replace(x,"")
  if X[0]==" ":
    X=X[1:]
  if Y[0]==" ":
    Y=Y[1:]

  X=data_clean(X)
  Y=data_clean(Y)
  X=X.split(".")
  Y=Y.split(".")
  common_text=""
  for i in X:
    if (i in Y and len(word_tokenize(i))>3):
      common_text+=i+"."
  
  return common_text

def finding_complement(X,Y,Corp_Participants):
  #returns Y-X
  X,Y=removing_corp(X,Y,Corp_Participants)
  x="BERT-Presentation"
  y="KL-Presentation"
  if x in (X or Y):
    X=X.replace(x,"")
    Y=Y.replace(x,"")
  if y in (Y or X):
    Y=Y.replace(y,"")
    X=X.replace(x,"")
  if (len(X)>0 and len(Y)>0):
    if X[0]==" ":
      X=X[1:]
    if Y[0]==" ":
      Y=Y[1:]  
    X=data_clean(X)
    Y=data_clean(Y)
    X=X.split(".")
    Y=Y.split(".")
    common_text=[]
    for i in X:
      if i in Y:
        common_text.append(i)
    
    for i in common_text:
      if i in Y :
        index_i=Y.index(i)
        Y.pop(index_i)
    
    text=""
    for i in Y:
      text+=i+"."

    return text
  else:
    return data_clean(Y)

def data_clean(train_data):
  train_data=train_data.replace("\n\n"," ")
  train_data=train_data.replace("\n"," ")
  train_data=train_data.replace(", "," ")
  train_data=train_data.replace(" ,"," ")
  train_data=train_data.replace(","," ")
  train_data=train_data.replace("-"," ")
  train_data=train_data.replace("    "," ")
  train_data=train_data.replace("   "," ")
  train_data=train_data.replace("  "," ") 
  train_data=train_data.replace("<Sentence:","")
  train_data=train_data.replace(">","")
  train_data=train_data.replace("(","")
  train_data=train_data.replace(")","")
  train_data=train_data.replace(".,",".")

  return train_data

def preparing_data_PDFwrite(docs):
  x='Presentaion\n\n'
  count_for_qna=0
  
  for i in range(1,len(docs)):
    if i==1:
      for k in docs[i]:
        y=str(k)
        if y.count("<Sentence:")>0:
          y=y.replace("<Sentence:","")
          y=y.replace(">","")
          y=y.replace("(","")
          y=y.replace(")","")
          y=y.replace(".,",".")
        x+=y +"\n"
      x+="\nQnA\n\n"
    else:
      y=str(docs[i])
      if y.count("<Sentence:")>0:
        y=y.replace("<Sentence:","")
        y=y.replace(">","")
        y=y.replace("(","")
        y=y.replace(")","")
        y=y.replace(".,","")
           
      x+=y
      x+="  \n\n"
      
      
  return x

def preparing_final_data(Bert_data,KL_data,doc_pres,Doc_Answers):
  #Bert_data is str of summarised BERT Data
  #KL_data is str of summarised KL Data
  Corp="CORPORATE PARTICIPANTS"
  Pres="Presentaion"
  QnA="QnA"
  data=""
  index_corp=Bert_data.index(Corp)
  index_pres= Bert_data.index(Pres)
  data+="\n"+Bert_data[index_corp:index_pres]#Adding names of Corp. Participant
  
  #Adding Presentation Bert then KL
  index_pres= Bert_data.index(Pres)
  index_QnA= Bert_data.index(QnA)
  Bert_Pres=Bert_data[index_pres:index_QnA]
  Bert_Pres=Bert_Pres.replace("Presentaion\n","BERT-Presentation")
  data+="PRESENTATION\n\n"+"Original Presentation-\n"+doc_pres+"\n\n"+Bert_Pres

  index_pres= KL_data.index(Pres)
  index_QnA= KL_data.index(QnA)
  KL_Pres=KL_data[index_pres:index_QnA]
  KL_Pres=KL_Pres.replace("Presentaion\n","KL-Presentation")
  data+="\n"+KL_Pres

  #Adding QnA Header
  QnA_count=Bert_data.count("Question-")
  data+="\n\nQnA\n\n"
  for i in range(QnA_count):
    question_id= "Question-"+str(i+1)
    ans_id= "Answer-"+str(i+1)
    #Adding question
    index_ques= Bert_data.index(question_id)
    index_ans= Bert_data.index(ans_id)
    data+="\n\n"+Bert_data[index_ques:index_ans]

    #Adding Bert Answer then KL Answer
    if i!= QnA_count-1:
      question_id= "Question-"+str(i+2)
      ans_id= "Answer-"+str(i+1)    
      index_ques= Bert_data.index(question_id)
      index_ans= Bert_data.index(ans_id)
      data+="\nOriginal Answer-\n"+Doc_Answers[i] +"\nBERT:\n"+Bert_data[index_ans:index_ques]
    else:
      
      ans_id= "Answer-"+str(i+1)    
      
      index_ans= Bert_data.index(ans_id)
      data+="\nOriginal Answer-\n"+Doc_Answers[i]+ "\n\nBERT:\n"+Bert_data[index_ans:]
#Adding KL Answer
    if i!= QnA_count-1:
      question_id= "Question-"+str(i+2)
      ans_id= "Answer-"+str(i+1)    
      index_ques= KL_data.index(question_id)
      index_ans= KL_data.index(ans_id)
      data+="\nKL:\n"+KL_data[index_ans:index_ques]
    else:
      
      ans_id= "Answer-"+str(i+1)    
      
      index_ans= KL_data.index(ans_id)
      data+="\nKL:\n"+KL_data[index_ans:]
  
  return data

def removing_corp(Bert_data,KL_data,Corp_Participants):
  if "BERT-Presentation" in Bert_data:
    Bert_data=Bert_data.replace("BERT-Presentation ","")
  if "KL-Presentation" in KL_data:
    KL_data=KL_data.replace("KL-Presentation ","")
  
  for i in Corp_Participants:
    if i in Bert_data:
      Bert_data=Bert_data.replace(i," ")
    if i in KL_data:
      KL_data=KL_data.replace(i," ")
  
  return Bert_data,KL_data

def preparing_final_data_test(Bert_data,KL_data,doc_pres,Doc_Answers,Corp_Participants,word_tokenize):
  #Bert_data is str of summarised BERT Data
  #KL_data is str of summarised KL Data
  
  Corp="CORPORATE PARTICIPANTS"
  Pres="Presentaion"
  QnA="QnA"
  data=""
  index_corp=Bert_data.index(Corp)
  index_pres= Bert_data.index(Pres)
  #Corp_Participants=Bert_data[index_corp:index_pres][:]
  data+="\n"+Bert_data[index_corp:index_pres]#Adding names of Corp. Participant

  Corp_Participants=Corp_Participants.split("  ")
  Corp_Participants=Corp_Participants[1:]
  x=Corp_Participants[-1]
  
  Corp_Participants[-1]= x[0:(len(Corp_Participants[-1])-1)]

  #Adding Presentation Bert then KL
  index_pres= Bert_data.index(Pres)
  index_QnA= Bert_data.index(QnA)
  Bert_Pres=Bert_data[index_pres:index_QnA]
  Bert_Pres=Bert_Pres.replace("Presentaion\n","BERT-Presentation")
  data+="PRESENTATION\n\n"+"Original Presentation-\n"+"Sentence Count -"+str(len(doc_pres.split("."))) +"\n"
  data+=doc_pres+"\n\n"+"Sentence Count -"+str(len(Bert_Pres.split("."))) +"\n"+Bert_Pres

  index_pres= KL_data.index(Pres)
  index_QnA= KL_data.index(QnA)
  KL_Pres=KL_data[index_pres:index_QnA]
  KL_Pres=KL_Pres.replace("Presentaion\n","KL-Presentation")  
  data+="\n"+"Sentence Count -"+str(len(KL_Pres.split("."))) +"\n"+KL_Pres
# Adding 4 sets of KL and Bert and complements
  Bert_Pres,KL_Pres=removing_corp(Bert_Pres,KL_Pres,Corp_Participants)
  #removing corporate names
  Pres_bert_and_kl=lcs(Bert_Pres,KL_Pres,len(Bert_Pres),len(KL_Pres),Corp_Participants,word_tokenize)  
  Pres_bert_and_klc=finding_complement(Pres_bert_and_kl,Bert_Pres,Corp_Participants)
  
  Pres_bertc_and_kl=finding_complement(Pres_bert_and_kl,KL_Pres,Corp_Participants)
  Pres_bertc_and_kl=finding_complement(Pres_bert_and_klc,Pres_bertc_and_kl,Corp_Participants)
  
  Pres_bertc_and_klc= finding_complement(Bert_Pres,doc_pres,Corp_Participants)
  Pres_bertc_and_klc= finding_complement(Pres_bertc_and_kl,Pres_bertc_and_klc,Corp_Participants)
  Pres_bertc_and_klc= finding_complement(Pres_bert_and_kl,Pres_bertc_and_klc,Corp_Participants)
  data+="\n" +"KL and Bert\n\n"   + Pres_bert_and_kl
  data+="\n\n"+"Bert~ and KL\n\n" + Pres_bertc_and_kl
  data+="\n\n"+"Bert and KL~\n\n" + Pres_bert_and_klc
  data+="\n\n"+"Bert~ and KL~\n\n"+ Pres_bertc_and_klc



  #Adding QnA Header
  QnA_count=Bert_data.count("Question-")
  data+="\n\nQnA\n\n"
  for i in range(QnA_count):
    question_id= "Question-"+str(i+1)
    ans_id= "Answer-"+str(i+1)
    #Adding question
    index_ques= Bert_data.index(question_id)
    index_ans= Bert_data.index(ans_id)
    data+="\n\n"+Bert_data[index_ques:index_ans]

    #Adding Bert Answer then KL Answer
    if i!= QnA_count-1:
      question_id= "Question-"+str(i+2)
      ans_id= "Answer-"+str(i+1)    
      index_ques= Bert_data.index(question_id)
      index_ans= Bert_data.index(ans_id)
      Bert_ans=Bert_data[index_ans:index_ques]
      sent_count_doc=len(Doc_Answers[i].split("."))
      sent_count_bert=len(Bert_ans.split("."))
      data+="\nOriginal Answer-\n"+"Sentence Count-"+str(sent_count_doc)+"\n"+Doc_Answers[i]
      data+= "\n"+"Sentence Count-"+str(sent_count_bert)+"\nBERT:\n"+Bert_ans
    
    else:     
      ans_id= "Answer-"+str(i+1)     
      index_ans= Bert_data.index(ans_id)
      Bert_ans=Bert_data[index_ans:]
      sent_count_doc=len(Doc_Answers[i].split("."))
      sent_count_bert=len(Bert_ans.split("."))
      data+="\nOriginal Answer-\n"+"Sentence Count-"+str(sent_count_doc)+"\n"+Doc_Answers[i]
      data+="\n"+"Sentence Count-"+str(sent_count_bert)+"\nBERT:\n"+Bert_ans
#Adding KL Answer
    if i!= QnA_count-1:
      question_id= "Question-"+str(i+2)
      ans_id= "Answer-"+str(i+1)    
      index_ques= KL_data.index(question_id)
      index_ans= KL_data.index(ans_id)
      KL_ans=KL_data[index_ans:index_ques]
      sent_count_kl=len(KL_ans.split("."))
      data+="\nKL:\n"+"Sentence Count"+str(sent_count_kl)+"\n"+KL_ans
    else:      
      ans_id= "Answer-"+str(i+1)         
      index_ans= KL_data.index(ans_id)
      KL_ans=KL_data[index_ans:]
      sent_count_kl=len(KL_ans.split("."))
      data+="\nKL:\n"+"Sentence Count"+str(sent_count_kl)+"\n"+KL_ans
    
    Bert_ans,KL_ans=removing_corp(Bert_ans,KL_ans,Corp_Participants)
    Ans_bert_and_kl=lcs(Bert_ans,KL_ans,len(Bert_ans),len(KL_ans),Corp_Participants,word_tokenize)  
    Ans_bert_and_klc =finding_complement(Ans_bert_and_kl,Bert_ans,Corp_Participants)
    
    Ans_bertc_and_kl =finding_complement(Ans_bert_and_kl,KL_ans,Corp_Participants)
    Ans_bertc_and_kl =finding_complement(Ans_bert_and_klc,Ans_bertc_and_kl,Corp_Participants)    
    
    Ans_bertc_and_klc= finding_complement(Bert_ans, Doc_Answers[i],Corp_Participants)
    Ans_bertc_and_klc= finding_complement(Ans_bertc_and_kl,Ans_bertc_and_klc,Corp_Participants)
    Ans_bertc_and_klc= finding_complement(Ans_bert_and_kl,Ans_bertc_and_klc,Corp_Participants)
    data+="\n" +"KL and Bert\n\n"   + Ans_bert_and_kl
    data+="\n\n"+"Bert~ and KL\n\n" + Ans_bertc_and_kl
    data+="\n\n"+"Bert and KL~\n\n" + Ans_bert_and_klc
    data+="\n\n"+"Bert~ and KL~\n\n"+ Ans_bertc_and_klc


  
  return data