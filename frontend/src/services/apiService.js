const baseUrl = "http://127.0.0.1:8000/bets/"

export const getToken = (url, options) => {
    fetch(url, options)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            const token = data.token;
            localStorage.setItem('token', token);
            console.log('Token', token);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

export const fetchData = async () => {
    const url = `${baseUrl}api`;
    
    const token = localStorage.getItem('token');
    if (token === "undefined") {
        console.error('You are not logged in')
        return;
    }

    const options = {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
        }
    }

    try {
        const response = await fetch(url, options)
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
