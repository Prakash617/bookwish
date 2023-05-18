from django.shortcuts import render, redirect
from .models import PostEventFeedback

def feedback_view(request):
    if request.method == 'POST':
        post_event_feedback = PostEventFeedback(
            name=request.POST['name'],
            dob=request.POST['dob'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            permanent_address=request.POST['permanent_address'],
            gender=request.POST['gender'],
            feedback=request.POST['feedback'],
            is_interested=request.POST.get('is_interested') == 'on',
            expected_join_date=request.POST['expected_join_date'] or None,
        )
        # Save the instance to the database
        post_event_feedback.save()
    
        return redirect('feedback_success')
    
    return render(request, 'my_forms/feedback_form.html')




def feedback_success(request):
    return render(request, 'my_forms/feedback_success.html')

