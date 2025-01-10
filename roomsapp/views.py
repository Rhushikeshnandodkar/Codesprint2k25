from django.shortcuts import render, redirect
from .models import *
from sentence_transformers import SentenceTransformer, util
# Create your views here.

rel_model = SentenceTransformer('all-MiniLM-L6-v2') 

def create_room(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['title']
            text = request.POST['text']
            room = Room.objects.create(room_name=name, content=text, creator=request.user)
            room.save()
            print(room)
            return redirect("room_details", room_id=room.id)
        return render(request, "create_room.html")
    else:
        return redirect('home')
    
def room_details(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room=room.id)
    return render(request, "room_details.html", {'room': room, 'messages': messages})

def dashboard(request):
    if request.user.is_authenticated:
        rooms = Room.objects.filter(creator=request.user)
    else:
        return redirect('/login')
    return render(request, "dashboard.html", {'rooms': rooms})

# def questionsdash(request, room_id):
#     room = Room.objects.get(id=room_id)
#     return render(request, "questdash.html", {'room': room})

def calculate_relevancy(content, questions, messages):
    content_embedding = rel_model.encode(content, convert_to_tensor=True)
    question_embeddings = rel_model.encode(questions, convert_to_tensor=True)

    relevancy_scores = util.pytorch_cos_sim(content_embedding, question_embeddings)
    scores = relevancy_scores.squeeze().tolist()

    # Handle single-score scenario
    if isinstance(scores, float):
        scores = [scores]

    results = [(questions[i], scores[i]*100, messages[i].user.username) for i in range(len(scores))]
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def questionsdash(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room=room, tag="Not Spam")
    # print(room, messages)
    not_spam_questions = []
    for i in messages:
        not_spam_questions.append(i.content)
    rel_results = calculate_relevancy(room.content, not_spam_questions, messages)
    print(rel_results)

    return render(request, "questdash.html", {'most_relevant' : rel_results[0:15], "other_relevant" : messages})