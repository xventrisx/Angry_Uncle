__all__=[
    'is_auth',
	'add_project_perm',
	'send_invition_perm',
	'add_sprint_perm',
	'add_issue_perm',
	'chenge_issue_perm',
	'change_sprit_perm',
	'add_userstory_perm',
	'change_userstory_perm',
	'create_task_perm',
	'change_task_perm',

]

from django.http import HttpResponse



def is_auth(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.is_authenticated:
			return view(*args, **kwargs)
		else:
			return HttpResponse('User is not auth', status=403)
	return wrapper


def add_project_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.add_project'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def send_invition_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('management.send_invitation'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper

def add_sprint_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.add_sprint'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def add_issue_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.add_issue'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def chenge_issue_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.change_issue'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def change_sprit_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.change_sprint'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def add_userstory_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.add_userstory'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def change_userstory_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.change_userstory'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def create_task_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.add_task'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper


def change_task_perm(view):
	def wrapper(*args, **kwargs):
		if args[-1].user.has_perm('tasker.change_task'):
			return view(*args, **kwargs)
		else:
			return HttpResponse('Permission denied', status=403)
	return wrapper