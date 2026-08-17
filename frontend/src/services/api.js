export async function apiFetch(url, options = {}) {
    const token = localStorage.getItem("access_token")

    const response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${token}`,
        },
    })

    if (response.status === 401) {
        localStorage.removeItem("access_token")
        window.location.reload()
        return
    }

    return response
}