from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

# Create your models here.
class reader(models.Model):
    reference_id=models.CharField(max_length=200)
    reader_name=models.CharField(max_length=200)
    reader_contact=models.CharField(max_length=200)
    reader_address=models.TextField()
    active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.reader_name

class Book(models.Model):
    title = models.CharField(max_length=200, default="")
    author = models.CharField(max_length=200, default="")
    isbn = models.CharField(max_length=20, unique=True, default="temp")  # We'll set a temporary default
    publication_year = models.IntegerField(default=2000)  # Set a reasonable default year
    category = models.CharField(max_length=100, blank=True, null=True)  # Make category optional
    available_copies = models.IntegerField(default=0)
    total_copies = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Book price for fine calculations
    added_date = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add to default
    
    def __str__(self):
        return self.title


class BookIssue(models.Model):
    # Status constants for penalty calculation
    PENALTY_POINT_LATE_PER_DAY = 1
    PENALTY_POINT_LOST = 5
    PENALTY_POINT_DAMAGED = 3
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(reader, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)
    is_damaged = models.BooleanField(default=False)
    damage_description = models.TextField(blank=True, null=True)
    penalty_points = models.IntegerField(default=0)
    fine_rate = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)  # Default daily fine rate
    
    def __str__(self):
        return f"{self.book.title} issued to {self.reader.reader_name}"

    def is_overdue(self):
        if not self.is_returned and timezone.now() > self.due_date:
            return True
        return False
    
    def calculate_overdue_days(self):
        """Calculate the number of days a book is overdue"""
        if not self.due_date:
            return 0
            
        if self.is_returned and self.return_date > self.due_date:
            # Calculate days between return_date and due_date
            delta = self.return_date - self.due_date
            return delta.days
        elif not self.is_returned and timezone.now() > self.due_date:
            # Calculate days between current time and due_date
            delta = timezone.now() - self.due_date
            return delta.days
        return 0
    
    def calculate_fine(self):
        """Calculate fine based on overdue days"""
        if self.is_lost:
            return self.calculate_lost_book_penalty()
        
        overdue_days = self.calculate_overdue_days()
        if overdue_days > 0:
            return Decimal(str(overdue_days)) * Decimal(str(self.fine_rate))
        return Decimal('0.00')
    
    def calculate_lost_book_penalty(self):
        """Calculate penalty for lost book (half of book price)"""
        if self.is_lost:
            return Decimal(str(self.book.price)) * Decimal('0.5')
        return Decimal('0.00')
    
    def get_total_amount_due(self):
        """Calculate the total amount due (fine + lost book penalty if applicable)"""
        total = Decimal('0.00')
        
        if self.is_lost:
            total += self.calculate_lost_book_penalty()
        elif self.is_damaged:
            # Add a damage fee (20% of book price)
            total += Decimal(str(self.book.price)) * Decimal('0.2')
            
        # Add overdue fine if applicable
        if not self.is_lost:  # Don't charge overdue fees for lost books
            total += self.calculate_fine()
            
        return total
        
    def calculate_penalty_points(self):
        """Calculate total penalty points"""
        points = 0
        
        # Points for late return
        overdue_days = self.calculate_overdue_days()
        if overdue_days > 0:
            points += overdue_days * self.PENALTY_POINT_LATE_PER_DAY
            
        # Points for lost book
        if self.is_lost:
            points += self.PENALTY_POINT_LOST
            
        # Points for damaged book
        if self.is_damaged:
            points += self.PENALTY_POINT_DAMAGED
            
        return points
    
    def update_penalty_points(self):
        """Update the penalty points based on current status"""
        self.penalty_points = self.calculate_penalty_points()
        return self.penalty_points
