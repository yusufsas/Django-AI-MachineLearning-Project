import React, { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/api') // Django sunucusunun adresini doğru olarak ayarlayın
      .then(response => response.json())
      .then(data => {
        console.log(data); // Kontrol amaçlı
        setMessage(data.message);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>{message}</h1>
      </header>
      <main>
        <p>Welcome to my Django and React App!</p>
      </main>
    </div>
  );
}

export default App;