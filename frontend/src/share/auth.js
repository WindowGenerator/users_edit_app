const USER_TOKEN_LOCATION = 'dummy-user-token';


export function getUserToken() {
    return window.localStorage.getItem(USER_TOKEN_LOCATION);
}

export function setUserToken(token) {
    window.localStorage.setItem(USER_TOKEN_LOCATION, token);
}

export function removeUserToken() {
    window.localStorage.removeItem(USER_TOKEN_LOCATION);
}