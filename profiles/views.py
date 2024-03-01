from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import forms
from . import models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import random
import json

def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000000, 999999999))

def index(request):
    try:
        curr_user = models.Status.objects.get(user_name=request.user) # getting details of current user
    except:
        # if no details exist (new user), create new details
        curr_user = models.Status()
        curr_user.account_number = randomGen()# random account number for every new user
        curr_user.balance = 0
        curr_user.user_name = request.user
        curr_user.save()
    if request.user.groups.filter(name='Employee').exists():
        return render(request, "profiles/profile_employee.html", {"curr_user": curr_user})
    elif request.user.groups.filter(name='Customer').exists():
        return render(request, "profiles/profile_customer.html", {"curr_user": curr_user})

def money_transfer(request):
    if request.method == "POST":
        form = forms.MoneyTransferForm(request.POST)
        if form.is_valid():
            form.save()
            existing_user = models.Status.objects.get(user_name=request.user)
            curr_user = models.MoneyTransfer.objects.filter(enter_your_user_name=request.user).first()
            if curr_user:
                enter_the_destination_account_number = request.POST.get('enter_the_destination_account_number')
                enter_the_amount_to_be_transferred_in_INR = request.POST.get('enter_the_amount_to_be_transferred_in_INR')
                dest_user_acc_num = enter_the_destination_account_number
                destination_user = models.Status.objects.get(account_number=enter_the_destination_account_number)

                from_account_number = existing_user.account_number

                temp = curr_user  # NOTE: Delete this instance once money transfer is done
                transfer_amount = int(enter_the_amount_to_be_transferred_in_INR)  # FIELD 2
                print("transfer amount", transfer_amount)
                curr_user = models.Status.objects.get(user_name=request.user)  # FIELD 3

                print(curr_user.user_name)
                transaction = models.Transaction(
                    from_account_number=from_account_number,
                    to_account_number=dest_user_acc_num,
                    amount_transferred=transfer_amount,
                )
                transaction.save()
                if transfer_amount > 50000:
                    new_request = models.Request(from_account_number=from_account_number,
                                                 to_account_number=dest_user_acc_num,
                                                 amount_transferred=transfer_amount)
                    new_request.save()
                    print(new_request.id)
                    #
                    # Call the authorize_payment function
                        # Perform any additional actions if authorized
                    #     print("Transaction authorized!")
                    #     curr_user.balance = curr_user.balance - transfer_amount
                    #     print("curr_user_balance", curr_user.balance)
                    #     destination_user.balance = destination_user.balance + transfer_amount
                    #     curr_user.save()
                    #     destination_user.save()
                    # else:
                    #     # Handle unauthorized transaction
                    #     print("Transaction unauthorized!")
                else:
                    if curr_user.balance > transfer_amount:
                        curr_user.balance = curr_user.balance - transfer_amount
                        print("curr_user_balance", curr_user.balance)
                        destination_user.balance = destination_user.balance + transfer_amount
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Insufficient Balance to make the transaction'})
                    curr_user.save()
                    destination_user.save()
                temp.delete()  # NOTE: Now deleting the instance for future money transactions

        return redirect("profiles/profile_customer.html")
    else:
        form = forms.MoneyTransferForm()
    return render(request, "profiles/money_transfer.html", {"form": form})


