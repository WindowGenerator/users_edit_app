import {getUserToken, setUserToken, removeUserToken} from '../../share/auth';
import {authentication} from '../../share/api';


// законс под реакт, но на самом деле ванила
export function render() {
    const template = `
    <body>
        <main class="container login-page">
            <div class="form-wrapper">
                <div class="bg-white">
                    <h1 class="text-title">Login</h1>
                    <div class="field-group">
                        <label class="label">Username</label>
                        <input class="input" type="text" name="username" id="username"
                            placeholder="Enter Your Username">
                        <div class= "underline"></div>
                    </div>
                    <div class="field-group">
                        <label class="label">Password</label>
                        <input class="input" type="password" name="password" id="password"
                            placeholder="Enter Your Password">
                        <div class="underline"></div>
                    </div>
                    <button class="btn-base btn-submit" onclick="login();">Submit</button>
                </div>
            </div>
        </main>
    </body>
    `;

	return template;
}

function username() {
    return document.getElementById('username').value;
}

function password() {
    return document.getElementById('password').value;
}

function validateInput() {
    if (!username()) {
        throw 'не указано имя пользователя';
    }

    if (!password()) {
        throw 'не указано имя пользователя';
    }
}

export async function login() {
    let user;
    try {
        validateInput();

        user = await authentication(username(), password());
    } catch (error) {
        alert(error);
        return;
    }
    setUserToken(user['access_token']);

    window.location.reload();

}
window.login = login;