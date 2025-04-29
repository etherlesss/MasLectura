import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user') || '{}'),
        tokenExpiration: localStorage.getItem('tokenExpiration') || null,
    }),
    actions: {
        setToken(token: any, expiration: any) {
            this.token = token;
            this.tokenExpiration = expiration;
            localStorage.setItem('token', token);
            localStorage.setItem('tokenExpiration', expiration);
        },
        setUser(user: any) {
            this.user = user;
            localStorage.setItem('user', JSON.stringify(user));
        },
        logout() {
            this.token = null;
            this.user = null;
            this.tokenExpiration = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            localStorage.removeItem('tokenExpiration');
        },
        isTokenValid() {
            if (!this.token || !this.tokenExpiration) {
                return false;
            }
            return Date.now() < new Date(this.tokenExpiration).getTime();
        }
    }
});