def authorize_payment(request, request_id):
    if request.method == 'POST':
        # Retrieve the Request object
        payment_request = models.Request.objects.get(id=request_id)
        

        # Update the request_resolved field to True
        payment_request.request_resolved = True
        payment_request.save()


        from_user_status = models.Status.objects.get(account_number = payment_request.from_account_number)
        if from_user_status.balance > payment_request.amount_transferred:
            from_user_status.balance = from_user_status.balance - payment_request.amount_transferred
            print("curr_user_balance", from_user_status.balance)
            destination_user = models.Status.objects.get(account_number=payment_request.to_account_number)
            destination_user.balance = destination_user.balance + payment_request.amount_transferred
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient Balance to make the transaction'})
        from_user_status.save()
        destination_user.save()

        return JsonResponse({'status': 'success', 'message': 'Payment request authorized successfully and completed'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    # Indicate that the payment authorization was successful


def fetch_all_requests_not_resolved(request):
    if request.method == 'GET':
        # Retrieve all requests from the database
        all_requests = models.Request.objects.filter(request_resolved=False)

        # Create a list to store request details
        requests_list = []

        # Iterate through each request and extract relevant information
        for payment_request in all_requests:
            request_details = {
                'id': payment_request.id,
                'from_account_number': payment_request.from_account_number,
                'to_account_number': payment_request.to_account_number,
                'amount_transferred': str(payment_request.amount_transferred),
                'request_resolved': payment_request.request_resolved,
                'date_and_time': payment_request.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            requests_list.append(request_details)

        # Create a dictionary containing the list of requests
        response_data = {'requests': requests_list}

        # Return the data in JSON format
        return JsonResponse(response_data)

    # Handle other HTTP methods (optional)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=400)

def fetch_all_transactions_of_user(request,account_number):
    if request.method == 'GET':
        all_transactions = models.Transaction.objects.get(from_account_number=account_number)
        transactions_list = []

        # Iterate through each request and extract relevant information
        for transaction_request in all_transactions:
            transaction_details = {
                'id': transaction_request.id,
                'from_account_number': transaction_request.from_account_number,
                'to_account_number': transaction_request.to_account_number,
                'amount_transferred': str(transaction_request.amount_transferred),
                'date_and_time': transaction_request.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            transactions_list.append(transaction_details)

        # Create a dictionary containing the list of requests
        response_data = {'requests': transactions_list}

        # Return the data in JSON format
        return JsonResponse(response_data)

        # Handle other HTTP methods (optional)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


def fetch_all_transactions(request):
    if request.method == 'GET':
        # Retrieve all requests from the database
        all_transactions = models.Transaction.objects.all()

        # Create a list to store request details
        transactions_list = []

        # Iterate through each request and extract relevant information
        for transaction_request in all_transactions:
            transaction_details = {
                'id': transaction_request.id,
                'from_account_number': transaction_request.from_account_number,
                'to_account_number': transaction_request.to_account_number,
                'amount_transferred': str(transaction_request.amount_transferred),
                'date_and_time': transaction_request.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            transactions_list.append(transaction_details)

        # Create a dictionary containing the list of requests
        response_data = {'requests': transactions_list}

        # Return the data in JSON format
        return JsonResponse(response_data)

    # Handle other HTTP methods (optional)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=400)


def loan(request):
    return render(request, "profiles/loans.html")

def ewallet(request):
    return render(request, "profiles/eWallet.html")

def online_pay(request):
    return render(request, "profiles/online_payment.html")

def settings(request):
    return render(request, "profiles/settings.html")

def edit_details(request):
    if request.method == "POST":
        # POST actions for BasicDetailsForms
        try:
            curr_user = models.BasicDetails.objects.get(user_name=request.user)
            form = forms.BasicDetailsForm(request.POST, instance=curr_user)
            if form.is_valid():
                form.save()
        except:
            form = forms.BasicDetailsForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user_name = request.user
                form.save()

        # POST actions for PresentLocationForm
        try:
            curr_user = models.PresentLocation.objects.get(user_name=request.user)
            form = forms.PresentLocationForm(request.POST, instance=curr_user)
            if form.is_valid():
                form.save()
        except:
            form = forms.PresentLocationForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user_name = request.user
                form.save()     
        
        # POST actions for Password change
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')

        return redirect("profiles/edit_details.html")
    
    else: # GET actions
        try:
            curr_user = models.BasicDetails.objects.get(user_name=request.user)
            form1 = forms.BasicDetailsForm(instance=curr_user) # basic details
        except:
            form1 = forms.BasicDetailsForm()
        
        try:
            curr_user = models.PresentLocation.objects.get(user_name=request.user)
            form2 = forms.PresentLocationForm(instance=curr_user) # location
        except:
            form2 = forms.PresentLocationForm()

        # change password
        form3 = PasswordChangeForm(request.user)

        dici = {"form1": form1, "form2": form2, "form3": form3}
        return render(request, "profiles/edit_details.html", dici)

def delete_account(request):
    return render(request, "profiles/delete_account.html")

""" def transaction_requests(request):
    return render(request, 'profiles/transaction_requests.html')   """

def transaction_requests(request):
    # Call fetch_all_requests_not_resolved view function to get unresolved requests
    response = fetch_all_requests_not_resolved(request)
    if response.status_code == 200:
        # Extract JSON data from the response
        data = json.loads(response.content)
        # Pass the data to the template for rendering
        return render(request, 'profiles/transaction_requests.html', {'requests_data': data['requests']})
    else:
        # Handle error response (optional)
        return render(request, 'error.html', {'error_message': 'Failed to fetch transaction requests'})
