import { getUserToken, removeUserToken } from "./auth";

const BACKEND_PATH = 'http://127.0.0.1:1337'
const API_BASE_PATH = BACKEND_PATH + '/api/'
const STANDARD_INIT = {
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
}


const sendRequest = async(url, init = {}) => fetch(url, init)
    .then(async(response) => {
        if (response.ok) {
            return response;
        } else {
            let errors;
            try {
                errors = await response.json();
                if (!errors) {
                    return undefined;
                }
                errors = errors['detail'];
            } catch {
                errors = response.text();
                if (!errors) {
                    return undefined;
                }
            }
            throw Error(errors)
        }
    });

export async function authentication(username, password) {
    const data = {
        'username': username,
        'password': password
    }
    const response = await sendRequest(
        API_BASE_PATH + 'auth/login', 
        {
            method: 'POST',
            body: JSON.stringify(data), 
            headers: {
                'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            ...STANDARD_INIT
        }
    );
    return await response.json();
}

function getAndValidAuthToken() {
    const token = getUserToken()
    if (!token) {
        removeUserToken();
        window.location.reload();
    }
    return token;
}

export async function getAllUsers()  {
    const token = getAndValidAuthToken();

    const response = await sendRequest(
        API_BASE_PATH + 'users/all', 
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token,
            },
            ...STANDARD_INIT
        }
    );
    return await response.json();
}


export async function createUser(createFields) {
    const token = getAndValidAuthToken();

    const response = await sendRequest(
        API_BASE_PATH + 'users/create', 
        {
            method: 'POST',
            body: JSON.stringify(createFields), 
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token,
            },
            ...STANDARD_INIT
        }
    );
    return await response.json();
}

export async function updateUser(updateFields) {
    const token = getAndValidAuthToken();

    const response = await sendRequest(
        API_BASE_PATH + 'users/update', 
        {
            method: 'POST',
            body: JSON.stringify(updateFields), 
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token,
            },
            ...STANDARD_INIT
        }
    );
    return await response.json();
}

export async function deleteUser(username) {
    const token = getAndValidAuthToken();

    const response = await sendRequest(
        API_BASE_PATH + `users/delete?username=${username}`, 
        {
            method: 'DELETE',
            headers: {
                'Authorization': token,
            },
            ...STANDARD_INIT
        }
    );
}