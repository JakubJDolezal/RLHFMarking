import json
import os

from django.shortcuts import render, redirect, get_object_or_404
from transformers import AutoConfig, AutoModelForCausalLM, LlamaTokenizer
from accelerate import init_empty_weights

from .models import Response, Question
from .forms import ScoreForm, QuestionForm
from django.views.decorators.csrf import csrf_exempt

f = open('config.json')

config = json.load(f)


config_model = AutoConfig.from_pretrained(config['model_directory'] + '\\config.json')
with init_empty_weights():
    model = AutoModelForCausalLM.from_config(config_model)
model.tie_weights()
from accelerate import load_checkpoint_and_dispatch, init_empty_weights

model = load_checkpoint_and_dispatch(
    model, config['model_directory'], device_map="auto", no_split_module_classes=["LlamaDecoderLayer"]
)
tokenizer = LlamaTokenizer.from_pretrained(config['model_directory'])
device = 'cuda:0'


def generate_bot_response(message, temperature):
    inputs = tokenizer.encode_plus(message, return_tensors='pt')
    len_input = inputs['input_ids'].size(dim=1)
    outputs = model.generate(inputs['input_ids'].to(device), max_length=int(config["max_response"]), temperature=temperature).cpu()
    response = tokenizer.decode(outputs[0][len_input:], skip_special_tokens=True)
    # response = 'Random Response'
    return response

def question_responses_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    responses = Response.objects.filter(question=question)
    return render(request, 'myapp/question_responses.html', {'question': question, 'responses': responses})

@csrf_exempt
def question_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']

            # Here we should generate responses for the question. For this
            # example, we will simply create a single response.
            prepending = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. User: "
            appending = "Bot:"
            temperature=1
            response_text = generate_bot_response(prepending + question + appending, temperature)
            response = Response(question=question, text=response_text)
            response.save()

            return redirect('response_view')
    else:
        form = QuestionForm()
    return render(request, 'question_form.html', {'form': form})


# Remember to update score_view and response_view to include questions

def home_view(request):
    return render(request, 'home.html')


def response_view(request):
    responses = Response.objects.all().order_by('question')
    return render(request, 'response_list.html', {'responses': responses})



@csrf_exempt
def score_view(request, response_id):
    response = Response.objects.get(pk=response_id)
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            response.score = form.cleaned_data['score']
            response.save()
            return redirect('response_view')
    else:
        form = ScoreForm(initial={'score': response.score})
    return render(request, 'score_form.html', {'form': form, 'response': response})
