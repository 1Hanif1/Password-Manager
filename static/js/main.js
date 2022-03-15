
const generate_button = document.querySelector('.nav__register')
const password_field = document.querySelector('.gen--pass')
const savepass_form = document.querySelector('.save__pass');
const genPassBtn = document.querySelector('.btn--one');
const viewPassBtn = document.querySelector('.btn--two');
const searchPassBtn = document.querySelector('.btn--three');
const searchBtn = document.querySelector('.search_password');
const genPassDiv = document.querySelector('.dashboard__generate--password')
const viewPassDiv = document.querySelector('.dashboard__view--password')
const searchPassDiv = document.querySelector('.dashboard__search--password')
const table = document.querySelector('.password--table');
const table_two = document.querySelector('.search__pass--table');
const allDashboardDiv = [genPassDiv, viewPassDiv, searchPassDiv]
const allDashboardBtn = [genPassBtn, viewPassBtn, searchPassBtn]

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

generate_button.addEventListener('click', async function (e) {
    let data = await fetch('/gen_pass')
    data = await data.json()
    password_field.value = data['password']
})

savepass_form.addEventListener('submit', async function (e) {
    e.preventDefault();
    let message = document.querySelector('.success__message')
    let website_name = document.querySelector('.gen--website');
    let user_name = document.querySelector('.gen--username');
    let generated_password = document.querySelector('.gen--pass');


    data = await fetch('/save_pass', {
        method: "POST",
        body: JSON.stringify(
            {
                'user': session_username,
                'website': website_name.value.toLowerCase(),
                'username': user_name.value,
                'password': generated_password.value,
            }
        ),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })

    data = await data.json()

    if (data['message'] == 'Saved') {
        [website_name, user_name, generated_password].forEach(input => input.value = null)
        message.textContent = "Password Saved Succesfully"
        setTimeout(() => message.textContent = '', 3000)
    } else if (data['message'] == 'Exists') {
        message.textContent = "Account for website with this username already exists."
        setTimeout(() => message.textContent = '', 3000)
    } else {
        message.textContent = "There was an Error"
        setTimeout(() => message.textContent = '', 3000)
    }

})


const resetDashboard = function () {
    allDashboardDiv.forEach(div => div.classList.add('hide'))
    allDashboardBtn.forEach(div => div.classList.remove('active'))
}

genPassBtn.addEventListener('click', function () {
    resetDashboard()
    genPassDiv.classList.remove('hide');
    this.classList.add('active')
})

const deletePassword = async function (e) {
    if (!e.target.classList.contains('delete_password')) return
    const table_row = e.target.closest('tr');
    const data = {
        "website": table_row.querySelector('.website--js').textContent,
        "username": table_row.querySelector('.username--js').textContent,
        "password": table_row.querySelector('.password--js').textContent,
    }
    let response = await fetch('/del_pass', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    response = await response.json()
    if (response.message == "OK") {
        table_row.parentNode.removeChild(table_row)
    }
}

const addDataToTable = function (data, table) {
    let passwords = data['passwords']
    passwords.forEach(password => {
        const table_row = `
                <tr>
                    <td class="website--js">${password.website}</td>
                        <td class="username--js">${password.username}</td>
                        <td class="password--js">${password.password}</td>
                        <td>
                            <button class="delete_password" type="submit">Delete</button>
                        </td>
                </tr>
                `
        table.insertAdjacentHTML('beforeend', table_row);
    })
}

viewPassBtn.addEventListener('click', async function () {
    if (this.classList.contains('active')) return;
    table.innerHTML = null;
    let table_headers = `
            <tr>
                <th>Website</th>
                <th>Username</th>
                <th>Password</th>
                <th>Delete</th>
            </tr>
            `
    table.insertAdjacentHTML('beforeend', table_headers)
    resetDashboard()
    viewPassDiv.classList.remove('hide')
    this.classList.add('active')
    let data;
    data = await fetch("/get_pass")
    data = await data.json()
    addDataToTable(data, table);
})

table_two.addEventListener('click', async (e) => {
    if (e.target.classList.contains("search_password")) {
        const search_string = document.querySelector('.search_password_input').value
        if (!search_string) return;
        data = await fetch(`/search_pass`, {
            method: "POST",
            body: JSON.stringify({
                'username': session_username,
                'website': search_string.toLowerCase(),
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        data = await data.json()
        table_two.innerHTML = null;
        let table_headers = `
            <tr>
                <th colspan="3"><input placeholder="Search for a website" class="search_password_input" type="text"></th>
                <th><button class="search_password" type="submit">Search</button></th>
            </tr>
            `
        table_two.insertAdjacentHTML('beforeend', table_headers)
        addDataToTable(data, table_two)
    } else if (e.target.classList.contains('delete_password')) {
        deletePassword(e)
    } else return;
})

searchPassBtn.addEventListener('click', async function () {
    resetDashboard()
    searchPassDiv.classList.remove('hide')
    this.classList.add('active')
    table_two.innerHTML = null;
    let table_headers = `
            <tr>
                <th colspan="3"><input placeholder="Search for a website" class="search_password_input" type="text"></th>
                <th><button class="search_password" type="submit">Search</button></th>
            </tr>
            `
    table_two.insertAdjacentHTML('beforeend', table_headers)
})

table.addEventListener('click', deletePassword.bind(this))
