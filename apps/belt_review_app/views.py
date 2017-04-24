from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.db.models import Count
# Create your views here.

def current_user(request):
	return User.objects.get(id=request.session['user_id'])



def index(request):

	return render(request, "belt_review_app/index.html")

def books(request):
	print request.session['user_name']
	context = {
		"recent_reviews": Review.objects.all().order_by('-created_at').all()[0:3],
		"current_user": current_user(request),
	}
	return render(request, "belt_review_app/success.html",context)

def addingbookandreviews(request):
	return render(request, "belt_review_app/addbook.html")	

def addingbookandreviewspost(request):
	if request.method != 'POST':
		return redirect('/bookadd')

	errors=[]
	is_valid = True

	if len(request.POST['book-title'])<2:
		is_valid = False
		errors.append('Book title cannot be blank')
	if len(request.POST['author'])<2:
		is_valid = False
		errors.append('Author field cannot be blank')
	if len(request.POST['review']) < 2:
		is_valid = False
		errors.append('Review field cannot be blank')
	print 'errors',errors
	if is_valid == False:
		for error in errors:
			messages.error(request,error)
			print error
		return redirect('/bookadd')

# if check[0] == False:
# 			for error in check[1]:
# 				print error
# 				messages.error(request,error)
# 			return redirect('/')

	else:
		author = Author.objects.create(name=request.POST['author'])
		book = Book.objects.create(title=request.POST['book-title'], author=author)
		review = Review.objects.create(
				user = current_user(request),
				book = book,
				review = request.POST['review'],
				rating = int(request.POST['rating'])
			)
		print book.id
		return redirect('/booksprofile/{}'.format(book.id))

def booksprofile(request,bookid):

	context = {
		"book": Book.objects.filter(id=bookid),
		"current_user": current_user(request),
	}

	return render(request,"belt_review_app/book.html",context)

def bookspost(request,bookid):
	if request.method != 'POST':
		return redirect('/booksprofile/{}'.format(bookid))

	elif len(request.POST['review']) < 2:
		return redirect('/booksprofile/{}'.format(bookid))

	else:
		book = Book.objects.get(id=bookid)
		review = Review.objects.create(
					user = current_user(request),
					book = book,
					review = request.POST['review'],
					rating = int(request.POST['rating'])
				)

		return redirect("/booksprofile/{}".format(bookid))

def deletereview(request,reviewid):
	# if 'user_id' not in reuqest.session:
	# 	return redirect('/')
	# else:
	review = Review.objects.get(id=reviewid)
	# print 'bookid',review.book.id
	review.delete()

	return redirect('/booksprofile/{}'.format(review.book.id))

def deletereviewfromhome(request,reviewid):
	# if 'user_id' not in reuqest.session:
	# 	return redirect('/')
	# else:
	review = Review.objects.get(id=reviewid)
	print 'bookid',review.book.id
	review.delete()

	return redirect('/books')




def userprofile(request,userid):
	# review = Review.objects.all().annotate(count=Count(['title']))
	# print review
	# print review
	# review.group_by=['title']
	# results = QuerySet(query=review, model=Review)
	# for i in review:
	# 	print i.book.title
	newarr=[]
	user = User.objects.get(id=userid)
	print user
	for review in user.reviews.all():
		print review.book
		if review.book not in newarr:
			newarr.append(review.book)
	print newarr


	context = {
		"reviews": newarr,
		"user": User.objects.get(id=userid),
		"current_user": current_user(request),
	}

	return render(request,"belt_review_app/user_profile.html",context)










def createUser(request):
	if request.method != 'POST':
		return redirect('/')
	else:

		check = User.objects.validateUser(request.POST)
		if check[0] == False:
			for error in check[1]:
				print error
				messages.error(request,error)
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
			user = User.objects.create(
				first_name = request.POST.get('first-name'),
				last_name = request.POST.get('last-name'),
				email = request.POST.get('email'),
				password = hashed_pw
			)
			print 'user_id: ',user.id
			request.session['user_id'] = user.id
			request.session['user_name'] = user.first_name
			return redirect('/books')



def login(request):
	print 'login'
	if request.method != 'POST':
		return redirect('/')
	else:
		#see if the email is in the db
		#
		user = User.objects.filter(email= request.POST.get('email')).first()
		if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
			request.session['user_name'] = user.first_name
			request.session['user_id'] = user.id
			return redirect('/books')
		else:
			messages.error(request,'invalid')
			return redirect('/')

def logout(request):
	request.session.pop('user_name',None)
	return redirect('/')



