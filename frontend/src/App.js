import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [playlistUrl, setPlaylistUrl] = useState(null);
  const [status, setStatus]         = useState(null);   // 'success' | 'error' | null
  const [errorMsg, setErrorMsg]     = useState('');

  const handleLogin = () => {
    // kick off backend flow
    setStatus(null);
    window.location.href = 'http://localhost:5000/login';
  };

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const url    = params.get('playlist_url');
    const err    = params.get('error');
    if (url) {
      setPlaylistUrl(url);
      setStatus('success');
    } else if (err) {
      setErrorMsg(err);
      setStatus('error');
    }
  }, []);

  return (
    <div className="container">
      <h1 className="header">
        Take your<br/>
        musical<br/>
        snapshot
      </h1>

      {status === 'success' ? (
        <>
          <div className="message-success">
            🎉 Your playlist was created!
          </div>
          <a
            href={playlistUrl}
            className="open-button"
            target="_blank"
            rel="noopener noreferrer"
          >
            Open new playlist
          </a>
        </>
      ) : status === 'error' ? (
        <div className="message-error">
          ❌ Uh‑oh, something went wrong: {errorMsg}
        </div>
      ) : (
        <button className="spotify-button" onClick={handleLogin}>
          Create playlist
        </button>
      )}
    </div>
  );
}

export default App;
