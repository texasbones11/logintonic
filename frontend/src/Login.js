import React, { useState } from 'react';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSimpleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5050/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      console.log('Login Success:', data);
    } catch (error) {
      console.error('Login Error:', error);
    }
  };

  const handleGitHubLogin = () => {
    window.open('http://localhost:5050/login/github', '_self');
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSimpleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login with Email/Password</button>
      </form>
      <hr />
      <button onClick={handleGitHubLogin}>Login with GitHub</button>
    </div>
  );
}

export default Login;
