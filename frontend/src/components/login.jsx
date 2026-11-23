import { useState } from "react";

function Login({ API_URL, setAccessToken, setRefreshToken, setPage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  function login() {
    fetch(API_URL + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, password: password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          if (typeof data.detail === "string") {
            setMsg(data.detail);
          } else {
            setMsg("Enter a valid email and password");
          }
        } else {
          setRefreshToken(data.refresh_token);
          setAccessToken(data.access_token);
        }
      });
  }

  return (
    <div>
      <h2>Login</h2>
      <p>{msg}</p>
      <input placeholder="Email" onChange={(lgin) => setEmail(login.target.value)} />
      <input type="password" placeholder="Password" onChange={(login) => setPassword(login.target.value)} />
      <button onClick={login}>Login</button>
      <button onClick={() => setPage("registar")}>Go to Register</button>
    </div>
  );
}

export default Login;