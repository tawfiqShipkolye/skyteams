from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from django.contrib.auth import get_user_model

# Author: Student 3 - Tawfiq

User = get_user_model()

@login_required
def inbox(request):
    received = Message.objects.filter(
        recipients=request.user,
        is_draft=False
    )
    return render(request, 'messaging/inbox.html', {'messages_list': received})

@login_required
def sent(request):
    sent_messages = Message.objects.filter(
        sender=request.user,
        is_draft=False
    )
    return render(request, 'messaging/sent.html', {'messages_list': sent_messages})

@login_required
def drafts(request):
    draft_messages = Message.objects.filter(
        sender=request.user,
        is_draft=True
    )
    return render(request, 'messaging/drafts.html', {'messages_list': draft_messages})

@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if 'save_draft' in request.POST:
                message.is_draft = True
            else:
                message.is_draft = False
            message.save()
            form.save_m2m()
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/compose.html', {'form': form})

@login_required
def view_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user in message.recipients.all():
        message.is_read = True
        message.save()
    return render(request, 'messaging/view_message.html', {'message': message})

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.sender == request.user:
        message.delete()
        messages.success(request, 'Message deleted.')
    return redirect('inbox')