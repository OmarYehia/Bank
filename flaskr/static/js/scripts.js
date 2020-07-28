// Global variables
let account_info = {};

// Creating account
document.querySelector('#create-form').onsubmit = e => {
    e.preventDefault()
    fetch('/accounts/create', {
        method: 'POST',
        body: JSON.stringify({
            'first_name': document.querySelector('#first_name').value,
            'last_name': document.querySelector('#last_name').value,
            'password': document.querySelector('#password_create').value,
            'balance': document.querySelector('#deposit_amount').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        if (jsonRes['success'] === false) {
            if (jsonRes['error'] === 400) {
                alert("There's a missing field!\nUser couldn't be created!");
                return;
            }
        }
        let account_header = document.querySelector('#account_header');
        account_header.innerHTML = 'Account successfully created, ' + jsonRes['first_name'] + ' ' +
                                    jsonRes['last_name'] + '.<br> Account number: ' + jsonRes['id'];
        let account_balance = document.querySelector('#account_balance');
        account_balance.innerHTML = 'You currently have ' + jsonRes['balance'] + ' $'
        document.querySelector('#account-actions').className = 'container text-center';
        document.querySelector('#create_account').disabled = true;
        document.querySelector('#first_name').disabled = true;
        document.querySelector('#last_name').disabled = true;
        document.querySelector('#password_create').disabled = true;
        document.querySelector('#deposit_amount').disabled = true;
        document.querySelector('#actions').className = 'container text-center';
        document.querySelector('#action-container').className = 'container text-center';
        document.querySelector('#total_accounts').innerHTML = 'There are currently ' + jsonRes['new_number_of_accounts'] + ' accounts';

        // Adding information to the global variables
        account_info.id = jsonRes['id'];
        account_info.balance = jsonRes['balance'];
        account_info['first_name'] = jsonRes['first_name'];
        account_info['last_name'] = jsonRes['last_name'];
        
    })
}

// Accessing account
document.querySelector('#get-account').onsubmit = e => {
    e.preventDefault();
    let account_id = document.querySelector('#account_id').value;
    let account_password = document.querySelector('#password_access').value;
    if (account_id === '' || account_password === '') {
        alert('Please enter a valid username or password!');
        return;
    }
    fetch('/accounts/' + account_id + '/' + account_password, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        if (jsonRes['success'] === false) {
            if (jsonRes['error'] === 404) {
                alert('This account ID is invalid!')
                return;
            } else if (jsonRes['error'] === 401) {
                alert('Wrong password!')
                return;
            } else if (jsonRes['error'] === 400) {
                alert('Username or Password is missing!')
            }
        }

        let account_header = document.querySelector('#account_header');
        account_header.innerHTML = 'Welcome back, ' + jsonRes['first_name'] + ' ' + jsonRes['last_name'];
        let account_balance = document.querySelector('#account_balance');
        account_balance.innerHTML = 'You currently have ' + jsonRes['balance'] + ' $'
        document.querySelector('#account-actions').className = 'container text-center';
        document.querySelector('#access_account').disabled = true;
        document.querySelector('#create_account').disabled = true;
        document.querySelector('#password_access').disabled = true;
        document.querySelector('#account_id').disabled = true;
        document.querySelector('#first_name').disabled = true;
        document.querySelector('#last_name').disabled = true;
        document.querySelector('#password_create').disabled = true;
        document.querySelector('#deposit_amount').disabled = true;
        document.querySelector('#actions').className = 'container text-center';
        document.querySelector('#action-container').className = 'container text-center';

        // Adding information to the global variables
        account_info['id'] = jsonRes['id'];
        account_info['balance'] = jsonRes['balance'];
        account_info['first_name'] = jsonRes['first_name'];
        account_info['last_name'] = jsonRes['last_name'];
    })
}

// Withdraw function
document.querySelector('#withdraw').onclick = e => {
    document.querySelector('#account_header').innerHTML = 'Welcome back, ' + account_info['first_name'] + ' ' + account_info['last_name'];
    fetch('/accounts/' + account_info['id'] + '/withdraw', {
        method: 'PATCH',
        body: JSON.stringify({
            'action_amount': document.querySelector('#action-amount').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        if (jsonRes['success'] === false) {
            if (jsonRes['error'] === 400) {
                alert('Please enter an amount to withdraw!')
                return;
            } else if (jsonRes['error'] === 422) {
                alert('Insufficient funds!')
                return;
            }
        }
        let account_balance = document.querySelector('#account_balance');
        account_balance.innerHTML = 'You currently have ' + jsonRes['new_amount'] + ' $'

        // Updating global variables with the new balance
        account_info['balance'] = jsonRes['new_amount'];
    })
}

// Deposit function
document.querySelector('#deposit').onclick = e => {
    document.querySelector('#account_header').innerHTML = 'Welcome back, ' + account_info['first_name'] + ' ' + account_info['last_name'];
    fetch('/accounts/' + account_info['id'] + '/deposit', {
        method: 'PATCH',
        body: JSON.stringify({
            'action_amount': document.querySelector('#action-amount').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        if (jsonRes['success'] === false) {
            if (jsonRes['error'] === 400) {
                alert('Please enter an amount to deposit!')
                return;
            } else if (jsonRes['error'] === 422) {
                alert('Please enter a valid number!')
                return;
            }
        }
        let account_balance = document.querySelector('#account_balance');
        account_balance.innerHTML = 'You currently have ' + jsonRes['new_amount'] + ' $'

        // Updating global variables with the new balance
        account_info['balance'] = jsonRes['new_amount'];
    })
}

// Delete account
document.querySelector('#delete_account').onclick = e => {
    fetch('/accounts/' + account_info['id'] + '/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        document.querySelector('#account_header').innerHTML = 'Sorry to see you leave, ' + jsonRes['first_name']
                                            + ' ' + jsonRes['last_name'] + '!';
        document.querySelector('#account_balance').innerHTML = 'You have ' + jsonRes['remaining_balance']
                                            + '$. You can withdraw them anytime on site.';
        document.querySelector('#actions').className = 'hidden';
        document.querySelector('#action-container').className = 'hidden';
        document.querySelector('#modify_name').className = 'container text-center hidden'
        document.querySelector('#modify_password').className = 'container text-center hidden'
        document.querySelector('#total_accounts').innerHTML = 'There are currently ' + jsonRes['remaining_accounts'] + ' accounts';
        document.querySelector('#access_account').disabled = false;
        document.querySelector('#create_account').disabled = false;
        document.querySelector('#password_access').disabled = false;
        document.querySelector('#account_id').disabled = false;
        document.querySelector('#first_name').disabled = false;
        document.querySelector('#last_name').disabled = false;
        document.querySelector('#password_create').disabled = false;
        document.querySelector('#deposit_amount').disabled = false;
    })
}

// Showing modify name form
document.querySelector('#modify_account_name').onclick = e => {
    console.log('click', e)

    // If the form is hidden on click it shows it and vice versa
    if (document.querySelector('#modify_name').className === 'container text-center hidden') {
        document.querySelector('#modify_name').className = 'container text-center';
    } else {
        document.querySelector('#modify_name').className = 'container text-center hidden';
    }

    // Populating the fields for the user
    document.querySelector('#modify_fname').value = account_info['first_name'];
    document.querySelector('#modify_lname').value = account_info['last_name'];

}

// Updating name
document.querySelector('#modify_name_form').onsubmit = e => {
    e.preventDefault()
    fetch('/accounts/' + account_info['id'] + '/modify_name', {
        method: 'PATCH',
        body: JSON.stringify({
            'first_name': document.querySelector('#modify_fname').value,
            'last_name': document.querySelector('#modify_lname').value
        }),
        headers: {
            'Content-Type': 'application/json'
        } 
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        if (jsonRes['success'] === false) {
            if (jsonRes['error'] === 400) {
                alert('Please enter the missing field!')
                return;
            } else if (jsonRes['error'] === 422) {
                alert('Something went wrong!')
                return;
            }
        }
        document.querySelector('#account_header').innerHTML = 'Your account name has successfully been updated to '
                            + jsonRes['first_name'] + ' ' + jsonRes['last_name'];
        document.querySelector('#modify_name').className = 'container text-center hidden'
        account_info['first_name'] = jsonRes['first_name'];
        account_info['last_name'] = jsonRes['last_name'];
    })

}

// Showing modify password form
document.querySelector('#modify_account_password').onclick = e => {
    console.log('click', e)

    // If the form is hidden on click it shows it and vice versa
    if (document.querySelector('#modify_password').className === 'container text-center hidden') {
        document.querySelector('#modify_password').className = 'container text-center';
    } else {
        document.querySelector('#modify_password').className = 'container text-center hidden';
    }
}

// Updating password
document.querySelector('#modify_password_form').onsubmit = e => {
    e.preventDefault()
    fetch('/accounts/' + account_info['id'] + '/modify_password', {
        method: 'PATCH',
        body: JSON.stringify({
            'old_password': document.querySelector('#old_password').value,
            'new_password': document.querySelector('#new_password').value
        }),
        headers: {
            'Content-Type': 'application/json'
        } 
    })
    .then(response => {
        return response.json();
    })
    .then(jsonRes => {
        if (jsonRes['success'] === false) {
            if (jsonRes['error'] === 400) {
                alert('Please enter the missing field!')
                return;
            } else if (jsonRes['error'] === 422) {
                alert('Something went wrong!')
                return;
            } else if(jsonRes['error'] === 401) {
                alert('Your old password does not match our records')
                return;
            }
        }

        document.querySelector('#account_header').innerHTML = 'Your password was successfuly changed!'
        document.querySelector('#modify_password').className = 'container text-center hidden';

    })

}

