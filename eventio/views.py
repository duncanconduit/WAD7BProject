from django.shortcuts import render

def about(request):
    context_dict = {}
    context_dict['authors'] = [
        {'name': 'Brieuc Doucy', 'github_url': 'https://github.com/brieucdoucy', 'email': '2885025D@student.gla.ac.uk'},
        {'name': 'Duncan Conduit', 'github_url': 'https://github.com/duncanconduit', 'email': '3070971C@student.gla.ac.uk'},
        {'name': 'Robbie Copeland', 'github_url': 'https://github.com/rc1600', 'email': '2768763C@student.gla.ac.uk'},
        {'name': 'Junquan Chen', 'github_url': 'https://github.com/playersssssss', 'email': '2982317C@student.gla.ac.uk'},
    ]
    return render(request,'about.html', context=context_dict)