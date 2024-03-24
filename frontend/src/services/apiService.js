export const getToken = () => {
    const url = 'http://127.0.0.1:8000/bets/api-token-auth/';
    const data = {
        username: 'offdout',
        password: 'ZhinL6L7*'
    };

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    };

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

export const fetchData = () => {
    const url = 'http://127.0.0.1:8000/bets/api';
    
    const token = localStorage.getItem('token');
    console.log("tokenzing", token);
    if (!token) {
        console.error('No token found in local storage')
    }

    const options = {
        headers: {
            'Authorization': `Token ${token}`,
        }
    }

    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('datas flag', data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
