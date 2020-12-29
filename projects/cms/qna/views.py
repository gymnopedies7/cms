from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib import messages
# Create your views here.

def index(request):

    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') #검색어
    so = request.GET.get('so','recent') #정렬기준

    #정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    #조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    
    #페이징처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list':page_obj, 'page':page, 'kw':kw, 'so':so }

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

@login_required(login_url='common:login')
def question_create(request):
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('qna:index')
    else:
        form = QuestionForm()
    context = {'form':form}  
    return render(request, 'qna/question_form.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('qna:detail', question_id=question_id)
        else:
            form=AnswerForm()
        context = {'question':question, 'form':form}
        return render(request, 'qna/question_detail.html',context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('qna:detail', question_id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('qna:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'qna/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('qna:detail', question_id=question.id)
    question.delete()
    return redirect('qna:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('qna:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('qna:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'qna/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('qna:detail', question_id=answer.question.id)