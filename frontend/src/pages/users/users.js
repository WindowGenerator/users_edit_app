import {removeUserToken} from '../../share/auth';
import {getAllUsers, createUser as _createUser, deleteUser as _deleteUser, updateUser as _updateUser} from '../../share/api';


const GLOBAL = {};

const USERS_CONTAINER_ID = 'users-container';
const MODALS = `
<div class="modal" id="user-modal">
    <div class="modal-bg modal-exit" onclick="clearUserModalElements();"></div>
    <div class="modal-container">
        <button onclick="clearUserModalElements()" class="modal-close modal-exit">X</button>
        <h1 id="modal-title">Create User</h1>
        <div class="field-group">
            <label class="label">Username</label>
            <input class="input" type="text" name="username" id="username"
                placeholder="Enter Your Username">
            <div class= "underline"></div>
        </div>
        <div class="field-group">
            <label class="label">Email</label>
            <input class="input" type="text" name="email" id="email"
                placeholder="Enter Your Email">
            <div class= "underline"></div>
        </div>
        <div class="field-group">
            <label class="label">Bio</label>
            <textarea class="input" id="bio" placeholder="Enter Your Bio"></textarea>
            <div class= "underline"></div>
        </div>
        <div class="field-group">
            <label class="label">Password</label>
            <input class="input" type="password" name="password" id="password"
                placeholder="Enter Password">
            <div class= "underline"></div>
        </div>
        <div class="field-group">
            <label class="label">Permission</label>
            <select class="input" id="permission">
                <option value="right:view">View</option>
                <option value="right:full">Full</option>
            </select>
        </div>
        <button class="btn-base btn-submit modal-exit" onclick="createUser();" id="modal-submit">Create</button>
    </div>
</div>
`;

export function render() {
    const template = `
    <body>        
        ${MODALS}
        <main class="container">
            <div class="users-page-wrapper">
                <div class="bg-white">
                    <button class="btn-base btn-logout" onclick="logout()">Logout</button>
                    <button class="btn-base btn-create" data-modal="user-modal" type-modal="create">Create user</button>
                    <h1 class="text-title">Users</h1>
                    <div class="users-container" id="${USERS_CONTAINER_ID}"></div>
                </div>
            </div>
        </main>
    </body>
    `;

	return template;
}

export async function logout() {
    removeUserToken();
    window.location.reload();

}

function parseUserModal() {
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const bio = document.getElementById('bio');
    const permission = document.getElementById('permission');
    
    const userFields = {
        username: username.value ? username.value : undefined,
        email: email.value ? email.value : undefined,
        password: password.value ? password.value : undefined,
        bio: bio.value ? bio.value : undefined,
        permission: permission.value ? permission.value : undefined,
    }

    return userFields;
}

function setUserModalFields(user) {
    document.getElementById('username').value = user.username;
    document.getElementById('email').value = user.email;
    document.getElementById('password').value = "";
    document.getElementById('bio').value = user.bio;
    document.getElementById('permission').value = user.permission;
}

export function clearUserModalElements() {
    document.getElementById('username').value = "";
    document.getElementById('email').value = "";
    document.getElementById('password').value = "";
    document.getElementById('bio').value = "";
    document.getElementById('permission').value = "";
}

export async function createUser() {
    const userFields = parseUserModal();
    try {
        await _createUser(userFields);
    } catch (error) {
        alert(error);
    }
    clearUserModalElements();
    await reloadContent();
}

export async function updateUser() {
    const userFields = parseUserModal();
    try {
        await _updateUser(userFields);
    } catch (error) {
        alert(error);
    }
    clearUserModalElements();
    await reloadContent();
}

export async function deleteUser(userElem) {
    try {
        await _deleteUser(userElem.id);
    } catch (error) {
        alert(error);
    }
    await reloadContent();
}


async function onInit() {
   await reloadContent();
   initModals();
}

async function reloadContent() {
    const users = await getAllUsers();
    GLOBAL.users = {};
    for (let user of users) {
        GLOBAL.users[user.username] = user;
    }
    renderUsers(users);
}

function renderUsers(users) {
    const userContainer = document.getElementById(USERS_CONTAINER_ID);

    userContainer.innerHTML = `
            <div class="user-row">
                <label class="user-label">Username:</label>
                <label class="user-label">Email:</label>
                <label class="user-label">Bio:</label>
                <label class="user-label">Actions:</label>
            </div>
        `

    for (let user of users) {
        const userElement = document.createElement('user');

        userElement.id = user.username;

        userElement.innerHTML = `
            <div class="user-row">
                <label class="user-label">${user.username}</label>
                <label class="user-label">${user.email}</label>
                <label class="user-label">${truncateString(user.bio, 20)}</label>
                <div class="btn-container">
                    <button class="btn-base btn-from-container" data-modal="user-modal" type-modal="update" username="${user.username}">User card</button>
                    <button onclick="deleteUser(${user.username})" class="btn-base btn-from-container">Del</button>
                </div>
            </div>
        `
        userContainer.appendChild(userElement.cloneNode(true));
        
    }

}

function truncateString(str, num) {
    if (str.length > num) {
      return str.slice(0, num) + "...";
    } else {
      return str;
    }
  }


function initModals() {
    const modals = document.querySelectorAll("[data-modal]");

    modals.forEach(function (trigger) {
        console.log(trigger);
        trigger.addEventListener("click", function (event) {
            event.preventDefault();
            
            const typeModal = trigger.attributes['type-modal'].value;
            const modal = document.getElementById(trigger.dataset.modal);

            setValuesForUserModal(typeModal, trigger)

            modal.classList.add("open");

            const exits = modal.querySelectorAll(".modal-exit");
            exits.forEach(function (exit) {

                exit.addEventListener("click", function (event) {
                    event.preventDefault();
                    modal.classList.remove("open");
                });
            });
        });
    });
}

function setValuesForUserModal(typeModal, trigger) {
    if (typeModal === "update") {
        document.getElementById("modal-title").innerHTML = "Update User";
        document.getElementById("modal-submit").innerHTML = "Update";

        document.getElementById("modal-submit").onclick = (event) => updateUser();

        const user = GLOBAL.users[trigger.attributes['username'].value];
        setUserModalFields(user);   
    } else {
        document.getElementById("modal-title").innerHTML = "Create User";
        document.getElementById("modal-submit").innerHTML = "Create";

        document.getElementById("modal-submit").onclick = (event) => createUser();
    }
}


window.logout = logout;
window.deleteUser = deleteUser;
window.createUser = createUser;

window.clearUserModalElements = clearUserModalElements;
window.onload = onInit;
