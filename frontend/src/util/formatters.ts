export function formatDate(date: string): string {
    return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
    });
}

export function formatDateHTML(date: string): string {
    return new Date(date).toISOString().split('T')[0];
}