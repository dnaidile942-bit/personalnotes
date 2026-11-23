import { useState } from "react";

function Registar({ API_URL, setPage }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  function register() {
    fetch(API_URL + "/register", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify({ username: username, email: email, password: password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          if (typeof data.detail === "string") {
            setMsg(data.detail);
          } else {
            setMsg("Enter a valid email and a password");
          }
        } else {
          setMsg("Registered successfully");
        }
      });
  }

  return (
    <div>
      <h2>Register</h2>
      <p>{msg}</p>
      <input placeholder="Username" onChange={(name) => setUsername(name.target.value)} />
      <input placeholder="Email" onChange={(mail) => setEmail(mail.target.value)} />
      <input type="password" placeholder="Password" onChange={(pswd) => setPassword(pswd.target.value)} />
      <button onClick={register}>Register</button>
      <button onClick={() => setPage("login")}>Go to Login</button>
    </div>
  );
}

export default Registar;