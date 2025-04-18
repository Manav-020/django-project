from django.shortcuts import render
from django.contrib import admin
from django.contrib import messages
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import *

# Create your views here.

def home(request):
    return render(request,"home.html",context={"current_tab": "home"})

def readers(request):
    return render(request,"readers.html",context={"current_tab": "readers"})

def shopping(request):
    return HttpResponse("Welcome to shopping")

def save_student(request):
    student_name= request.POST['student_name']
    return render(request,"welcome.html",context={'student_name':student_name})

def reader_tab(request):
    search_query = request.GET.get('search_query', '')
    
    if search_query:
        # Search across multiple fields
        readers = reader.objects.filter(
            models.Q(reader_name__icontains=search_query) |
            models.Q(reference_id__icontains=search_query) |
            models.Q(reader_contact__icontains=search_query)
        )
        
        # Check if any readers were found
        if not readers.exists():
            return render(request, "readers.html", context={
                "current_tab": "readers",
                "readers": [],
                "search_query": search_query,
                "no_results": True,
                "error_message": f"No readers found matching '{search_query}'"
            })
    else:
        readers = reader.objects.all()
    
    return render(request, "readers.html", context={
        "current_tab": "readers", 
        "readers": readers,
        "search_query": search_query
    })

def save_reader(request):
    reader_item=reader(
        reference_id=request.POST['reader_ref_id'],
        reader_name=request.POST['reader_name'],
        reader_contact=request.POST['reader_contact'],
        reader_address=request.POST['address'],
        active=True
    )
    reader_item.save()
    return redirect('/readers')

def edit_reader(request, id):
    if request.method == 'POST':
        reader_item = reader.objects.get(id=id)
        reader_item.reference_id = request.POST['reader_ref_id']
        reader_item.reader_name = request.POST['reader_name']
        reader_item.reader_contact = request.POST['reader_contact']
        reader_item.reader_address = request.POST['address']
        reader_item.active = True
        reader_item.save()
        return redirect('/readers')
    else:
        reader_item = reader.objects.get(id=id)
        return render(request, "edit_reader.html", context={"current_tab": "readers", "reader": reader_item})

def delete_reader(request, id):
    reader_item = reader.objects.get(id=id)
    reader_item.delete()
    return redirect('/readers')

def book_tab(request):
    try:
        # Add sample books if none exist
        if Book.objects.count() == 0:
            sample_books = [
                {
                    'title': 'The Great Gatsby',
                    'author': 'F. Scott Fitzgerald',
                    'isbn': '9780743273565',
                    'publication_year': 1925,
                    'category': 'Fiction',
                    'available_copies': 2,
                    'total_copies': 2,
                    'description': 'A story of decadence and excess.'
                },
                {
                    'title': 'To Kill a Mockingbird',
                    'author': 'Harper Lee',
                    'isbn': '9780446310789',
                    'publication_year': 1960,
                    'category': 'Fiction',
                    'available_copies': 3,
                    'total_copies': 3,
                    'description': 'A story of racial injustice and loss of innocence.'
                },
                {
                    'title': '1984',
                    'author': 'George Orwell',
                    'isbn': '9780451524935',
                    'publication_year': 1949,
                    'category': 'Science Fiction',
                    'available_copies': 1,
                    'total_copies': 1,
                    'description': 'A dystopian social science fiction novel.'
                }
            ]
            
            for book_data in sample_books:
                Book.objects.create(**book_data)
        
        # Get search query parameter
        search_query = request.GET.get('search_query', '')
        
        if search_query:
            # Search across multiple fields
            books = Book.objects.filter(
                models.Q(title__icontains=search_query) |
                models.Q(author__icontains=search_query) |
                models.Q(isbn__icontains=search_query) |
                models.Q(category__icontains=search_query)
            )
            
            # Check if any books were found
            if not books.exists():
                readers = reader.objects.all()
                return render(request, "books.html", context={
                    "current_tab": "books",
                    "books": [],
                    "readers": readers,
                    "search_query": search_query,
                    "no_results": True,
                    "error_message": f"No books found matching '{search_query}'"
                })
        else:
            books = Book.objects.all()
            
        readers = reader.objects.all()
        return render(request, "books.html", context={
            "current_tab": "books",
            "books": books,
            "readers": readers,
            "search_query": search_query
        })
    except Exception as e:
        return render(request, "books.html", context={
            "current_tab": "books",
            "books": [],
            "readers": [],
            "error_message": f"Error loading books: {str(e)}"
        })

