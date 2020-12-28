from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.

def index(request):

    page = request.GET.get('page', '1') # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list':page_obj}

    return render(request, 'qna/question_list.html', context)

def detail(request, question_id):

    question = Question.objects.get(id=question_id)
    context = {'question': question}
    
    return render(request, 'qna/question_detail.html', context)

def answer_create(request, question_id):
  
#question_id 매개변수에는 url 매핑 정보값이 넘어옴(2, 3 등)
#request 매개변수에는 qna/question_detail.html 에서 textarea에 입력된 데이터가 파이썬 객체에 담겨 넘어옴
#이 값을 추출하기 위한 코드가 request.POST.get('content') : form 데이터항목 중 name 이 content
#Question 모델을 통해 Answer 모델 데이터를 생성하기 위해 question.answer_set.create 사용
#Answer 모델이 Question 모델을 Foreign Key로 참조하고있으므로, question.answer_set 표현사용가능
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    
    return redirect('qna:detail', question_id=question_id)

def question_create(request):
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('qna:index')
    else:
        form = QuestionForm()
    context = {'form':form}  
    return render(request, 'qna/question_form.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('qna:detail', question_id=question_id)
        else:
            form=AnswerForm()
        context = {'question':question, 'form':form}
        return render(request, 'qna/question_detail.html',context)

