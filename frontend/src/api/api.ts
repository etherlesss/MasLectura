import axios from 'axios';

// URL DEL SERVIDOR BACKEND
const url = 'http://127.0.0.1:3307/api';

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

export async function getList(id_lista: number) {
    return GETRequest(`/list/${id_lista}`);
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
export async function getGenresById(id: number) {
    return GETRequest(`/book_genre/${id}`);
}
export async function getBookTags() {
    return GETRequest('/book_tag');
}

export async function getTagsIdBook(id: number) {
    return GETRequest(`/book_tag/${id}`);
}

export async function getBooks() {
    return GETRequest('/books');
}

export async function getDetailedBooks() {
    return GETRequest('/books/detailed');
}

export async function getUserLists(id_usuario: number) {
    return GETRequest(`/profile/${id_usuario}/lists`);
}

export async function getListFirstBook(id_lista: number) {
    return GETRequest(`/list/${id_lista}/first-book`);
}

export async function getListBooks(id_lista: number) {
    return GETRequest(`/list/${id_lista}/books`);
}
export async function getCommentsByBook(id_libro: number) {
    return GETRequest(`/comentario/${id_libro}`);
}

export async function getRecommendations(id_usuario: number) {
    return GETRequest(`/recommend?id_usuario=${id_usuario}`);
}
export async function getUserRole(id_usuario: number) {
  return GETRequest(`/user/role/${id_usuario}`);
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

export async function createList(data: any) {
    return POSTRequest('/list', data);
}

export async function rateBook(data: any, id_libro: number) {
    return POSTRequest(`/book/${id_libro}/rate`, data);
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

export async function addComment(data: { id_usuario: number, descripcion: string, id_libro: number}) {
    return POSTRequest('/comentario', data);
}

export async function addBookToList(data: { id_lista: number, id_libro: number }) {
  return POSTRequest('/list/add-book', data);
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

export async function updateList(id_lista: number, data: any) {
    return PATCHRequest(`/list/${id_lista}`, data);
}
export async function updateBook(id_libro: number, data: any) {
    return axios.patch(`${url}/book/edit/${id_libro}`, data, config);
}
export async function updateBookGenres(id_libro: number, data: any) {
    return axios.put(`${url}/book_genre/edit/${id_libro}`, data, config);
}

export async function updateBookTags(id_libro: number, data: any) {
    return axios.put(`${url}/book_tag/edit/${id_libro}`, data, config);
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

export async function removeBookFromList(id_lista: number, id_libro: number) {
    return DELETERequest(`/list/${id_lista}/book/${id_libro}`);
}

export async function deleteList(id_lista: number) {
    return DELETERequest(`/list/${id_lista}`);
}

export async function deleteComment(id_comentario: number) {
    return DELETERequest(`/comentario/${id_comentario}`);
}
export async function deleteUser(id_usuario: number) {
    return DELETERequest(`/user/${id_usuario}`);
}