def edit_book(request, id):
    try:
        if request.method == 'POST':
            book = Book.objects.get(id=id)
            
            # Validation for available copies <= total copies
            available_copies = int(request.POST['available_copies'])
            total_copies = int(request.POST['total_copies'])
            if available_copies > total_copies:
                return render(request, "edit_book.html", context={
                    "current_tab": "books", 
                    "book": book,
                    "error_message": "Available copies cannot exceed total copies."
                })
            
            # Validation for publication year (4 digits)
            pub_year = int(request.POST['publication_year'])
            if pub_year < 1000 or pub_year > 9999:
                return render(request, "edit_book.html", context={
                    "current_tab": "books", 
                    "book": book,
                    "error_message": "Publication year must be a valid 4-digit year."
                })
            
            # Check for ISBN uniqueness (only if ISBN changed)
            isbn = request.POST['isbn']
            if isbn != book.isbn and Book.objects.filter(isbn=isbn).exists():
                return render(request, "edit_book.html", context={
                    "current_tab": "books", 
                    "book": book,
                    "error_message": "A book with this ISBN already exists."
                })
            
            # If all validations pass, update the book
            book.title = request.POST['title']
            book.author = request.POST['author']
            book.isbn = isbn
            book.publication_year = pub_year
            book.category = request.POST['category']
            book.available_copies = available_copies
            book.total_copies = total_copies
            book.description = request.POST['description']
            book.price = float(request.POST.get('price', book.price))
            book.save()
            return redirect('/books')
        else:
            book = Book.objects.get(id=id)
            return render(request, "edit_book.html", context={"current_tab": "books", "book": book})
    except Exception as e:
        books = Book.objects.all()
        return render(request, "books.html", context={
            "current_tab": "books", 
            "books": books,
            "error_message": f"Error editing book: {str(e)}"
        })

