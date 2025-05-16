import axios from 'axios';

// URL DEL SERVIDOR BACKEND
const url = 'http://127.0.0.1:6640/api';

const token = localStorage.getItem('token');

// Configurar axios
const config = {
    headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
    }
}

/*
    API REQUESTS
*/

/*
    GET
*/
async function GETRequest(endpoint: string) {
    try {
        const res = await axios.get(url + endpoint, config);
        return res;
    } catch (err: any) {
        console.error('GET request error:', err.response);
        return err.response;
    }
}

export async function getProfile(id_usuario: number) {
    return GETRequest(`/profile/${id_usuario}`);
}
export async function getTags() {
    return GETRequest('/tag');
}

export async function getBook(id: number) {
    return GETRequest(`/book/${id}`);
}
export async function getGenres() {
    return GETRequest('/genre');
}
export async function geBookGenres() {
    return GETRequest('/book_genre');
}
export async function getBookTags() {
    return GETRequest('/book_tag');
}
export async function getBooks() {
    return GETRequest('/book');
}

/*
    POST
*/
async function POSTRequest(endpoint: string, data: any) {
    try {
        const res = await axios.post(url + endpoint, data, config);
        return res;
    } catch (err: any) {
        console.error('POST request error:', err.response);
        return err.response;
    }
}

export async function login(data: any) {
    return POSTRequest('/login', data);
}

export async function signup(data: any) {
    return POSTRequest('/signup', data);
}

export async function addBookTag(data: any) {
    return POSTRequest('/book_tag', data);
}

export async function addBook(data: any) {
    return POSTRequest('/book', data);
}

export async function addBookGenre(data: any) {
    return POSTRequest('/book_genre', data);
}

export async function addGenre(data: any) {
    return POSTRequest('/genre', data);
}

export async function addTag(data: any) {
    return POSTRequest('/tag', data);
}

export async function uploadImage(formData: FormData) {
    try {
        const res = await axios.post(
            url + '/upload_image',
            formData,
            {
                headers: {
                    // Axios detecta FormData y pone el boundary automáticamente
                    'Authorization': token ? `Bearer ${token}` : '',
                }
            }
        );
        return res;
    } catch (err: any) {
        console.error('POST uploadImage error:', err.response);
        return err.response;
    }
}

/*
    PATCH
*/
async function PATCHRequest(endpoint: string, data: any) {
    try {
        const res = await axios.patch(url + endpoint, data, config);
        return res;
    } catch (err: any) {
        console.error('PATCH request error:', err.response);
        return err.response;
    }
}

export async function recoverPassword(mail: string) {
    return PATCHRequest('/recover-password', { mail });
}

export async function resetPassword(token: string, pwd: string) {
    return PATCHRequest('/reset-password', { token, pwd });
}

export async function updateProfile(id_usuario: number, data: any) {
    return PATCHRequest(`/profile/${id_usuario}`, data);
}

export async function updatePassword(id_usuario: number, data: any) {
    return PATCHRequest(`/profile/${id_usuario}/change-password`, data);
}

/*
    DELETE
*/
async function DELETERequest(endpoint: string, data: any = {}) {
    try {
        const res = await axios.delete(url + endpoint, {
        ...config,
        data: data
        });
        return res;
    } catch (err: any) {
        console.error('DELETE request error:', err.response);
        return err.response;
    }
}