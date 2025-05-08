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
        return res.data;
    } catch (err: any) {
        console.error('GET request error:', err.response);
        return err.response;
    }
}

export async function getProfile(id_usuario: number) {
    return GETRequest(`/profile/${id_usuario}`);
}

/*
    POST
*/
async function POSTRequest(endpoint: string, data: any) {
    try {
        const res = await axios.post(url + endpoint, data, config);
        return res.data;
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

/*
    PATCH
*/
async function PATCHRequest(endpoint: string, data: any) {
    try {
        const res = await axios.patch(url + endpoint, data, config);
        return res.data;
    } catch (err: any) {
        console.error('PATCH request error:', err.response);
        return err.response;
    }
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
        return res.data;
    } catch (err: any) {
        console.error('DELETE request error:', err.response);
        return err.response;
    }
}