def delete_book(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('/books')
    except Exception as e:
        books = Book.objects.all()
        return render(request, "books.html", context={
            "current_tab": "books", 
            "books": books,
            "error_message": f"Error deleting book: {str(e)}"
        })
def save_book(request):
    try:
        if request.method == 'POST':
            # Validation for available copies <= total copies
            available_copies = int(request.POST['available_copies'])
            total_copies = int(request.POST['total_copies'])
            if available_copies > total_copies:
                books = Book.objects.all()
                readers = reader.objects.all()
                return render(request, "books.html", context={
                    "current_tab": "books", 
                    "books": books,
                    "readers": readers,
                    "error_message": "Available copies cannot exceed total copies."
                })
            
            # Validation for publication year (4 digits)
            pub_year = int(request.POST['publication_year'])
            if pub_year < 1000 or pub_year > 9999:
                books = Book.objects.all()
                readers = reader.objects.all()
                return render(request, "books.html", context={
                    "current_tab": "books", 
                    "books": books,
                    "readers": readers,
                    "error_message": "Publication year must be a valid 4-digit year."
                })
            
            # Check for ISBN uniqueness
            isbn = request.POST['isbn']
            if Book.objects.filter(isbn=isbn).exists():
                books = Book.objects.all()
                readers = reader.objects.all()
                return render(request, "books.html", context={
                    "current_tab": "books", 
                    "books": books,
                    "readers": readers,
                    "error_message": "A book with this ISBN already exists."
                })
            
            # If all validations pass, create and save the book
            book = Book(
                title=request.POST['title'],
                author=request.POST['author'],
                isbn=isbn,
                publication_year=pub_year,
                category=request.POST['category'],
                available_copies=available_copies,
                total_copies=total_copies,
                description=request.POST['description'],
                price=float(request.POST.get('price', 0.00))  # Get book price with default of 0.00
            )
            book.save()
            messages.success(request, f"Book '{book.title}' has been added successfully")
            return redirect('/books')
    except Exception as e:
        books = Book.objects.all()
        readers = reader.objects.all()
        return render(request, "books.html", context={
            "current_tab": "books", 
            "books": books,
            "readers": readers,
            "error_message": f"Error saving book: {str(e)}"
        })

def issue_book(request):
    try:
        if request.method == 'POST':
            book_id = request.POST['book_id']
            reader_id = request.POST['reader_id']
            
            # Get loan duration from form, default to 14 days if not provided
            loan_duration = int(request.POST.get('loan_duration', 14))
            # Get fine rate from form, default to 10.00 if not provided
            fine_rate = float(request.POST.get('fine_rate', 10.00))
            
            book = Book.objects.get(id=book_id)
            reader_obj = reader.objects.get(id=reader_id)
            
            # Check if book is available
            if book.available_copies <= 0:
                raise Exception("No copies available for issue")
            
            # Check if reader already has this book
            existing_issue = BookIssue.objects.filter(
                book=book,
                reader=reader_obj,
                is_returned=False
            ).first()
            
            if existing_issue:
                raise Exception(f"This book is already issued to {reader_obj.reader_name}")
            
            # Set due date based on the loan duration
            due_date = timezone.now() + timedelta(days=loan_duration)
            
            # Create book issue record
            issue = BookIssue(
                book=book,
                reader=reader_obj,
                is_returned=False,
                due_date=due_date,
                fine_rate=fine_rate
            )
            issue.save()  # Save the issue record
            
            # Update available copies
            book.available_copies -= 1
            book.save()
            
            messages.success(request, f"Book '{book.title}' has been issued to {reader_obj.reader_name}")
            return redirect('/books')
            
    except Exception as e:
        books = Book.objects.all()
        readers = reader.objects.all()
        return render(request, "books.html", context={
            "current_tab": "books",
            "books": books,
            "readers": readers,
            "error_message": f"Error issuing book: {str(e)}"
        })

def view_issued_books(request):
    try:
        issued_books = BookIssue.objects.filter(is_returned=False)
        
        # Calculate all required values for display
        for book in issued_books:
            # Calculate overdue information
            book.overdue_days = book.calculate_overdue_days()
            book.is_overdue = book.is_overdue()
            
            # Calculate fines and fees
            book.current_fine = book.calculate_fine()
            book.damage_fee = Decimal(str(book.book.price)) * Decimal('0.2') if book.is_damaged else Decimal('0.00')
            book.lost_fee = book.calculate_lost_book_penalty() if book.is_lost else Decimal('0.00')
            
            # Calculate potential penalty points
            book.potential_penalty_points = book.calculate_penalty_points()
            
            # Calculate total amount due
            book.total_amount_due = book.get_total_amount_due()
        
        return render(request, "issued_books.html", context={
            "current_tab": "issued_books",
            "issued_books": issued_books
        })
    except Exception as e:
        return render(request, "issued_books.html", context={
            "current_tab": "issued_books",
            "issued_books": [],
            "error_message": f"Error loading issued books: {str(e)}"
        })

def return_book(request, issue_id):
    try:
        issue = BookIssue.objects.get(id=issue_id)
        
        # If the form was submitted with damage information
        if request.method == 'POST' and not issue.is_returned:
            is_damaged = request.POST.get('is_damaged') == 'yes'
            damage_description = request.POST.get('damage_description', '')
            
            issue.is_returned = True
            issue.return_date = timezone.now()
            
            # Set damage information if reported
            if is_damaged:
                issue.is_damaged = True
                issue.damage_description = damage_description
            
            # Calculate fine and penalty points
            fine_amount = issue.get_total_amount_due()
            issue.update_penalty_points()  # Update penalty points
            
            book = issue.book
            
            # Handle different cases (lost, damaged, returned)
            if issue.is_lost:
                # Book is lost, don't increment available copies
                penalty = issue.calculate_lost_book_penalty()
                messages.warning(request, f"Book '{book.title}' marked as lost. A penalty of ${penalty:.2f} and {issue.penalty_points} penalty points apply.")
            elif issue.is_damaged:
                # Book is damaged but returned to inventory
                book.available_copies += 1
                book.save()
                damage_fee = Decimal(str(book.price)) * Decimal('0.2')
                messages.warning(request, f"Book '{book.title}' reported as damaged. A fee of ${damage_fee:.2f} and {issue.penalty_points} penalty points apply. Description: {damage_description}")
            else:
                # Normal return
                book.available_copies += 1
                book.save()
                
                if fine_amount > 0:
                    messages.warning(request, f"Book '{book.title}' returned with a fine of ${fine_amount:.2f} and {issue.penalty_points} penalty points for late return.")
                else:
                    messages.success(request, f"Book '{book.title}' has been returned successfully. No penalties.")
            
            issue.save()
            return redirect('/books/issued')
            
        # If the request is to show the return form with damage options
        elif not issue.is_returned:
            book = issue.book
            # Calculate potential damage fee (20% of book price)
            damage_fee = Decimal(str(book.price)) * Decimal('0.2')
            
            return render(request, "return_book.html", {
                "issue": issue,
                "book": book,
                "damage_fee": damage_fee,
                "current_tab": "issued_books"
            })
        
        return redirect('/books/issued')
    except Exception as e:
        return render(request, "issued_books.html", context={
            "current_tab": "issued_books",
            "issued_books": BookIssue.objects.filter(is_returned=False),
            "error_message": f"Error returning book: {str(e)}"
        })

def returns(request):
    try:
        # Get only returned books, ordered by return date (most recent first)
        returned_books = BookIssue.objects.filter(
            is_returned=True
        ).order_by('-return_date')
        
        # Ensure penalty points are up to date
        for book_issue in returned_books:
            if book_issue.penalty_points == 0 and (book_issue.is_damaged or book_issue.is_lost or book_issue.calculate_overdue_days() > 0):
                book_issue.update_penalty_points()
                book_issue.save()
        
        # Calculate details for each returned book
        for book in returned_books:
            if book.return_date and book.due_date:
                book.returned_late = book.return_date > book.due_date
                if book.returned_late:
                    book.days_late = (book.return_date - book.due_date).days
                else:
                    book.days_late = 0
            else:
                book.returned_late = False
                book.days_late = 0
            
            # Calculate different components of fines
            book.late_fee = Decimal(str(book.days_late)) * Decimal(str(book.fine_rate)) if not book.is_lost else Decimal('0.00')
            book.damage_fee = Decimal(str(book.book.price)) * Decimal('0.2') if book.is_damaged else Decimal('0.00')
            book.lost_fee = book.calculate_lost_book_penalty() if book.is_lost else Decimal('0.00')
            book.total_fee = book.late_fee + book.damage_fee + book.lost_fee
        
        return render(request, "returns.html", context={
            "current_tab": "returns",
            "returned_books": returned_books
        })
    except Exception as e:
        return render(request, "returns.html", context={
            "current_tab": "returns",
            "returned_books": [],
            "error_message": f"Error loading return history: {str(e)}"
        })
def mark_as_lost(request, issue_id):
    try:
        issue = BookIssue.objects.get(id=issue_id)
        if not issue.is_returned and not issue.is_lost:
            issue.is_lost = True
            issue.save()
            
            book = issue.book
            penalty = issue.calculate_lost_book_penalty()
            
            # Book is lost, so don't increment available copies
            # Instead, reduce the total copies
            book.total_copies -= 1
            book.save()
            
            messages.warning(request, f"Book '{book.title}' marked as lost. A penalty of ${penalty} applies. Please pay at the counter.")
        
        return redirect('/books/issued')
    except Exception as e:
        return render(request, "issued_books.html", context={
            "current_tab": "issued_books",
            "issued_books": BookIssue.objects.filter(is_returned=False),
            "error_message": f"Error marking book as lost: {str(e)}"
        })
