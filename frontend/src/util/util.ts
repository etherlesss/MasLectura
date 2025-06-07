import { API_URL } from '@/api/api';

export function getPortadaUrl(portada: string | undefined): string {
    if (!portada) return 'https://demuseo.com/wp-content/uploads/woocommerce-placeholder.png';
    if (portada.startsWith('http')) return portada;
    return API_URL + portada;
}