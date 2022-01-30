import 'regenerator-runtime/runtime';

import {getUserToken} from './share/auth.js';


const app = async () => {
    document.getElementById('app').appendChild(await App());
};

async function App() {
    window._template = document.createElement('template');

    const token = getUserToken();
    
    let page = await import("./pages/login/login");
    if (token) {
        page = await import("./pages/users/users");
    }
    const innerHTML = page.render();

    window._template.innerHTML = `
        <div class="container">
        ${innerHTML}
        </div>
    `;
    return window._template.content.cloneNode(true);
}

// Load app
app();
