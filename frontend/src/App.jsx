import { useState } from "react";
import Login from "./components/login";
import Registar from "./components/registar";
import Notes from "./components/notes";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [accessToken, setAccessToken] = useState("");
  const [refreshToken, setRefreshToken] = useState("");
  const [page, setPage] = useState("login"); 

  if (accessToken !== "") {
    return (
      <Notes
        API_URL={API_URL}
        accessToken={accessToken}
        refreshToken={refreshToken}
        setAccessToken={setAccessToken}
        setRefreshToken={setRefreshToken}
      />
    );
  }

  if (page === "registar") {
    return <Registar API_URL={API_URL} setPage={setPage} />;
  }

  return (
    <Login
      API_URL={API_URL}
      setAccessToken={setAccessToken}
      setRefreshToken={setRefreshToken}
      setPage={setPage}
    />
  );
}

export default App;